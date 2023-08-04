'''
Generally, there are several functions that need to run to make the LSM tree work:
Write Data
Read Data
Search Data
Compaction
Deletion

Helper functions may include:
Bloom filter
Sparse index

Each of these is defined below:

Write Data:
    When memtable reaches <arbitrary size>, write contents of memtable to disk in KEY-sorted order

Read Data:
    First we check the Bloom Filter to see if the KEY exists
    If NO: return "key does not exist"
    If YES: iterate from latest segment file to oldest, looking for MOST RECENT key:value pair

Search Data:
    First search for key:value in memTable
    If not present, search from most recent file backwards, since only the most recent key:value is relevant

Compaction:
Compare key:value pairs across segments and update to most recent value:
    1. If newest value is tombstone marker: delete key:value
    2. Write neweset segment to incldue most recent key:value pair


'''

import collections
import os
import uuid
import json

DELETED = None

class LSMTree():

    def __init__(self, tree_dir: str) -> None:
        self.file_tree = collections.deque([])      #using deque to make left append efficient O(1) instead of O(n) with list
        self.tree_dir = 'LSM_chunks/'
        self.mem_table = {}

    def search_LSM(self, key):
        # return 'None' if key has been deleted or if element does not exist
        if str(key) in self.mem_table:
            print('found in mem table')
            return self.mem_table.get(key)
        else:
            print('not found in mem table, searching disk')
            return self.search_LSM_files(key)
        print('Key not found in LSM')
        return None

    def search_LSM_files(self, key):
        for files in self.file_tree:
            contents_dict = self.load_to_memory(files)
            if key in contents_dict:
                print(f'key found in file {files}')
                return contents_dict.get(key)
            contents_dict.clear()
        return None

    #add a trigger to dump mem_table to disk
    def write(self, key, value):        #put
        key = str(key)
        self.mem_table.setdefault(key, 0)
        self.mem_table[key] = value
        with open('lsm.log', 'a') as f:
            json.dump(self.mem_table, f)
            #f.write(f'{key}:{value}\n')

    def read(self, key):                #get
        key = str(key)
        if key in self.mem_table:
            return self.mem_table.get(key)
        
    def delete(self, key):
        key = str(key)
        self.mem_table.setdefault(key, 0)
        self.mem_table[key] = None
        with open('lsm.log', 'a') as f:
            json.dump(self.mem_table, f)
            #f.write(f'{key}:{None}\n')


    def filename_generator(self) -> str:
        #creates a "unique" filename in a specified directory and returns it as a string
        return self.tree_dir + str(uuid.uuid4())

#when to write to disk? and should file size be limited to xxxx kb?
#should sstable have a default assignment of self.mem_table? 
#or should compaction have its own write to disk method so self.file_tree doesn't get totally messed up?
    def flush_mem_table(self, filename):
        #re-wrote the above code using JSON instead. Significantly more compact
        filename = self.filename_generator()
        with open(filename, 'w') as j:
            json.dump(self.mem_table, j, sort_keys=True)
        self.file_tree.appendleft(filename)
        #clear the mem_table log file
        with open('lsm.log', 'w') as log:
            log.write('')

        #WISHLIST: A meta file that provides line no. for data in files across the structure
        #to behave like a skip list for lookup

    def load_to_memory(self, filename):
        with open(filename, 'r') as read_file:
            return json.load(filename)


#lay good groundwork...
#eventually the structure is too large to be confined to one file after compaction
#How to plan for this?
#Compaction is likely too big to fit all in memory, so a log of the process is necessary
#ANSWER:
#Merge sort two chunk files together (divide as necessary afterwards?) at a time, 

    def compaction(self):
        compaction_file_tree = []
        #First, let's delete all of the tombstoned values, sequentially
        # mem_table first
        tombstone_list = [key for key, value in self.memtable.items() if value == None]
        for key in tombstone_list:
            self.mem_table.pop(key)
        # files next, in order from most recent to oldest
        for f in self.file_tree:
            with open(f, 'r') as j:
                json_dict = json.load(f)
                tombstone_list_builder = [key for key, value in json_dict.items() if value == None]
                tombstone_list.extend(tombstone_list_builder)
                tombstone_list_builder.clear()
                for key in tombstone_list:
                    if key in json_dict:
                        json_dict.pop(key)
            with open(f,'w') as j:    
                json.dump(json_dict, j)
        
        # free up a little memory
        tombstone_list.clear()

        #Now all tombstoned keys should be gone, lowering our comparisons

        
        #this might need to be written as a function that is called with two dictionaries
        #so compaction can consolidate 2 files into 1 (recursively?), eventually resulting in 1 file
        compaction_dict = {}
        
        file_tree_len = len(self.file_tree) - 1
        while self.file_tree:

            compaction_file_tree.append(self.compaction_merge_sort())
        
            #killing file_tree elements to satisfy loop calling this function. Maybe move it up there?
            os.remove(self.file_tree[0])
            self.file_tree.popleft()

            self.balance_files(compaction_file_tree)
        
        #write to file
        
        with open(filename, 'w'):
            json.dump(compaction_dict)

        #then balance file sizes for memory loading consideration...

    def compaction_merge_sort(self):
        #might want to pass two dicts as arguments? Handle the opening and loading in self.compaction?
        compaction_dict = {}
        #load two adjacent chunks
        recent_contents_dict = self.load_to_memory(self.file_tree[0])
        older_contents_dict = self.load_to_memory(self.file_tree[1])
        
        #put keys into indexed format, deque to maintain constant pop(0) time complexity
        ordered_keys_recent = collections.deque(recent_contents_dict.keys())
        ordered_keys_older = collections.deque(older_contents_dict.keys())
        #using the two deques, merge sort two dicts into one
        while ordered_keys_recent and ordered_keys_older:
            if ordered_keys_recent[0] <= ordered_keys_older[0]:
                if ordered_keys_recent[0] == ordered_keys_older[0]:
                    older_contents_dict.pop(ordered_keys_older[0])
                    ordered_keys_older.popleft()
                compaction_dict.update(recent_contents_dict.pop(ordered_keys_recent[0]))
                ordered_keys_recent.popleft()
            else:
                compaction_dict.update(older_contents_dict.pop(ordered_keys_older(0)))
                ordered_keys_older.popleft()
        
        return compaction_dict

    def balance_files(self, compaction_tree: list):
        for f in compaction_tree:
            with open(f, 'r'):
                contents_dict = json.load(f)
            if len(content_dict) >= 5:
                sorted_keys = sorted(contents_dict.keys())
                
                
    def compaction_write(compaction_dict: dict):
        with open('compaction/testing', 'w'):
            json.dump(compaction_dict)


    def recover_LSM(self):
        #import os, glob
        #search dir and return list of files in order of creation (newest first), this becomes self.file_tree
        #side note: may have to pass in a dir as an argument
        #call recover_from_log to rebuild current mem_table
        pass

    def recover_from_log(self):
        temp_tuple = tuple()
        with open('LSM.log') as f:
            for lines in f:
                #print(lines)
                try:
                    lines = lines[:-1]
                    temp_tuple = (lines.split(':'))
                    (key, value) = temp_tuple
                    self.mem_table[key] = value
                except:
                    pass

        
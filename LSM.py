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
import linecache
import uuid
import json

DELETED = None

class LSMTree():

    def __init__(self, tree_dir: str) -> None:
        self.file_tree = collections.deque([])      #using deque to make left append efficient O(1) instead of O(n) with list
        self.tree_dir = tree_dir
        self.mem_table = {}

    def search_LSM(self, key): #does this funcion return anything?
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

    
    def write(self, key, value):        #put
        key = str(key)
        self.mem_table.setdefault(key, 0)
        self.mem_table[key] = value
        with open('lsm.log', 'a') as f:
            f.write(f'{key}:{value}\n')

    def read(self, key):                #get
        key = str(key)
        if key in self.mem_table:
            return self.mem_table.get(key)
        
    def delete(self, key):
        key = str(key)
        self.mem_table.setdefault(key, 0)
        self.mem_table[key] = None
        with open('lsm.log', 'a') as f:
            f.write(f'{key}:{None}\n')


    def filename_generator(self) -> str:
        #creates a "unique" filename in a specified directory and returns it as a string
        return str(uuid.uuid4())

#when to write to disk? and should file size be limited to xxxx kb?
    def write_to_disk(self, sstable: dict, filename):
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
        '''read_file = open(filename)
        file_contents = read_file.read()
        file_contents_dict = file_contents.split('\n')
        file_contents_dict = [items.split(':') for items in file_contents_dict] #make this a generator
        return dict(file_contents_dict)
'''
        #re-write the above using JSON
        with open(filename, 'r') as read_file:
            return json.load(filename)


#lay good groundwork...
#eventually the structure is too large to be confined to one file after compaction
#How to plan for this?
#Compaction is likely too big to fit all in memory, so a log of the process is necessary
#ANSWER:
#load first elements from each sorted file and compare across files, write lowest key:value to compacted file, pop, repeat

    def compaction(self):
        #First, let's delete all of the tombstoned values, sequentially
        # mem_table first
        tombstone_list = [key for key, value in self.memtable.items() if value == None]
        for key in tombstone_list:
            self.mem_table.pop(key)
        # files next, in order from most recent to oldest
        for f in self.file_tree:
            with open(f, 'r') as j:
                json_dict = j.load()
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
        #Next load n elements from each chunk file, then compare the firts 
                #This might not work with JSON. 
                #Maybe the data needs to be in DIRs and broken into smaller chunks?
                #Maybe I can work with a different sorting algorithm?

                

        
        if key in compaction_dict:
            pass

        elif key in tombstone_set:
            pass

        else:
            compaction_dict[key] = value


    '''compaction can be done in one pass:
    compare the first elements across sorted files something like this

    for files in file_tree:
        first_elems.append((files[0], files[1]))        #gets first element from each file
        first_elems.sort()
        while first_elems[0] == 'del' or first_elems[0] in tombstone_set:
            tombstone_set.add(first_elems[0])
            file.pop(first_elems[0])
            first_elems.pop(0)
        while first_elems[0] == file.lastadded:
            first_elems.pop(0)
        file.write(first_elems[0])
        #pop first_elems[0] from its file and repeat
        
    something like that. Definitely some bugs built into this code, what if the whole first_elems list is dupes?
    Maybe make a short elements cache list, duplicates should come up at the same time across files


    This approach might have me changing the format of .txt output to many lines
    file.readline() could be the solution for compaction'''



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

        
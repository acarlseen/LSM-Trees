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

class LSMTree():

    def __init__(self, tree_dir: str) -> None:
        self.file_tree = collections.deque([])      #using deque to make left append efficient O(1) instead of O(n) with list
        self.tree_dir = tree_dir
        self.mem_table = {}

    def search_LSM(self, key): #does this funcion return anything?
        if key in self.mem_table:
            print('found in mem table')
            return self.mem_table.get(key)
        else:
            print('not found in mem table, searching disk')
            return self.search_LSM_files(key)
        print('Key not found in LSM')
        return None

    def search_LSM_files(self, key):
        for files in self.file_tree:
            current = open(files)
            contents_dict = current.read()
            contents_dict = contents_dict.split(',')
            contents_dict = [items.split(':') for items in contents_dict]
            if key in contents_dict:
                print(f'key found in file {files}')
                return contents_dict.get(key)
            contents_dict.clear()

    
    def write(self, key, value):        #put
        self.mem_table.setdefault(key, 0)
        self.mem_table[key] = value
        f = open('lsm.log', 'a')
        f.write(f'{key}:{value}\n')
        f.close()

    def read(self, key):                #get
        if key in self.mem_table:
            return self.mem_table.get(key)
        
    def delete(self, key):
        self.mem_table.setdefault(key, 0)
        self.mem_table[key] = 'del'
        f = open('lsm.log', 'a')
        f.write(f'{key}:del\n')
        f.close()


    def filename_generator(self) -> str:
        #creates a "unique" filename in a specified directory and returns it as a string
        #considering using date time + system time, should be unique enough
        pass


#when to write to disk? and should file size be limited to xxxx kb?
    def write_to_disk(self, sstable: dict, filename):
        ordered_keys = list(sorted(sstable))     #more efficient to sort with each insertion?
        if filename not in self.file_tree:
            self.file_tree.appendleft(filename)
        filename = self.tree_dir + self.file_tree[-1] + '.txt'
        new_file = open(filename, 'w')

        bookend_list = list(sstable.keys())
        first, last = bookend_list[0], bookend_list[-1] #could present difficulty-- does not follow key:value format of the file
        
        new_file.write(f'{first}, {last} \n')      #this writes a first and last key at the top of the file (might delete)
        
        for key in ordered_keys:
            new_file.write(f'{key}:{sstable.get(key)}\n')
        new_file.close()
        
        #trim the last \n from the .txt file
        new_file = open(filename, 'rb+')
        new_file.seek(-1, 2)
        new_file.truncate()
        new_file.close()
        
        #clear the log after writing to disk
        #think about moving this elsewhere after broadening use of write_to_disk()
        #log = open('lsm.log', 'w')
        #log.write('')
        #log.close()

        #WISHLIST: A meta file that provides line no. for data in files across the structure
        #to behave like a skip list for lookup

    def load_to_memory(self, filename):
        read_file = open(filename)
        file_contents = read_file.read()
        file_contents_dict = file_contents.split('\n')
        file_contents_dict = [items.split(':') for items in file_contents_dict]
        return dict(file_contents_dict)


#lay good groundwork...
#eventually the structure is too large to be confined to one file after compaction
#How to plan for this?
#Compaction is likely too big to fit all in memory, so a log of the process is necessary
#ANSWER:
#load first elements from each sorted file and compare across files, write lowest key:value to compacted file, pop, repeat

    def compaction(self):
        tombstone_set = set()
        duplicates = set()
        c_log = open('compaction_log.log')
        temp = open('temp_file')
        #first, let's clear out older entries, lower the number of comparisons 
        #the following code should go back in time, deleting repeated elements after most recent assignment
        dict_a = self.mem_table
        for files in self.file_tree:
            dict_b = self.load_to_memory(files)
            #first look for tombstones and pop
            for key, value in dict_a.items():
                if value == 'del':
                    tombstone_set.add(key)
            for key in tombstone_set:
                dict_a.pop(key)

            duplicates.add(set(dict_a).intersection(dict_b))    #creates a list of duplicate values as they are traversed
            for keys in duplicates:
                dict_b.pop(keys)
            self.write_to_disk(dict_b, files)
            dict_a = dict_b             #have to test, this may set dict_a as a pointer to dict_b

            #Immediate problem with this code as-written: only comparing adjacent files
            #this means that if file A and file C have elements in common, but not shared with file B
            #the redundant elements persist.

            #Now, across all log files, there should only be one of each key
        
        #let's load elements from file, 50 at a time
        #the following should generate a list of the first 50 lines from each file
        unsorted_tuples = []
        temp_tuples = []
        for files in self.file_tree:
            for x in range(50):
                temp = linecache.getline(files, x)
                temp = temp[:-1]
                temp_tuples.append(temp.split(':'))
            unsorted_tuples.append(temp_tuples)
            temp_tuples.clear()

        
        #Now we want to pull the first tuple from each list in the array and sort
        sorted_tuples = []
        for lists in unsorted_tuples:
            sorted_tuples.append(lists[0])
        
        sorted_tuples.sort()
        #pull the zero element from sorted_tuples, write to file, and pop the element from our unsorted tuples list

        #write to file
        (key, value) = sorted_tuples[0]
        with open(filename) as compaction:
            compaction.write(f'{key}:{value}\n')

        for i, tuples in unsorted_tuples:
            if tuples[0][0] == key:
                tuples.pop(0)


                




        
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

        




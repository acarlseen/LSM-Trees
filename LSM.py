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


'''Maybe it makes sense to build the mem-table as a linked list coupled with a sparse list
since this is a write-heavy data structure
Sparse list mitigates search cost for node insertion'''


class listNode:
    def __init__(self, data) -> None:
        self.data = data
        self.next = None

class LSMList:
    def __init__(self):
        self.head = None
        self.sparse_list = [] #sparse_list must always have the first and last node addresses
    
    def num_elements(self):
        result = 1
        itr = self.head
        while itr.next is not None:
            result += 1
            itr = itr.next
        return result

    def update_sparse_list(self, num_segments: int):
        #produces a class list of node addresses in the format [0, c, 2c, 3c,..., -1]
        #where c is the interval size, and the final interval is list_length % c in length.
        index = 0
        size = self.num_elements()
        self.sparse_list.clear()
        if size >= num_segments:
            segment_size = size//num_segments
        itr = self.head
        
        while itr.next is not None:
            #this loop as written, produces num_segments + remainder chunk. 
            if index % segment_size == 0: 
                self.sparse_list.append(itr)
            index += 1
            itr = itr.next
        if self.sparse_list[-1] != itr:
            self.sparse_list.append(itr)
        

    def search(self, key):  #return bool value and list node
        '''if FALSE, returned value is the "insert after me" node'''
        '''if TRUE, returned value is node containing data'''
        sparse_length = len(self.sparse_list)
        if sparse_length > 1:
            for _ in range(sparse_length-1):
                pass

    def insert(self):
        #method name makes sense, all new nodes are inserted in order
        #called when adding any new node
        #maybe called in order to add a new node after looking for an
        #exiting node!
        '''First narrow search by using sparse_list to find interval data belongs in
        then iterate using two pointers: itr_prev and itr_next
        
         When new_node.data belongs between itr_prev and itr_next
            itr_prev.next = new_node
            new_node.next = itr_next '''
        pass


    '''This could all be handled by a dictionary with a sort call before writing to disk.
    I don't think that a linked list as written can keep up with a hash table for write-heavy
    data structure. Fun to write, but not going to be the ultimate answer.
    #
    In the end, dictionaries are likely best for the memTable portion of this. O(1) lookup. But might
    still benefit from having an object assigned as the value in the pair?'''

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
        f.write(f'{key}:{value},')
        f.close()

    def read(self, key):                #get
        if key in self.mem_table:
            return self.mem_table.get(key)
        
    def delete(self, key):
        self.mem_table.setdefault(key, 0)
        self.mem_table[key] = 'del'


    def filename_generator(self) -> str:
        #creates a "unique" filename in a specified directory and returns it as a string
        #considering using date time + system time, should be unique enough
        pass


#when to write to disk? and should file size be limited to xxxx kb?
    def write_to_disk(self, sstable: dict, filename):
        ordered_keys = list(sorted(sstable))     #more efficient to sort with each insertion?
        if filename not in self.file_tree:
            self.file_tree.appendleft(filename)
        filename = self.tree_dir + self.file_tree[-1] + '.csv'
        new_file = open(filename, 'w')

        bookend_list = list(sstable.keys())
        first, last = bookend_list[0], bookend_list[-1] #could present difficulty-- does not follow key:value format of the file
        
        new_file.write(f'{first}, {last}, \n')      #this writes a first and last key at the top of the file (might delete)
        
        for key in ordered_keys:
            new_file.write(f'{key}:{sstable.get(key)},')
        new_file.close()
        
        #clear the log after writing to disk
        #think about moving this elsewhere after broadening use of write_to_disk()
        log = open('lsm.log', 'w')
        log.write('')
        log.close()

    def load_to_memory(self, filename):
        read_file = open(filename)
        file_contents = read_file.read()
        file_contents_dict = file_contents.split(',')
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





        


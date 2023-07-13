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
import test_generator


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

    def filename_generator(self) -> str:
        #creates a "unique" filename in a specified directory and returns it as a string
        #considering using date time + system time, should be unique enough
        pass

    def write_to_disk(self):
        #once mem_table is arbitrarily large enough, it is written to disk
        #comma delineated?
        self.mem_table = dict(sorted(self.mem_table))     #figure out if this is more efficient or sort with each insertion?
        self.file_tree.appendleft(self.filename_generator())
        filename = self.tree_dir + self.file_tree[-1] + '.csv'
        new_file = open(filename, 'xw')

        bookend_list = list(self.mem_table.keys())
        first, last = bookend_list[0], bookend_list[-1] #could present difficulty-- does not follow key:value format of the file
        
        new_file.write(f'{first}, {last}, \n')      #this writes a first and last key at the top of the file (might delete)
        new_file.write(self.mem_table)
        new_file.close()
        self.mem_table.clear()

    def search_LSM(self, key): #does this funcion return anything?
        if key in self.mem_table:
            print('found in mem table')
            return self.mem_table.get(key)
        else:
            print('not found in mem table, searching disk')
            for files in self.file_tree:
                current = open(files)
                contents_dict = current.read()
                contents_dict = contents_dict.split(',')
                contents_dict = [items.split(':') for items in contents_dict]
                if key in contents_dict:
                    print(f'key found in file {file}')
                    return contents_dict.get(key)
                contents_dict.clear()
        print('Key not found in LSM')
        return None
    
    def write(self, key, value):
        self.mem_table.setdefault(key, 0)
        self.mem_table[key] = value
        f = open('lsm.log')
        f.write(f'{key}:{value},')
        f.close()

    def read(self, key):
        if key in self.mem_table:
            return self.mem_table.get(key)





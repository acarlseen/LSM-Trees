'''
The purpose of this library is to use bits for boolean operations

An int in a list uses four bytes of space, represented below:
0000 0000   0000 0000   0000 0000   0000 0000
which can be used to store 32 boolean values

zero index from right to left 0-31
figure out bitwise operators...

build a dict for doing | operation
0: 1
1: 2
2: 4
3: 8
...esentially 2^(index)

When adding to the bloom filter, use 'or' operator to add a 1 in desired bit location
'''
import math

class bool_field():

    def __init__(self, size: int):
        self.size = size
        self.length = math.ceil(size/32)
        self.bool_array = [0]*self.length
    
    def insert(self, hash_val):
        array_index = math.floor(hash_val / 32)
        bit_index = hash_val % 32
        val_at_index = self.bool_array[array_index]
        self.bool_array[array_index] = val_at_index | 2**bit_index

    def get(self, hash_val):
        array_index = math.floor(hash_val / 32)
        bit_index = hash_val % 32
        try:
            bits = bin(self.bool_array[array_index])[2:]        #for some reason, these two lines cannot be combined
            bits = bits[::-1]                                   #slicing behaves strangely with [2::-1]
            return int(bits[bit_index])
        except IndexError:
            return False
    
    def print_field(self):
        '''bit_string = ''
        for element in self.bool_array:
            temp = str(bin(element))[2:]
            bit_string += temp[::-1]
        print(bit_string)'''
        bit_string = ''
        for element in self.bool_array:
            temp = str(bin(element))[2:]
            if len(temp) < 32:
                if len(bit_string) + 32 < self.size:
                    extension_length = 32 - len(temp)
                else:
                    extension_length = self.size - (len(temp) + len(bit_string))
                extension = ['0']*extension_length
                ext_str = ''
                temp = ext_str.join(extension) + temp
            bit_string += temp[::-1]
        print(bit_string)
        return(bit_string)
    
    def array_copy(self):
        bit_string = ''
        for element in self.bool_array:
            temp = str(bin(element))[2:]
            if len(temp) < 32:
                if len(bit_string) + 32 < self.size:
                    extension_length = 32 - len(temp)
                else:
                    extension_length = self.size - (len(temp) + len(bit_string))
                extension = ['0']*extension_length
                ext_str = ''
                temp = ext_str.join(extension) + temp
            bit_string += temp[::-1]
        str_list = [*bit_string]
        return list(map(int, str_list))


#---------------------------------------------------
#----------------Bool Field Testing-----------------
#---------------------------------------------------

if __name__ == '__main__':
    bf = bool_field(85)
    bf.print_field()
    bf.insert(31)
    bf.insert(80)
    bf.print_field()
    array = bf.array_copy()
    print(len(array))
    
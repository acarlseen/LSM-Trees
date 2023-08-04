import random
import json
import bool_field as bf

#Now I have a big question: What to do if we delete an element?
# hashing n%10 would yield 5 for 15, 25, 35, etc, so how do we update the filter?

word = 'hello'
word_value = hash(word)
print(word[:4])
print(random.random())

fractional_number = 1.346
whole_number = fractional_number//1
print(whole_number)

num = 12345
num_str = str(num)
print(num_str)
num_array = [*num_str]
print(f'num_array is {num_array}')

trim = 2
trimmed_num = int(str(num)[trim: -trim])
print(type(trimmed_num))


class BloomFilter():
    
    def __init__(self, size: int, hashes: int) -> None:
        self.hash_array_size = size     # number of bits in bloom filter
        self.hashes = hashes            # number of hashes per element
        self.bloom_array = bf.bool_field(size)
        self.hash_const = random.random()   # this will be for hash3


    #ideally, two layers of hashing lowers the occurence of collisions
    def get_hashes(self, key):
        hashes = (self.hash1(key), self.hash2(key), self.hash3(key), self.hash4(key))
        return hashes[:self.hashes]

    def hash1(self, key):    # build a mod hash function
        value = 0
        if type(key) == str:
            for char in key:
                value += ord(char)
        elif type(key) == int:
            value = key
        return value % self.hash_array_size
    
    def hash2(self, key):    # folding method using shift folding
        value = 0
        fold = key
        while len(key) >= 4:
            fold = key[0:4]
            value += self.fold(fold)
            key = key[4:]
        if key:
            value += self.fold(key)
        return value % self.hash_array_size
    
    def fold(self, key: str):
        section_val = ''
        for char in key:
            section_val += str(ord(char))
        return int(section_val)
            

    def hash3(self, key):    # build a mid-square hash function
        num_digits = len(str(self.hash_array_size))
        key = int(key)
        temp = key*key
        digit_diff = len(str(temp)) - num_digits
        if digit_diff <= 0:
            return temp
        elif digit_diff > 0:
            trim = digit_diff // 2
            if digit_diff % 2 == 0:
                return int(str(temp)[trim: -trim])
            else:
                return int(str(temp)[trim: -trim - 1])
    
    def hash4(self, key):   #build this when I find a good example of multiplication hash
        pass

    def search(self, key):
        hash_list = self.get_hashes(key)
        for h in hash_list:
            if self.bloom_array.get(h) == False:
                return False
        return True
            
    ''' h1 = self.hash1(key)
        if self.hashes == 2:
            h2 = self.hash2(key)
            if self.bloom_array.get(h2):
                return bool(self.bloom_array[h2])
        return bool(self.bloom_array[h1])'''

    def insert(self, key):
        hash_list = self.get_hashes(key)
        for h in hash_list:
            self.bloom_array.insert(h)
        '''h1 = self.hash1(key)
        self.bloom_array.insert(h1)
        if self.hashes == 2:
            h2 = self.hash2(key)
            self.bloom_array.insert(h2)'''


    
#----------------------------------------------------
#--------------Testing Bloom Filter------------------
#----------------------------------------------------

test_list = [random.randint(0, 15) for x in range(5)]
print(test_list)

with open('scratch_test', 'r') as f:
    test_data = json.load(f)

bloom = BloomFilter(100, 2)
for num in test_data.keys():
    bloom.insert(num)
    print(bloom.hash2(num))

print(test_data)
print(bloom.bloom_array)

print(bloom.bloom_array.print_field())

look_for = str(random.randint(0,50))
if bloom.search(look_for):
    print(f'{look_for} might be present')
else:
    print(f'{look_for} is not present')



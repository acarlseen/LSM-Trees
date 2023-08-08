import bool_field as bf
import basic_bloom_filter as f
import random

def command_generator(this_many):
    return [(random.randint(0,1), str(random.randint(0,1000))) for x in range(this_many)]

def array_test(command_list):
    test_bloom = [0]*96
    bloom = f.BloomFilter(96, 2)
    for tup in command_list:
        (command, key) = tup
        
        if test_bloom != bloom.bloom_array.array_copy():    #test parity with each pass
            print('Arrays not equal')
            return
        
        if command == 0:                                    #apply commands
            bloom.insert(key)
            index = bloom.get_hashes(key)
            for i in index:
                test_bloom[i] = 1
        
        elif command == 1:
            chars = [str(x) for x in test_bloom]
            string = ''.join(chars)
            print(string)
            bloom.bloom_array.print_field()
            index = bloom.get_hashes(key)
            exist = True
            for i in index:
                if test_bloom[i] == False:
                    exist = False
                    print(f'{key} not present in test_bloom')
                    break
            if exist == True:
                print(f'{key} might be present in test_bloom')
            if bloom.search(key) == 1:
                print(f'{key} might be present')
            else:
                print(f'{key} not present')
    bloom.bloom_array.print_field()
    print(len(bloom.bloom_array.print_field()))


if __name__ == '__main__':
    commands = command_generator(300)
    array_test(commands)
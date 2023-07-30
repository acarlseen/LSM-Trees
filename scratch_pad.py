import random
import linecache
import json

'''new_dict = {x:x**2 for x in range(100)}
print(new_dict)
#dict_as_string = str(new_dict)
#print(dict_as_string)
new_file = open("newfile.csv", 'w')
temp = ''
for key, value in new_dict.items():
    temp+= f'{key}:{value},'
new_file.write(temp[:-1])
new_file.close()


#convert back to dictionary
read_file = open('newfile.csv')
file_contents = read_file.read()
file_contents_list = file_contents.split(',')
file_contents_list = [items.split(':') for items in file_contents_list]
print(file_contents_list)
file_contents_list = dict(file_contents_list)
#everything is still a string. Any memory efficient way to typecast this?
print(file_contents_list)
#or is it even necessary? Maybe only need to do on-demand, not for whole dictionary since
#it is write heavy, not read heavy
#maybe more efficient to typecast the search param as str()

read_file.close()'''

#import csv #seems to be the answer

my_dict = {'test': None}
print(my_dict)

# generate a command list
# apply that command list to both LSM object and tester in <test_generator>
# compare results


import LSM
import test_gen

#generate a command list
command_list = test_gen.command_generator(50)
print(command_list)
#SUCCESS! (wonder if I can change test_generator.py to test.py)

test_dict = {}
test_dict = test_gen.dict_test(test_dict, command_list)
print(f'dict is: {test_dict}')

test_tree = LSM.LSMTree('')
for tups in command_list:
    (command, key, value) = tups
    if command == 0:
        test_tree.mem_table.setdefault(key, 0)
 #       if test_tree.mem_table.get(key) == None:
 #           test_tree.mem_table[key] = 0
        test_tree.write(key, value)
    elif command == 1:
        test_tree.delete(key)
    else:
        test_tree.read(key)

pop_list = []
for key, val in test_tree.mem_table.items():
    if test_tree.mem_table.get(key) == 'del':
        pop_list.append(key)

for key in pop_list:
    test_tree.mem_table.pop(key)

print(f'tree is {test_tree.mem_table}')

if test_dict == test_tree.mem_table:
    print('HECKA SUCCESSFUL')


old_dict = {1:200, 2:34, 23:67, 67:3040, 123: 239, 14: 293, 7: 934}

tuples = list(old_dict.items())
print(tuples)

number = 3040
if number in tuples[3]:
    print(f'Yup. {number} is here.')


with open('somefile.txt') as f:
    for lines in f:
        print(lines)

# Testing sorting and popping

N = 5
R = 10
key = 5

list_of_tuples = [ [divmod(ele, R + 1) for ele in random.sample(range((R + 1) * (R + 1)), N)] for x in range(10)]

list_of_tuples[1].pop(0)

for i, tuples in enumerate(list_of_tuples):
    print(tuples)

print('-----------------')

for i, tuples in enumerate(list_of_tuples):
    if tuples[0][0] == key:
        if len(tuples) == 1:
            #go back to log file and grab 50 more key:value pairs
            for x in range(50):
                temp = linecache.getline(test_tree.file_tree[i], x)     #list_of_tuples should mirror file_tree indexes
                temp = temp[:-1]                                        #shave off escape char
                temp = temp.split(':')                                  #split into tuple
                tuples.append(temp)                                     #append to list of tuples before....
        tuples.pop(0)                                                   #always popping the matching tuple at index 0
    print(tuples)



print(test_tree.filename_generator())


var_a = 1
var_b = '2'

if type(var_a) != type(var_b):
    print('types do not match')





with open("scratch_test", 'w') as j:
    json.dump(old_dict, j, sort_keys=True)

with open("scratch_test", 'r') as j:
    file_data = json.load(j)
print(file_data)
print(file_data.get('23'))

with open('scratch_test', 'r') as f:
    file_data = json.load(f)
    print(file_data)
file_data.pop('7')

with open('scratch_test', 'w') as f:
    json.dump(file_data, f)


print(str(f))


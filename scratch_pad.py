
new_dict = {x:x**2 for x in range(100)}
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

read_file.close()

#import csv #seems to be the answer

my_dict = {'test': None}
print(my_dict)

# generate a command list
# apply that command list to both LSM object and tester in <test_generator>
# compare results


import LSM
import test

#generate a command list
command_list = test.command_generator(50)
print(command_list)
#SUCCESS! (wonder if I can change test_generator.py to test.py)

test_dict = {}
test_dict = test.dict_test(test_dict, command_list)
print(f'dict is: {test_dict}')

test_tree = LSM.LSMTree('')
for tups in command_list:
    (command, key) = tups
    if command == 0:
        test_tree.mem_table.setdefault(key, 0)
        if test_tree.mem_table.get(key) == 'del':
            test_tree.mem_table[key] = 0
        test_tree.write(key, test_tree.mem_table.get(key) + 1)
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


old_dict = {1:200, 2:34, 23:67, 67:3040, 123: 239}

tuples = list(old_dict.items())
print(tuples)

number = 3040
if number in tuples[3]:
    print(f'Yup. {number} is here.')







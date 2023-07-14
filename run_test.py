import LSM
import test

#generate a command list
command_list = test.command_generator(500)      #change this integer value to run desired number of tests




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
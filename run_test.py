import LSM
import test_gen

#generate a command list
command_list = test_gen.command_generator(500)      #change this integer value to run desired number of tests

#run the command list on a dictionary
test_dict = {}
test_dict = test_gen.dict_test(test_dict, command_list)

#run the commmand list on LSM implimentation
#LSM.py handles deletion differently due to eventual compaction
#instead it assigns a tombstone value, so there is some additional code.
test_tree = LSM.LSMTree('')
for tups in command_list:
    (command, key, value) = tups
    if command == 0:
        test_tree.write(key, value)
    elif command == 1:
        test_tree.delete(key)
    elif command == 2:
        print(test_tree.read(key))
    elif command == 3:
        test_tree.flush_mem_table(test_tree.mem_table, test_tree.filename_generator())
    elif command == 4:
        pass
        # test_tree.recover_from_log()

pop_list = [key for key, val in test_tree.mem_table.items() if val == None]

for key in pop_list:
    test_tree.mem_table.pop(key)

print(f'dict is: {test_dict}')
print(f'tree is {test_tree.mem_table}')

test_tree.flush_mem_table(test_tree.mem_table, 'somefile')

if test_dict == test_tree.mem_table:
    print('HECKA SUCCESSFUL')

test_tree.mem_table.clear()
test_tree.recover_from_log()
print(test_tree.mem_table)
if test_dict == test_tree.mem_table:
    print('HECKA SUCCESSFUL')
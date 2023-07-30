'''Build a general test generator to test against a tried and true data structure'''
import random

def command_generator(n: int):
    #if a the test does not need to be retained, this doesn't have to be a list.
    #instead could be replaced by a loop with a call to test_generator returning 
    #two integers: rand(command), rand(key)

    return [(random.randint(0,100)%5, random.randint(0,5), random.randint(0, 10_000)) for _ in range(n)]
'''
0 = write
1 = delete
2 = search/find/whatever
3 = write to disk
4 = re-build from WAL
'''




def dict_test(LSM_dict: dict, command_list: list): 
    for data in command_list:
        (instr, key, value) = data
        key = str(key)
        if instr == 0:
            #put
            LSM_dict[key] = value
        elif instr == 1:
            #delete
            if key in LSM_dict.keys():
                LSM_dict.pop(key)
                print(f'{key} deleted')
            else:
                print("cannot delete, key does not exist")
        elif instr == 2:
            #get
            if key in LSM_dict.keys():
                print(LSM_dict[key])
            else:
                print("Key does not exist")
        elif instr == 3:
            pass
        elif instr == 4:
            pass
    #print(LSM_dict)
    return LSM_dict



'''I would suggest that the next step is to have the dict_test be broken up into two functions: 
    one that executes the commands against a dict and returns the results, 
    one that asserts two applications of the commands give the same results
'''
# re-write to test equivalncy of commands PER COMMAND
# I have a high level of confidence this works fine throughout,
# however(!) the current implementation only tests the end 
# result of manipulating the structure.
#
# I have high confidence because consistently arrriving at the same
# end through incongruent means is highly improbable

#UPDATE: many_tests() now checks each step and breaks the loop if equivalency is not achieved
# still prints "Successful test simulation" after running all tests if there are no errors

def many_tests(num_commands: int, num_tests: int):
    tups = []
    for _ in range(num_tests):
        command_list = command_generator(num_commands)

        dict_a = {}
        dict_b = {}
        while command_list:
            tups.append(command_list.pop(0))
            result_a = dict_test(dict_a, tups)
            result_b = dict_test(dict_b, tups)

            if result_a != result_b:
                print("Command list not uniformly applied")
                return False
            tups.clear()
    print("Successful test simulation")
    return True


if __name__ == '__main__':
    many_tests(15, 200)


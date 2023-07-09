'''Build a general test generator to test against a tried and true data structure'''
import random

def test_generator(n: int):
    #if a the test does not need to be retained, this doesn't have to be a list.
    #instead could be replaced by a loop with a call to test_generator returning 
    #two integers: rand(command), rand(key)
    '''test_list = []
    
    for _ in range(n):
        test_list.append((random.randint(0, 100) % 3 , random.randint(0, 5)))'''


    #test_list = 
    return [(random.randint(0,100)%3, random.randint(0,5)) for _ in range(n)]

    #print(test_list)
    #return (test_list)


def dict_test(LSM_dict: dict, command_list: list): 
    for data in command_list:
        (instr, key) = data
        if instr == 0:
            #put
            LSM_dict[key] = LSM_dict.setdefault(key, 0) + 1
        elif instr == 1:
            #delete
            if key in LSM_dict.keys():
                LSM_dict.pop(key)
                print(f'{key} deleted')
            else:
                print("cannot delete, key does not exist")
        else:
            #get
            if key in LSM_dict.keys():
                print(LSM_dict[key])
            else:
                print("Key does not exist")
    print(LSM_dict)
    return LSM_dict



'''I would suggest that the next step is to have the dict_test be broken up into two functions: 
    one that executes the commands against a dict and returns the results, 
    one that asserts two applications of the commands give the same results
'''

def many_tests(num_commands: int, num_tests: int):
    for _ in range(num_tests):
        command_list = test_generator(num_commands)

        dict_a = {}
        dict_b = {}

        result_a = dict_test(dict_a, command_list)
        result_b = dict_test(dict_b, command_list)

        if result_a != result_b:
            print("Command list not uniformly applied")
            return False
    print("Successful test simulation")
    return True
    
many_tests(15, 200)
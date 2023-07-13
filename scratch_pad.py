
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

import csv #seems to be the answer



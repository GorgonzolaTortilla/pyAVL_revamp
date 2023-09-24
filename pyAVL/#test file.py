#test file, for all your testing needs
import numpy as np
import re
# I am currently resisting the urge to name my functions "vibe check"
# or "cock check". I'm seriously trying to make all of this readable by
# other people, which is why all the variables aren't named some variation
# of "bullshit123". 


### Prints CLtot and CDtot from total forces file ###
# strings = np.array(open('Output/Total Forces').readlines())
# for i,line in enumerate(strings):
#     if 'CLtot' in line:
#         print(line.split()[0])
#     elif 'CDtot' in line:
#         print(line.split()[0])

# import numpy as np
# a = np.array([17,18,4,3,2,1])
# b = np.argsort(a)
# print(b)
# print(a[b])
# print(*a)

# with open('Models/Planes/a/a.avl') as f:
#     string = f.read()
#     new_values = [2,3,7,8]
#     string = re.sub('\{.*?\}','{{{}}}',string)
#     string = string.format(*new_values)
#     print(string)

# with open('Models/Planes/a/a.avl','w') as f:
#     f.write(string)

# array = ['a','b','c','d','e']
# print(array.pop(0))
# print(array)

# x = 0
# bool = False
# x = 1
# if x == 0:
#     print('x is 0')
# elif bool == False:
#     print('bool is false')

# from Scripts.parsing_scripts import *
# plane_name = 'a'
# avl = 1

# str = '1.0'
# float = float(str)
# print(float)

# dict = {}
# dict['store'] = 5
# print(dict) 

# strings = (open('Output/Total Forces').readlines())
# # for i,line in enumerate(strings):
# #     if 'CLtot' in line:
# #         print(line.split()[0])
# #     elif 'CDtot' in line:
# #         print(line.split()[0])
# print(strings[7].split('|')[0].split().__len__())

# from Scripts.parsing_scripts import locate_in_output
# print(locate_in_output(output_file='Total Forces', value = 'Sref'))
# post_run_flags = {}
# post_run_flags['store'] = ['Total Forces','Alpha']
# print(post_run_flags)
# for flag in post_run_flags:
#     print(flag)
#     print(post_run_flags[flag])

# for i in range(2):
#     print(i)
import numpy as np

# a = np.array([2,3])
# b = np.array([5,6])
# print(b-a)

start_values = [0,1]
end_values = [10,2]
N = 10
start_values = np.array(float(start_values))
end_values = (np.array(end_values))
step = (end_values - start_values)/(N-1)
new_values = start_values
new_values += step
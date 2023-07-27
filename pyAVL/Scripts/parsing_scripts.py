# Function bag - parsing scripts
# 
# Current Contents:
#       1. geometry_file_to_string()
#       2. surface_split_indices()
#       3. locate_in_avl()  <--- ** W I P **
#       4. parse() <--- ** W I P **
#
# Future Contents:
#       Something to locate a parameter in an avl file and place
#       brackets around it (mark for optimization). Will require a file,
#       surface + parameter (or surface + section + parameter) 
#
#       the parse() function
#
# Function Descriptions:
#       1. geometry_file_to_string()
#               Takes path to file "Generator\Geometry" (no file type) as an argument.
#               Returns a formatted array of subarrays. The subarrays contain organized 
#               surface information for use in "Generator.py". The "Generator\Geometry"
#               file is copy/pasted from the "Weight Iteration" spreadsheet, on the 
#               "Weight Iteration" sheet (first sheet) in the "AVL Geometry" section.
#               The format is not strictly enforced, but try copy/paste the spreadsheet
#               information to avoid errors.
#                   -Used in: "Generator.py"
#
#       2. surface_split_indices()
#               Takes the formatted array from "geometry_file_to_string()" and locates 
#               the indices of the surface keywords from "Scripts\keys surf_keywords".
#               Returns the indices where the surface keywords are found and removes
#               surface names from subarrays, placing them in the formatted array.
#                   -Used in: "Generator.py"
#
#       3. locate_in_avl()
#               Takes a ".avl" file, surface, section (optional) and parameter and marks
#               the specified parameter for optimization or sweeping. This is shown in the
#               ".avl" file by the curly brackets, "{}", around a parameter. 
#
#       
import numpy as np

def geometry_file_to_string(filename = None):
    try:
        string = open(filename,'r').read()
    except:
        if filename is None: 
            print('No file specified')
        else:
            print(f'Error in "geometry_file_to_string": File "{filename}" not found.')
    string = string.lower().split('\n')
    formatted_string = []
    for str in string:
        if str.split() == []:
            continue
        else:
            formatted_string.append(str.split())
    return formatted_string

def surface_split_indices(formatted_string):
    index = []
    from Scripts.keys import surf_keywords
    for row in formatted_string:
        for x in row:
            if x in surf_keywords:
                i = formatted_string.index(row)
                index.append(i)
                formatted_string[i] = x
                break
    index.append(len(formatted_string))
    return index

def locate_in_avl(avl_file = None, surface_name = None, section = None, parameter = ''):
    contents = open(f'{avl_file}').readlines()

    pass

def parse():
    pass



    
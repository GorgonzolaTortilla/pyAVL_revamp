# Function bag - parsing scripts
# 
# Current Contents:
#       1. geometry_file_to_string()
#       2. surface_split_indices()
#       3. mark_in_avl()
#       4. locate_in_line()
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
#               The format is not strictly enforced, but try to copy/paste the spreadsheet
#               information to avoid errors.
#                   -Used in: "Generator.py - generate_avl()"
#
#       2. surface_split_indices()
#               Takes the formatted array from "geometry_file_to_string()" and locates 
#               the indices of the surface keywords from "Scripts\keys surf_keywords".
#               Returns the indices where the surface keywords are found and removes
#               surface names from subarrays, placing them in the formatted array.
#                   -Used in: "Generator.py - generate_avl()"
#
#       3. mark_in_avl()
#               Takes a ".avl" file, surface, section number (optional) and parameter and marks
#               the specified parameter for optimization or sweeping. This is shown in the
#               ".avl" file by the curly brackets, "{}", around a parameter.
#                   -Used in: NOTHIN 🔥
#
#       4. locate_in_line()
#               Takes a line from a ".avl" file containing the "#" delimiter (e.g., "0.0 # ANGLE") 
#               and a keyword to search for ("ANGLE"). Returns the index of the number (left-side of "#")
#               that corresponds to the keyword (right-side of "#"").
#                   -Used in: "parsing_scripts.py - mark_in_avl()"

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

def mark_in_avl(plane_name = None, surface_name = None, section_number = None, parameter = '', mute = False):
    ## Programming Note: RE can probably improve this in some places ##
    #Import surface keywords for validation and searching
    from Scripts.keys import surf_keywords
    surface_name = surface_name.lower()
    if surface_name not in surf_keywords:
        print(f'Error in "locate_in_avl": Value "surface_name" not valid surface keyword (Given value: {surface_name}). Skipping step.\n'\
              f'Valid surface_keywords are {surf_keywords}')
        return None
    #Split the .avl file into individual lines
    avl_contents = (open(f'Models/Planes/{plane_name}/{plane_name}.avl').readlines())
    #Delete excess blank spaces and newline characters, put into lowercase for matching purposes
    formatted_contents = [x.strip().lower() for x in avl_contents]
    #Get indices where surface keywords are located
    surface_indices = [i for i,line in enumerate(formatted_contents) if line in surf_keywords]
    #Find the index where our desired surface_name is mentioned
    index = [i for i,surf_ind in enumerate(surface_indices) if formatted_contents[surf_ind] == surface_name][0]
    #Append maximum length as an index to avoid indexing errors
    surface_indices.append(len(avl_contents))
    #Check section_number's type and go through corresponding process
    #No section number - mark first occurance, none-found behavior: state that none was found (return id 0)
    #Int section number - mark in specific section, none-found @ section no. behavior: return error (return id 10)
    #Invalid section number - not accepted (return code 20)
    if section_number is None:
        #Track whether is match is found
        found_match = False
        for i in range(surface_indices[index],surface_indices[index+1]):
            #Check if the parameter is in the line and if a "#" is present
            #(The "#" are always on the same line as the parameter value, courtesy of generate_avl())
            if (parameter in formatted_contents[i].split()) & ('#' in formatted_contents[i]):
                #Note that match was found
                found_match = True
                #Note line where we find parameter
                index_in_avl = i
                #Extract line
                line_with_parameter = avl_contents[i]
                #Find parameter location within line
                index_in_line = locate_in_line(line = line_with_parameter, search_word = parameter)
                break
        if found_match == False:
            if mute == False:
                print(f'Parameter "{parameter}" not found in surface "{surface_name}". Please double-check the parameter name (return code 0).')
            return 0
    elif type(section_number) is int:
        #Track section no. and whether match is found
        sections_encountered = 0
        found_match = False
        for i in range(surface_indices[index],surface_indices[index+1]):
            #Check if the parameter is in the line and if a "#" is present
            #(The "#" are always on the same line as the parameter value, courtesy of generate_avl())
            if (parameter in formatted_contents[i].split()) & ('#' in formatted_contents[i]):
                #If section_number given, match section                                                                                                                     
                sections_encountered +=1
                if sections_encountered == section_number:
                    #Note that match was found
                    found_match = True
                    #Note line where we find parameter
                    index_in_avl = i
                    #Extract line
                    line_with_parameter = avl_contents[i]
                    #Find parameter location within line
                    index_in_line = locate_in_line(line = line_with_parameter, search_word = parameter)
                    break
        if sections_encountered == 0:
            if mute == False:
                print(f'Parameter "{parameter}" not found in surface "{surface_name}". Please double-check the parameter name (return code 0).')
            return 0
        elif found_match == False:
            if mute == False:
                print(f'Parameter "{parameter}" not found at section {section_number}; assuming section does not exist (return code 10).')
            return 10
    else:
        if mute == False: 
            print(f'Section number "{section_number}" (type: "{type(section_number)}") not valid. Please leave blank or provide an integer (return code 20).')
        return 20
    #Once you find the line with the parameter, split line to extract parameter value
    split_line = line_with_parameter.split(' ')
    variable = split_line[index_in_line]
    #Check if already marked
    if '{' in variable:
        print(f'Line "{" ".join(split_line).strip()}" already contains a marked parameter "{parameter}". Skipping step.')
        return None
    #Place {} around parameter value
    split_line[index_in_line] = f'{{{variable}}}'
    #Rejoin line, insert into avl_contents, and write to .avl
    marked_parameter = ' '.join(split_line)
    with open(f'Models/Planes/{plane_name}/{plane_name}.avl','w') as f:
        avl_contents[index_in_avl] = marked_parameter
        for str in avl_contents:
            f.write(str)
    #Print result
    print(f'Marked parameter "{parameter}" in surface {surface_name}, section {section_number}: "{marked_parameter.strip()}"')

def locate_in_line(line = None, search_word = None):
    search_word = search_word.lower()
    line = line.lower().strip().split('#')
    words = line[1].strip().split()
    return words.index(search_word)

def locate_in_avl(plane_name = None, surface_name = None, section_number = None, parameter = '', mute = False):
    #Returns [value, line no., in-line index]
    #Spliced from mark_in_avl()
    #Import surface keywords for validation and searching
    from Scripts.keys import surf_keywords
    surface_name = surface_name.lower()
    if surface_name not in surf_keywords:
        print(f'Error in "locate_in_avl": Value "surface_name" not valid surface keyword (Given value: {surface_name}). Skipping step.\n'\
              f'Valid surface_keywords are {surf_keywords}')
        return None
    #Standard operating procedure: use readlines(), strip(), and lower()
    avl_contents = (open(f'Models/Planes/{plane_name}/{plane_name}.avl').readlines())
    formatted_contents = [x.strip().lower() for x in avl_contents]
    #Get indices where surface keywords are located
    surface_indices = [i for i,line in enumerate(formatted_contents) if line in surf_keywords]
    #Find the index where our desired surface_name is mentioned
    index = [i for i,surf_ind in enumerate(surface_indices) if formatted_contents[surf_ind] == surface_name][0]
    #Append maximum length as an index to avoid indexing errors
    surface_indices.append(len(avl_contents))
    #Check section_number's type and go through corresponding process
    #No section number - mark first occurance, none-found behavior: state that none was found (return id 0)
    #Int section number - mark in specific section, none-found @ section no. behavior: return error (return id 10)
    #Invalid section number - not accepted (return code 20)
    if section_number is None:
        #Track whether is match is found
        found_match = False
        for i in range(surface_indices[index],surface_indices[index+1]):
            #Check if the parameter is in the line and if a "#" is present
            #(The "#" are always on the same line as the parameter value, courtesy of generate_avl())
            if (parameter in formatted_contents[i].split()) & ('#' in formatted_contents[i]):
                #Note that match was found
                found_match = True
                #Note line where we find parameter
                index_in_avl = i
                #Extract line
                line_with_parameter = avl_contents[i]
                #Find parameter location within line
                index_in_line = locate_in_line(line = line_with_parameter, search_word = parameter)
                break
        if found_match == False:
            if mute == False:
                print(f'Parameter "{parameter}" not found in surface "{surface_name}". Please double-check the parameter name (return code 0).')
            return 0
    elif type(section_number) is int:
        #Track section no. and whether match is found
        sections_encountered = 0
        found_match = False
        for i in range(surface_indices[index],surface_indices[index+1]):
            #Check if the parameter is in the line and if a "#" is present
            #(The "#" are always on the same line as the parameter value, courtesy of generate_avl())
            if (parameter in formatted_contents[i].split()) & ('#' in formatted_contents[i]):
                #If section_number given, match section                                                                                                                     
                sections_encountered +=1
                if sections_encountered == section_number:
                    #Note that match was found
                    found_match = True
                    #Note line where we find parameter
                    index_in_avl = i
                    #Extract line
                    line_with_parameter = avl_contents[i]
                    #Find parameter location within line
                    index_in_line = locate_in_line(line = line_with_parameter, search_word = parameter)
                    break
        if sections_encountered == 0:
            if mute == False:
                print(f'Parameter "{parameter}" not found in surface "{surface_name}". Please double-check the parameter name (return code 0).')
            return 0
        elif found_match == False:
            if mute == False:
                print(f'Parameter "{parameter}" not found at section {section_number}; assuming section does not exist (return code 10).')
            return 10
    else: 
        if mute == False:
            print(f'Section number "{section_number}" (type: "{type(section_number)}") not valid. Please leave blank or provide an integer (return code 20).')
        return 20
    #Once you find the line with the parameter, split line to extract parameter value
    split_line = line_with_parameter.split(' ')
    variable = split_line[index_in_line]
    #Return value, index of line, and in-line index of value
    return [variable, index_in_avl, index_in_line]

def locate_in_output(output_file = None, value = None):
    #Takes: an output file name and value from the output file
    #Returns: the requested value
    #Does not handle errors (yet?)
    output_contents = open(f'Output/{output_file}','r').readlines()
    for i,line in enumerate(output_contents):
        if value in line:
            #Don't even bother
            split_line = line.split('|')
            count = split_line[0].split().__len__()
            keywords = split_line[1].split()[-count:-1]
            keywords.append(split_line[1].split()[-1])
            keywords = [word.replace(',','') for word in keywords]
            index_in_line = keywords.index(value)
            return split_line[0].split()[index_in_line]
        
def fix_my_fucking_airfoils_bruh():
    pass

    
    
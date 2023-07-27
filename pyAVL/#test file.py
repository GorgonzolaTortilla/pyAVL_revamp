#test file
import numpy as np

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

### Locates (and marks?) parameters in avl file ###
def locate_in_avl(plane_name = None, surface_name = None, section = None, parameter = ''):
    try:
        surface_name = surface_name.lower()
    except AttributeError:
        print('hit the mfin griddy bruh 💀💀💀💀💀')
    avl_contents = (open(f'Models/Planes/{plane_name}/{plane_name}.avl').readlines())
    formatted_contents = [x.strip().lower() for x in avl_contents]
    from Scripts.keys import surf_keywords
    surface_indices = [i for i,line in enumerate(formatted_contents) if line in surf_keywords]
    try:
        index = [i for i,surf_ind in enumerate(surface_indices) if formatted_contents[surf_ind] == surface_name][0]
    except IndexError:
        print('hell nah bruh you used the wrong surface name 😭')
        return None
    except:
        print('some random bullshit happened idk tell an aero person')
    surface_indices.append(len(avl_contents))

    # Search for the parameter
    for i in range(surface_indices[index],surface_indices[index+1]):
        if (parameter in formatted_contents[i]) & ('#' in formatted_contents[i]):
            found_parameter = avl_contents[i].split(' ')
            found_at_index = i
            for i in range(len(found_parameter)):
                pass
            print('found it')

    # Once you find it
    print(found_parameter)
    found_parameter[0] = f'{{{found_parameter[0]}}}'
    marked_parameter = ' '.join(found_parameter)
    print(marked_parameter)
    with open(f'Models/Planes/{plane_name}/{plane_name}.avl','w') as f:
        avl_contents[found_at_index] = marked_parameter
        print(avl_contents)
        for str in avl_contents:
            f.write(str)
    print('end')

    
    pass

locate_in_avl(plane_name = 'a', surface_name = 'wing', parameter = 'angle')


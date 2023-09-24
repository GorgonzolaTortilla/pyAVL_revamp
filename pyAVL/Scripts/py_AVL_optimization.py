from py_AVL import AVL
from Scripts.parsing_scripts import locate_in_avl
import re
import numpy as np

class AVL_optimization(AVL):
    def __init__(self):
        super().__init__()

    def initialize_template(self):
        try:
            avl_contents = open(f'Models/Planes/{self.plane_name}/{self.plane_name}.avl').read()
        except AttributeError:
            print('ERROR: Please load a plane using "load_plane()" before creating template.')
        except FileNotFoundError:
            print(f'ERROR: File "Models/Planes/{self.plane_name}/{self.plane_name}.avl" does not exist. '+\
                  r'If you see this error message, tell an aero lead, cause something went wrong with py_AVL lmfao')
                    #If you see ⬆ this ⬆ message, the plane properly loaded in AVL but either self.plane_name didn't assign
                    #properly or just failed to open using this function. This shouldn't happen but it's here for debugging.
        self.template = re.sub('\{.*?\}','{}',avl_contents)

    def update_reference(self, surface):
        #What i need:
        #all yle
        #all chord
        #that's it?? seems shrimple
        yle = []
        chord = []
        section_number = 0
        while(True):
            section_number += 1
            try:
                value = float(locate_in_avl(plane_name = self.plane_name, surface_name = surface, section_number = section_number, parameter = 'yle', mute = True)[0])
                yle.append(value)
                value = float(locate_in_avl(plane_name = self.plane_name, surface_name = surface, section_number = section_number, parameter = 'chord', mute = True)[0])
                chord.append(value)
            except TypeError:
                #This occurs when locate_in_avl() returns an error code, typically to exit the while loop when no more sections are encountered.
                break
            except:
                print(f'Unknown error in "update_references": failed to assign value "{value}". See "update_reference()" function for details.')
                #This means that locate_in_avl() returned something other than the expected array or integer error code.
                #I don't think that's possible, but worth having the exception.
            sref = 0
            cref = 0
            bref = 2*yle[-1]
            for i in range(len(yle)-1):
                sref += (yle[i+1]-yle[i])*(chord[i]+chord[i+1])
            for i in range(len(yle)-1):
                y1 = yle[i]
                c1 = chord[i]
                dy = yle[i+1] - y1
                taper = chord[i+1]/c1
                m = (taper - 1)/dy
                cref += 2/sref*( c1**2*( m**2/3*dy**3 + (m - y1*m**2)*dy**2 + (1 - y1*m)**2*dy) )
        print(f'done updating refs: Cref = {cref}, Sref = {sref}, Bref = {bref}')

    def update_variables(self,new_values):
        new_contents = self.template.format(*new_values)
        with open(f'Models/Planes/{self.plane_name}/{self.plane_name}.avl','w') as f:
            f.write(new_contents)

    def parameter_sweep(self, start_values = None, end_values = None, N = None):
        #Takes:     start_values is an array containing the starting values for all marked parameters: [param_1, param_2,... param_n]
        #           end_values is an array containing the ending values for all marked parameters: [param_1, param_2,... param_n]    
        #           N is an integer for total number of values tested.
        #Returns:   NOTHIN 🔥🔥🔥🔥 jk it stores an indicated value in the self.store for scrutiny 🤓
        start_values = np.array(list(map(float,start_values)))
        end_values = np.array(list(map(float,end_values)))
        step = (end_values - start_values)/(N-1)
        new_values = start_values
        temp_list = self.input_list
        self.clear()
        for i in range(N):
            print(new_values)
            self.update_variables(new_values)
            self.update_reference(surface = 'wing')
            self.load_plane(self.plane_name)
            self.trim()
            self.run_avl(postrun = True)
            new_values += step
        self.input_list = temp_list
        
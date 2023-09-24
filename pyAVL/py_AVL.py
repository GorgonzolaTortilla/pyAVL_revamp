from ambiance import Atmosphere
import os
import sys
import re
import subprocess
import time
import numpy as np
import re
from Scripts.parsing_scripts import locate_in_output

def IsItWindows():
    """Return true if os is windows"""
    return True if os.name == 'nt' else False

class AVL:
    ### Standard variables ###
    input_list = ''
    post_run_flags = {}
    ### Some initialization stuff. ###
    def __init__(self):
        self.post_run_flags = {}
        self.store = []
        self.clear()
        self.cd = os.getcwd()
        self.win = IsItWindows()
        if self.win:
            self.avlpath = f'{self.cd}/avl.exe'
        else:
            self.avlpath = f'{self.cd}/avl3.35'

    ### Basic commands; you can do anything(?) with these. ###
    def input(self,input):
        self.input_list += f'{input}\n'

    def clear(self):
        self.input_list = ''

    def top(self):
        self.input('\n\n\n\n\n')

    def oper(self):
        self.top()
        self.input('oper')

    ### The panic button. ###
    def abort(self, error_message = 'UNSPECIFIED'):
        self.clear()
        self.input('quit')
        print(f'ERROR: Aborting RUN due to error: {error_message}.')
        quit()

    ### Commands for loading files and modifying parameters. ###
    def load_plane(self, plane): #Base
        try: open(f'Models/Planes/{plane}/{plane}.avl')
        except FileNotFoundError: 
            print(f'ERROR: File "Models/Planes/{plane}/{plane}.avl" does not exist.') 
            self.abort('there\'s no plane 💀')
        except:
            print('ERROR: Unknown error while loading plane. Please contact your nearest aero lead.')   
        self.input(f'load Models/Planes/{plane}/{plane}.avl')
        self.plane_name = plane

    def load_mass(self,plane): #Base
        try: open(f'Models/Planes/{plane}/{plane}.mass')
        except FileNotFoundError: 
            print(f'ERROR: File "Models/Planes/{plane}/{plane}.mass" does not exist.') 
            self.abort('mass brokey')
        except:
            print('ERROR: Unknown error while loading mass. Please contact your nearest aero lead.')  
        self.input(f'mass Models/Planes/{plane}/{plane}.mass')
        self.input('mset\n0')

    def atmosphere(self, altitude = 0, temp_offset = 0):
        # convert to imperial units
        altitude = altitude/3.28084 # ft to m
        temp_offset = 5/9*temp_offset # F to C
        self.oper()
        self.input('M')
        self.input('G 32.17')
        atmo = Atmosphere(altitude)
        self.input(f'D {(atmo.temperature[0]/(atmo.temperature[0]+temp_offset))*atmo.density[0]/515.378819}')
        self.top()

    def setVelocity(self, velocity): #Base
        self.oper()
        self.input('M')
        self.input('G 32.17')  
        self.input(f'V {velocity}')
        self.top()
        
    ### Commands for saving outputs. ###
    def save_output(self):
        self.input('MRF')
        self.input('ft Output/Total Forces\no')
        self.input('st Output/Stability Derivatives\no')
        self.input('sb Output/Body-Axis Derivatives\no')

    ### The command to run AVL. ###
    def run_avl(self, postrun = False): # opens avl and runs all of the stored commands
        self.AVLsp = subprocess.Popen(self.avlpath,
            shell=False,
            stdin=subprocess.PIPE,
            stdout=open('AVLsession.log', 'w'), # Put the output of this terminal into the open log file
            stderr=subprocess.PIPE)
        self.AVLsp.stdin.write(self.input_list.encode('utf-8'))
        self.AVLsp.stdin.flush()
        self.AVLsp.communicate()
        self.clear()
        if postrun == True:
            self.post_run()

    ### Post-run commands ###
    def post_run(self):
        for flag in self.post_run_flags:
            match flag:
                case 'store':
                    feed = self.post_run_flags[flag]
                    self.store.append(locate_in_output(output_file = feed[0], value = feed[1]))
                case 'trim':
                    feed = self.post_run_flags[flag]
                    print(f'Trim AoA: {locate_in_output(output_file = feed[0], value = feed[1])}')
                case _:
                    if flag is None:
                        print('No post-run flags.')
                    else:
                        print(f'Unknown post-run flag "{flag}".')

    ### Stability ###
    def trim(self):
        self.oper()
        self.input('a pm 0')
        self.input('x')
        self.save_output()
        self.post_run_flags['trim'] = ['Total Forces','Alpha']
    pass

    ### Optimization ###

    ### Unsorted. ###
    def load_opt_plane(self,plane): #Opt
        self.input('load Planes/{}/{}.avlopt_iter'.format(plane,plane))


    def setAtmosphere(self,altitude=0,temp_offset=0):
        # convert to imperial units
        altitude = altitude/3.28084 # ft to m
        temp_offset = 5/9*temp_offset # F to C
        self.input('oper')
        self.input('M')
        self.input('G 32.17')
        atmo = Atmosphere(altitude)
        self.input('D {}'.format((atmo.temperature[0]/(atmo.temperature[0]+temp_offset))*atmo.density[0]/515.378819))
        self.input('\n')

    def setVelocity(self,velocity):
        self.input('oper')
        self.input('M')
        self.input('G 32.17')  
        self.input('V {}'.format(velocity))
        self.input('\n')
        
    def saveOutput(self,output,name=0):
        self.input('MRF')
        self.input(output)
        if name == 0:
            self.input('output.{}'.format(output))
        else:
            self.input('{}.{}'.format(name,output))
        self.input('O\n')

    def readOutput(self,output,name=0):
        # load output file
        if name == 0:
            fname = ('output.{}'.format(output))
        else:
            fname = ('{}.{}'.format(name,output))
        
        out = np.array(open(fname).readlines()) # read the output file
        out = out[np.array(['|' in line for line in out])]


        var_dict = {}
        for line in out:
            line = line.replace('\n','').replace(':',',').split('|')
            line[0] = line[0].split()
            line[1] = [var.strip() for var in line[1].split(',')]
            for j in range(1,len(line[0])+1):
                var_dict[line[1][-j]] = float(line[0][-j])
        return var_dict
    
    def load_opt_template(self,plane): # loads an optimization template
        opt_template = open('Planes/{}/{}.avlopt_template'.format(plane,plane)).read() # read the optimization file
        optVars = re.findall(r'\{.*?\}',opt_template) # find all the declared variables

        # optVars = [var.replace('{','').replace('}','').split(',') for var in optVars] # remove brackets in var list
  
        var_dict = {} # create dictionary
        var_index = {}
        var_count = 0
        for index, optVar in enumerate(optVars): # name variables in dictionary
            opt_template = opt_template.replace(optVar,'{{{}}}')
            optVar = optVar.replace('{','').replace('}','').split(',')
            # print(optVar)
            if len(optVar) > 1:
                var_name = optVar[1]
                if var_name in var_dict.keys():
                    var_dict[var_name].append(float(optVar[0]))
                    var_index[var_name].append(int(index))
                else:
                    # print(optVar[0])
                    var_dict[var_name] = [float(optVar[0])]
                    var_index[var_name] = [int(index)]
            else: # if name not declared, give general name
                var_count += 1
                var_name = 'var_{}'.format(var_count)
                var_dict[var_name] = [optVar[0]]
                var_index[var_name] = [int(index)]
            # print('{'+str(index)+'}')

        # rearranges formatting for vector binning

        var_index_flat = [i for var in list(var_index.values()) for i in var]
        # print(var_index_flat)
        opt_template = opt_template.format(*list(np.argsort(var_index_flat))) # do not ask
        # print(np.argsort(var_index_flat))
        # print(opt_template)
        # print(*[item for index in list(var_dict.values()) for item in index])
        self.opt_template = opt_template # stores template
        self.var_dict = var_dict # stores vars within itself

        # print(opt_template)
        # print(np.argsort(var_index_flat))
        # print(var_dict.values())

    def writeOptimize(self,plane): # writes new values into iteration

        # this needs fixing bruhhh
        with open('Planes/{}/{}.avlopt_iter'.format(plane,plane),'w') as file:
            file.write(self.opt_template.format(*[i for var in list(self.var_dict.values()) for i in var]))
        # self.updateRefs(plane)
        # with open('Planes/{}/{}.avlopt_iter'.format(plane,plane),'w') as file:
        #     file.write(self.opt_template.format(*self.var_dict.values()))   

    def updateRefs(self,plane): # calculates new reference values
        with open('Planes/{}/{}.avlopt_iter'.format(plane,plane),'r') as file:
            fstring = np.array(file.readlines()) # reads line by line
            # print(fstring)
            surfref = []    
            for index, line in enumerate(fstring):
                if 'SURFACE' in line:
                    surfref.append(index)
                    if len(surfref) > 1:
                        break
            sectionindex = []
            for index, line in enumerate(fstring[:surfref[1]]):
                if 'SECTION' in line:
                    sectionindex.append(index)

            planform_data = []
            for i in range(len(sectionindex)):
                planform_data.append([float(line) for line in np.array(fstring[sectionindex[i]+1].split())[[1,3]]]) # disgusting python one liner
            planform_data = np.array(planform_data)
            # print(planform_data)
            
            section_lengths = planform_data[1:,0]-planform_data[:-1,0]
            self.var_dict['Bref'] = [2*sum(section_lengths)]
            S_ref = sum(section_lengths*(planform_data[:-1,1]+planform_data[1:,1]))
            self.var_dict['Cref'] = [2/S_ref*sum( section_lengths*(planform_data[:-1,1]*planform_data[1:,1]+1/3*(planform_data[1:,1]-planform_data[:-1,1])**2) )]
            self.var_dict['Sref'] = [S_ref]

            # print([section_lengths])
            
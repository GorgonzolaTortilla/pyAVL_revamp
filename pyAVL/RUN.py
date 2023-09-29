from py_AVL import AVL
from Scripts.py_AVL_stability import AVL_stability
from Scripts.py_AVL_optimization import AVL_optimization
from Scripts.parsing_scripts import *

avl = AVL()
### Your commands here. ###
avl.load_plane('a') 
mark_in_avl(plane_name = 'a', surface_name = 'wing', section_number = 2, parameter = 'yle')
avl.initialize_template()
avl.parameter_sweep(start_values = [1], end_values = [6], N = 21)



###########################
avl.run_avl()
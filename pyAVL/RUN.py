from py_AVL import AVL
from Scripts.py_AVL_stability import AVL_stability
from Scripts.py_AVL_optimization import AVL_optimization
from Scripts.parsing_scripts import *

avl = AVL_optimization()
# avl = AVL_optimization()
# type = optimization
### Your commands here. ###
avl.load_plane('a')
mark_in_avl(plane_name = 'a', surface_name = 'hstab', parameter = 'angle')
avl.initialize_template()
avl.parameter_sweep(start_values = [0], end_values = [10], N = 20)



###########################
avl.run_avl()
from py_AVL import AVL

class AVL_stability(AVL):
    def __init__(self):
        super().__init__()

    def trim(self):
        self.oper()
        self.input('a pm 0')
        self.input('x')
        self.save_output()
        self.post_run_flags['trim'] = ['Total Forces','Alpha']
    pass

class Surface():
    name = None
    position = None
    angle = None
    xle = None
    yle = None
    zle = None
    chord = None
    airfoil = None

    def __init__(self, info_dump):
        # Takes "info_dump" of name, position, angle, xle, yle, zle, chord (hopefully in that order) to create the geometry.

        #Imported keywords to parse "info_dump".
        from Scripts.keys import surf_keywords, surf_components

        #Search the info dump and assign surface parameters.
        #I know this is ugly, but it's serviceable. 
        for row in info_dump:
            print(row)
            if row in surf_keywords:
                self.name = row
            elif row[0] in surf_components:
                match row[0]:
                    case 'position':
                        self.position = list(map(float,row[1:]))
                    case 'angle':
                        self.angle = list(map(float,row[1:]))
                    case 'xle':
                        self.xle = list(map(float,row[1:]))
                    case 'yle':
                        self.yle = list(map(float,row[1:]))
                    case 'zle':
                        self.zle = list(map(float,row[1:]))
                    case 'chord':
                        self.chord = list(map(float,row[1:]))
                    case 'airfoil':
                        airfoil = row[1]
                        try:
                            for x in row[2:]:
                                airfoil += ' ' + x
                        except:
                            pass
                        self.airfoil = airfoil

            else:
                print(f'Unregonized keyword "{row[0]}" in first column; skipping row: {row}')

    # This⬇⬇ doesn't work well because it writes to the main directory and doesn't take a 
    # Plane name because it's just a surface. Maybe the surfaces could be assigned a plane_name
    # at initialization?

    # def WriteSurfaceAVL(self, plane_name):
    #     sref, cref, bref = self.ReferenceGeometry()
    #     TemplateAVL(plane_name = self.name, sref = sref, cref = cref, bref = bref, xcg = 0.25)
    #     self.WriteToAVL(plane_name)

    def modify_nodes(self, Nchordwise = 8, Csapce = 1.0, Nspanwise = 12, Sspace = 1.0):
        pass

    def write_to_avl(self, plane_name):   
        
        with open(f'Models/Planes/{plane_name}/{plane_name}.avl','a') as f:
            f.write('SURFACE\n')
            f.write(f'{self.name}\n')
            f.write(f'8 1.0 12 1.0 # Nchordwise Cspace Nspanwise Sspace\nYDUPLICATE\n0.0 # YDUPLICATE\nANGLE\n{self.angle[0]} # ANGLE\nTRANSLATE\n{self.position[0]} {self.position[1]} {self.position[2]} # TRANSLATE\n') # Generic parameters, adjust these later maybe
            for i,c in enumerate(self.chord):
                f.write('SECTION\n')
                f.write(f'{self.xle[i]} {self.yle[i]} {self.zle[i]} {c} 0.0 0 0 # Xle Yle Zle Chord Ainc Nspanwise Sspace\n')
                f.write(f'AFILE\nModels\Airfoils\{self.airfoil}.dat\n')

    def reference_geometry(self):
        sref = 0
        cref = 0
        bref = 2*self.yle[-1]
        for i in range(len(self.yle)-1):
            sref += (self.yle[i+1]-self.yle[i])*(self.chord[i]+self.chord[i+1])
        for i in range(len(self.yle)-1):
            y1 = self.yle[i]
            c1 = self.chord[i]
            dy = self.yle[i+1] - y1
            taper = self.chord[i+1]/c1
            m = (taper - 1)/dy
            cref += 2/sref*( c1**2*( m**2/3*dy**3 + (m - y1*m**2)*dy**2 + (1 - y1*m)**2*dy) )
        return sref, cref, bref 
        
def template_avl(plane_name,\
                sref = 10.0, cref = 1.0, bref = 10.0,\
                xcg = 0.25, ycg = 0.0, zcg = 0.0):
    with open(f'Models/Planes/{plane_name}/{plane_name}.avl','w') as f:
        f.write(f'{plane_name}\n')
        f.write(f'0.0 # Mach\n0 0 0 # IYsym IZsym Zsym\n{sref} {cref} {bref} # Sref Cref Bref\n{xcg} {ycg} {zcg} # Xref Yref Zref\n')

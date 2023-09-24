from Generator.SurfaceClass import Surface, template_avl
from Scripts.parsing_scripts import geometry_file_to_string, surface_split_indices

def generate_avl(filename = 'Generator/Geometry', plane_name = 'a'):
    #Read an already formatted (and more intuitive) file to create an unlabeled AVL file
    surfaces = []
    formatted_string = geometry_file_to_string(filename)
    index = surface_split_indices(formatted_string)
    
    #Creates surfaces array and make surface objects
    for i in range(len(index)-1):
        surfaces.append(Surface(formatted_string[index[i]:index[i+1]]))
    #Find wing surface and use values for reference geometry
    for surf in surfaces:
        if surf.name.lower() == 'wing':
            sref, cref, bref = surf.reference_geometry()
            template_avl(plane_name = plane_name, sref = sref, cref = cref, bref = bref, xcg = 0.5, zcg = 0.1)
            break
        elif surf == surfaces[-1]:
            template_avl(plane_name = plane_name)
            print('Error: no "wing" found. Generating default template with:\n'+\
                  'Sref = 10.0, cref = 1.0, bref = 10.0\n'+\
                  'Please check your geometry file to ensure "wing" is present.')
        else: continue        
    #Go through surfaces and write each to AVL file
    for i,surf in enumerate(surfaces):
        # surf.WriteSurfaceAVL(plane_name)
        surf.write_to_avl(plane_name)
    return None
    
generate_avl()

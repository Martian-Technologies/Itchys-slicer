import trimesh
import customtkinter as ctk


class Selector:
    def select_3d_file(self):
        filename = ctk.filedialog.askopenfilename(
            title='Select 3D File', filetypes=(('3D object', '*.obj;*.stl;*.ply;*.glb'), ('All files', '*.*')))
        if filename:
            extension = filename.split('.')[-1]
            if extension in ['obj', 'stl', 'ply', 'glb']:
                try:
                    mesh = trimesh.load(filename)
                    mesh.vertices -= mesh.center_mass
                    return mesh
                except Exception as e:
                    raise Exception('Failed to load file:\n{e}')
            else:
                raise Exception('Unsupported file format:\n.{extension}')

    def checkIfFlip(self, mesh):
        mesh.show()
        doflip = 'y' == input('do you want to flip the y and z axes (y/n): ')
        if doflip:
            mesh.vertices[:, [0, 1, 2]] = mesh.vertices[:, [0, 2, 1]]
            mesh.show()

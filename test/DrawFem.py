
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import EntityClass

class DrawModel:
    
    def __init__(self, triangle, coordinate) -> None:
        self.triangle = triangle
        self.coordinate = coordinate
        
    
    def draw_fea(self):
        """
        draw and show the  triangulated graph.
        
        :param triangle:    triangles list
        :param coordinate:  triangles' coordinate list
        
        
        :return: figure of FEA triangulation
        """
        elem = self.triangle

        x = []
        y = []
        for em in self.coordinate:
            x.append(em.get_x())
            y.append(em.get_y())
        plt.figure()
        plt.scatter(x, y, s=8)
        plt.gca().set_aspect('equal')
        mesh_fig = tri.Triangulation(x, y, elem)
        plt.triplot(mesh_fig, 'b.-', lw=1)
        plt.show()


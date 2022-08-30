
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import EntityClass

class DrawModel:
    
    def __init__(self, triangle, coordinate, rou) -> None:
        self.triangle = triangle
        self.coordinate = coordinate
        self.rou = rou
        
    
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

    def draw_rou(self):
        """draw the figures of the changed rou.
        """
        
        elem = self.triangle
        
        x = []
        y = []
        for em in self.coordinate:
            x.append(em.get_x())
            y.append(em.get_y())
        
        max_rou = max(self.rou[3])
        #print(max_rou)
        
        
        plt.figure()    
        for i in range(1, 5):
            
            plt.subplot(2, 2, i)
        
            plt.scatter(x, y, s=4)
            plt.gca().set_aspect('equal')
            mesh_fig = tri.Triangulation(x, y, elem)
            plt.triplot(mesh_fig, 'b.-', lw=1)
            
            for j in range(len(elem)):
                triangle_x = []
                triangle_y = []
                for p in range(3):
                    triangle_x.append(x[int(self.triangle[j][p])])
                    triangle_y.append(y[int(self.triangle[j][p])])
                triangle_x.append(triangle_x[0])
                triangle_y.append(triangle_y[0])
                color = self.rou[i - 1 ][j] / max_rou
                #print(color)
                plt.fill(triangle_x, triangle_y, color=(float(color),0.5, 0.5))
            
            
        
    
        plt.show()
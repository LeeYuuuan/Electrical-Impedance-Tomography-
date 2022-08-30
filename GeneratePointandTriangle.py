
from GeneratePoint import GeneratePointModel
from GenerateTriangle import GenerateTriangleModel
from DrawFem import DrawModel


class GeneratePointandTriangle:
    
    def __init__(self, count_layer, model_radius) -> None:
        """
        triangle:       save the triangle list.
        coordinate:     save the point coordinate list.
        point:          save the point id list.
        point_object:   save the object of point.   
        """
        self.count_layer = count_layer
        self.model_radius = model_radius
        
        self.triangle = None
        self.coordinate = None
        self.point = None
        self.point_object = None
    
    def initialize_parameters(self):
        """ 1. Generate the <object>Points  and <object> Triangles.
            2. Get points id List.
            3. Get points object List.
            4. Get coordinates List.
            5. Get Triangle List.
        """
        gpm = GeneratePointModel(self.count_layer, self.model_radius)
        self.point_object = gpm.get_point_list()
        self.point = gpm.get_point_id_list()
        self.coordinate = gpm.get_coordinate_list()
        
        gtm = GenerateTriangleModel(self.count_layer,self.model_radius, self.point_object)
        self.triangle = gtm.get_triangle()
    
    def get_triangle_list(self):
        return self.triangle
    
    def get_object_list(self):
        return self.point_object
    
    def get_point_list(self):
        return self.point
    
    def get_coordinate_list(self):
        return self.coordinate
    
    def draw_pic(self):
        
        dw = DrawModel(self.triangle, self.point_object)
        dw.draw_fea()

class GetPointandTriangle:
    def __init__(self) -> None:
        pass

                
    
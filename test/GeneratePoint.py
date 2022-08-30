
import math
from EntityClass import Point


class GeneratePointModel:
    
    
    def __init__(self, count_layer: int, model_radius: float) -> None:
        """_summary_

        Args:
            count_layer (int): The count of model layers.
            model_radius (float): The model radius.
        """
        if type(count_layer) == int and type(model_radius) in [int, float]:
            self.count_layer = count_layer
            self.model_radius = model_radius
            self.point_id = []
            self.point = []
            self.coordinate = []
        
        self.generate_point()
        
        
    
    def get_layer_radius(self, layer_id):
        """

        :param layer_id: which layer number to return
        :return the radius of this layer """

        if self.count_layer >= layer_id > 0:
            return layer_id * self.model_radius / self.count_layer
        else:
            return False

    def get_coordinate(self, point_log_id, layer_id):
        """
        get the coordinate of the point in a certain layer and number
        
        :param point_log_id: the logical id of this point in its layer
        :param layer_id: the id of the layer which this point belongs to
        :return: the coordinate of this point [float, float, 0]
        """
        if layer_id == 0:
            return [0, 0, 0]
        
        from FunctionSet import get_layer_point_count
        point_count = get_layer_point_count(layer_id)
        degree = (point_log_id / point_count) * 2 * math.pi
        x = round(math.cos(degree), 4) * self.get_layer_radius(layer_id)
        y = round(math.sin(degree), 4) * self.get_layer_radius(layer_id)
        
        return [x, y, 0.0]


    def generate_point(self):
        """
        sum_point_count: point 的总数
        current_layer: 遍历过程中当前的层数
        threshold: 遍历当前位置所在层的节点总数和之前遍历过所有层的节点总数之和
        :return: 获得包含 Point坐标的模型
        """
        from FunctionSet import get_layer_point_count, get_sum_point_count
        sum_point_count = get_sum_point_count(self.count_layer) + 1  # sum number of the point

        current_layer = self.count_layer
        previous_threshold = 0
        threshold = get_layer_point_count(current_layer)

        for p_c in range(sum_point_count):
            if p_c > threshold - 1:
                current_layer -= 1
                previous_threshold = threshold
                threshold += get_layer_point_count(current_layer)
            point_logical_id = p_c - previous_threshold
            point_coordinate = self.get_coordinate(point_logical_id, current_layer)
            point_gene = Point(p_c, point_logical_id, point_coordinate)
            self.coordinate.append(point_coordinate)
            self.point.append(point_gene)
            self.point_id.append(p_c)
    
    
    def get_point_list(self):
        """
        get the ordered point list.
         
        """
        
        return self.point
    
    def get_coordinate_list(self):
        """
        get the coordinate of all point.

        Returns: coordinate:
            _type_: list[x, y, z]
        """
        return self.coordinate
    
    def get_point_id_list(self):
        """get the list of point id.

        Returns:
            _type_: List of point id.
        """
        return self.point_id

"""
x = GeneratePointModel(3, 1)
print(x.get_point_id_list())
print(x.get_coordinate_list())"""



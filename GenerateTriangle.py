
import numpy as np


from GeneratePoint import GeneratePointModel




class GenerateTriangleModel:
    def __init__(self, count_layer: int, model_radius: float, point) -> None:
        
        self.point = point
        self.count_layer = count_layer
        self.model_radius = model_radius
        self.triangle = None
        
        self.generate_triangle()
        self.modified_triangle()
        
    
    def generate_layer_triangle(self, layer_id):
        """

        :param layer_id: 生成三角形的层号
        :return: 生成三角形
        """
        from FunctionSet import get_sum_point_count, generate_triangle_in_one_quadrant, get_several_layers_point_count

        if layer_id == 1:
            cur_start = get_several_layers_point_count(layer_id, self.count_layer)
            o = get_sum_point_count(self.count_layer)
            triangle = generate_triangle_in_one_quadrant(1, 1, self.point[cur_start], self.point[o], layer_id)
            return triangle

        cur_start = get_several_layers_point_count(layer_id, self.count_layer)
        per_start = get_several_layers_point_count(layer_id - 1, self.count_layer)
        triangle = generate_triangle_in_one_quadrant(1, 1, self.point[cur_start], self.point[per_start], layer_id)
        for tp in range(1, 3):
            for quadrant in range(2, 5):
                triangle = np.concatenate((triangle,
                                           generate_triangle_in_one_quadrant(
                                               tp, quadrant, self.point[cur_start], self.point[per_start], layer_id)),
                                          axis=0)
                if tp == 1 and quadrant == 4:
                    triangle = np.concatenate((triangle,
                                               generate_triangle_in_one_quadrant(
                                                   2, 1, self.point[cur_start], self.point[per_start], layer_id)),
                                              axis=0)
        return triangle

    def generate_triangle(self):
        """

        :return: generate all FEA element triangles.
        """
        triangle = self.generate_layer_triangle(1)
        for i in range(2, self.count_layer + 1):
            triangle = np.concatenate((triangle, self.generate_layer_triangle(i)))

        self.triangle = triangle

    def modified_triangle(self):
        """
        modified the triangle list:
        Number each triangle element counterclockwise.
        """ 
        def get_local_id_of_triangle(pt):
            """
            calculate the local id of the point for a triangle by coordinate.

            :param pt: three points of the triangle   type = list[pt1, pt2, pt3]
            :return: dict: lst [id, id, id]
            """
            order = []
            order_disorderly = [pt[0], pt[1], pt[2]]
            min_pt = np.array(order_disorderly).argmin()
            order.append(min_pt)
            order_disorderly.remove(pt[min_pt])
            target = 0  # 共有两种节点编号模式，若识别为第一种则target = 1, 跳过第二种模式的识别过程
            for i in range(2):
                if pt[min_pt] + 1 == order_disorderly[i]:
                    order.append(pt.index(order_disorderly[i]))
                    order_disorderly.remove(order_disorderly[i])
                    order.append(pt.index(order_disorderly[0]))
                    target = 1
                    break
            if target == 0:
                max_pt = np.array([pt[0], pt[1], pt[2]]).argmax()
                order.append(max_pt)
                order_disorderly.remove(pt[max_pt])
                order.append(pt.index(order_disorderly[0]))

            return order

        for i in range(len(self.triangle)):
            trg = self.triangle[i]
            pt = [trg[0], trg[1], trg[2]]
            local_order = get_local_id_of_triangle(pt)
            j = 0
            for index in local_order:
                self.triangle[i][index] = pt[j]
                j += 1        
        
    
    def get_triangle(self):
        """return triangle list.
        """
        return self.triangle


#x = GeneratePointModel(3, 1)
#print(x.get_point_id_list())
#print(x.get_coordinate_list())

#a = GenerateTriangleModel(3, 1, x.get_point_list())
#print(len(a.get_triangle()))


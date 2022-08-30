import numpy as np

class Point:
    def __init__(self, point_id, point_id_in_layer, point_coordinate, ):
        """

        :param point_id: 每个剖分点的编号                   type: int
        :param point_coordinate: 每个剖分点的坐标(3-d)      type: list[float, float, float]
        :param point_id_in_layer: 每个节点在该层中的逻辑id   type: int

        NOTE:
        if the point_id is not int, use None to initialize the  Point.
        if the len of point_coordinate is 2, use 0 to fill "z" (dim 3).
        if the type or the len is not available, use [None, None, None] to fill.
        """
        if type(point_id) == int:
            self.point_id = point_id
        else:
            print("point_id is not available!")
            self.point_id = None

        if type(point_coordinate) == list and len(point_coordinate) == 3:
            self.point_coordinate = point_coordinate
        elif type(point_coordinate) == list and len(point_coordinate) == 2:
            self.point_coordinate = point_coordinate.append(0)
        else:
            print("Point coordinate Initialization failed!")
            self.point_coordinate = [None, None, None]
        if type(point_id_in_layer) == int:
            self.point_id_in_layer = point_id_in_layer
    
    def get_coordinate(self):
        """ :return: 返回 Point坐标 """
        return self.point_coordinate

    def get_x(self):
        """ :return: 返回 Point 横坐标"""
        return self.point_coordinate[0]

    def get_y(self):
        """ :return: 返回 Point 纵坐标"""
        return self.point_coordinate[1]

    def get_z(self):
        """ :return: 返回 Point z坐标"""
        return self.point_coordinate[2]

    def get_id(self):
        """ :return: 返回 Point_id"""
        return self.point_id

    def get_log_id(self):
        """ :return: 返回 Point_id_in_layer 该点在其所在层的 logical id"""
        return self.point_id_in_layer


class Triangle:
    
    """
    create a triangle with:
        point1: id of point1
        point2: id of point2
        point3: id of point3
        
        edgelist: list[]
        
        coordinate1: coordinate of point1
        coordinate2: coordinate of point2
        coordinate3: coordinate of point3
        
        a: a1 = x2y3 - x3y2;     a2 = x3y1 - x1y3   a3 = x1y2 - x2y1
        b: b1 = y2 - y3;         b2 = y3 - y1       b3 = y1 - y2
        c: c1 = x3 - x2;         c2 = x1 - x3       c3 = x2 - x1
        
        rou: the resistivity of this triangle element.
        
        area: the area of this triangle.
        ke: the element_stiffness_matrix of this element.
        
    """
      
    def __init__(self, triangle, point) -> None:
        self.point1 = triangle[0]
        self.point2 = triangle[1]
        self.point3 = triangle[2]
        
        self.coordinate1 = point[self.point1].get_coordinate()
        self.coordinate2 = point[self.point2].get_coordinate()
        self.coordinate3 = point[self.point3].get_coordinate()
        
        x1, y1, z1 = self.coordinate1
        x2, y2, z2 = self.coordinate2
        x3, y3, z3 = self.coordinate3
        
        self.a1 = x2 * y3 - x3 * y2
        self.a2 = x3 * y1 - x1 * y3
        self.a3 = x1 * y2 - x2 * y1
        
        self.b1 = y2 - y3
        self.b2 = y3 - y1
        self.b3 = y1 - y2
        
        self.c1 = x3 - x2
        self.c2 = x1 - x3
        self.c3 = x2 - x1
        
        self.rou = float(2)
        self.ke = None
        self.del_ke = None
        
        def calculate_area_2(p1, p2, p3):
            """
            calculate twice the area of the elements.
            :param p1: The first point
            :param p2: The second point
            :param p3: The third point
            :return: twice the area of the triangle.
            """
            
            matrix = np.array([
                [1.0, p1[0], p1[1]],
                [1.0, p2[0], p2[1]],
                [1.0, p3[0], p3[1]]])
            det = np.linalg.det(matrix)
            return abs(det)

        self.area = 0.5 * calculate_area_2(self.coordinate1, self.coordinate2, self.coordinate3)
    
    def calculate_changed_parameters(self):
        
        def calculate_element_stiffness_matrix():
            esm = np.zeros([3, 3])
            esm[0, 0] = (self.b1 * self.b1 + self.c1 * self.c1)/(4 * self.rou * self.area)
            esm[1, 1] = (self.b2 * self.b2 + self.c2 * self.c2)/(4 * self.rou * self.area)
            esm[2, 2] = (self.b3 * self.b3 + self.c3 * self.c3)/(4 * self.rou * self.area)
            
            esm[0, 1] = (self.b1 * self.b2 + self.c1 * self.c2)/(4 * self.rou * self.area)
            esm[1, 0] = (self.b1 * self.b2 + self.c1 * self.c2)/(4 * self.rou * self.area)
            
            esm[0, 2] = (self.b1 * self.b3 + self.c1 * self.c3)/(4 * self.rou * self.area)
            esm[2, 0] = (self.b1 * self.b3 + self.c1 * self.c3)/(4 * self.rou * self.area)

            esm[1, 2] = (self.b2 * self.b3 + self.c2 * self.c3)/(4 * self.rou * self.area)
            esm[2, 1] = (self.b2 * self.b3 + self.c2 * self.c3)/(4 * self.rou * self.area)

            return esm
        
        self.ke = calculate_element_stiffness_matrix()
        
        def calculate_derivative_element_stiffness_matrix():
            desm = np.zeros([3, 3])
            
            desm[0, 0] = - (self.b1 * self.b1 + self.c1 * self.c1)/(4 * self.rou * self.area * self.rou)
            desm[1, 1] = - (self.b2 * self.b2 + self.c2 * self.c2)/(4 * self.rou * self.area * self.rou)
            desm[2, 2] = - (self.b3 * self.b3 + self.c3 * self.c3)/(4 * self.rou * self.area * self.rou)
            
            desm[0, 1] = - (self.b1 * self.b2 + self.c1 * self.c2)/(4 * self.rou * self.area * self.rou)
            desm[1, 0] = - (self.b1 * self.b2 + self.c1 * self.c2)/(4 * self.rou * self.area * self.rou)
            
            desm[0, 2] = - (self.b1 * self.b3 + self.c1 * self.c3)/(4 * self.rou * self.area * self.rou)
            desm[2, 0] = - (self.b1 * self.b3 + self.c1 * self.c3)/(4 * self.rou * self.area * self.rou)

            desm[1, 2] = - (self.b2 * self.b3 + self.c2 * self.c3)/(4 * self.rou * self.area * self.rou)
            desm[2, 1] = - (self.b2 * self.b3 + self.c2 * self.c3)/(4 * self.rou * self.area * self.rou)

            return desm
        self.del_ke = calculate_derivative_element_stiffness_matrix()
        
    def get_coordinate(self):
        
        return self.coordinate1, self.coordinate2, self.coordinate3
    
    def print_rou(self):
        print(self.rou)
    

class Edge:
    """
    create a edge with two Point_id
    """

    def __init__(self, pt_1, pt_2):
        self.edge = set()

        self.edge.add(pt_1)
        self.edge.add(pt_2)

    def is_equal(self, edge_target):
        """

        :param edge_target: The target edge to judge if they are equal.
        :return: True if they are equal, False for not equal.
        """
        if self.edge == edge_target.edge:
            return True
        else:
            return False
            
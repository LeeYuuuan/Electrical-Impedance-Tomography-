from EntityClass import Point, Triangle, Edge
import numpy as np
class PointTest:
    """Test for class <Point>
    """
    def __init__(self) -> None:
        self.p = Point(0,0,[0.,0.,0.])
        
    
    def point_test(self):
        pass
    


class TriangleTest:
    
    
    def __init__(self) -> None:
        
        p1 = Point(0, 0, [2, 0, 0])
        p2 = Point(1, 1, [2, 0.5, 0])
        p3 = Point(2, 2, [1, 0, 0]) 
        point = [p1, p2, p3]
        
        self.trg = Triangle([0, 1, 2], point)
    
    def test_calculate_changed_parameters(self):
        self.trg.calculate_changed_parameters()
        
        print("===rou===")
        print("  ",self.trg.rou, self.trg.rou == 2.0)
        print("=========")
        
        print("+++Area+++")
        print("  ",self.trg.area, self.trg.area == 0.25)
        print("++++++++++")

        
        print("=======单元刚度矩阵=======")
        print(self.trg.ke)
        print("True")
        print("===========================")
        
        print("=======单元刚度矩阵的导数=======")
        print(self.trg.del_ke,)
        print("True")
        print("=================================")
        
        print("=========parameters==============")
        print("a1:",self.trg.a1,"   a2:", self.trg.a2,"a3:", self.trg.a3)
        print("b1:",self.trg.b1,"    b2:", self.trg.b2,"b3:", self.trg.b3)
        print("c1:",self.trg.c1,"     c2:", self.trg.c2,"c3:", self.trg.c3)

        print(" True")
        print("=================================")
        
        
        
TT = TriangleTest()
TT.test_calculate_changed_parameters()
        
        
        
        


        
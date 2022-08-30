
from scipy.misc import derivative
from EntityClass import Triangle
from GeneratePoint import Point
from FunctionSet import *
from GeneratePointandTriangle import GeneratePointandTriangle
from DrawFem import DrawModel
np.set_printoptions(suppress=True, threshold=np.sys.maxsize)
import math


class FEAModel:
    def __init__(self, count_layer=3, model_radius=2):
        """

        :param count_layer: 剖分层数
        :param model_radius: 模型半径

        coordinate 做标 List
        triangle   单元（三角形） List
        """
        if type(count_layer) == int and type(model_radius) in [int, float]:
            self.count_layer = count_layer
            self.model_radius = model_radius
            self.point_id = None
            self.point = None
            self.coordinate = None
            self.triangle = None  # save the triangle elements
            self.excitation_count = 16
            
            self.current = 0.1 # current injected: I = 0.1
            
            self.triangle_object = []

            #self.triangle_parameters = []
            
            
            
            self.global_matrix = None
            self.b = None
            self.voltage_matrix = None

            self.del_global_matrix = None

            #self.jacobian = None
            self.inv_Y = None
            self.v0 = None
    
    
    def set_point_triangle(self):
        gpt = GeneratePointandTriangle(self.count_layer, self.model_radius)
        gpt.initialize_parameters()
        self.triangle = gpt.get_triangle_list()
        self.point = gpt.get_object_list()
        self.coordinate = gpt.get_coordinate_list()
        self.point_id = gpt.get_point_list()
    
    def generate_triangle_object(self):
        """ 
            1> calculate a, b, c, area
            2> set default rou
            3> save them in List[t_obj,...].
        """
        for trg in self.triangle:
            self.triangle_object.append(Triangle(trg, self.point))
    
    def set_parameters(self):
        """calculate the :
            1> element stiffness matrix
            2> derivative of element stiffness matrix
        """
        for trgo in self.triangle_object:
            trgo.calculate_changed_parameters()
        
    def set_all_resistivity(self, values):
        """set resistivity for all elements.
                1> set all elements with a certain number.
                2> set them to different values

        Args:
            values (int/float/list/np.array): modified value(s).
        """ 
        if type(values) in [float, int]:
            for to in self.triangle_object:
                to.rou = values
        else:
            for i in range(len(self.triangle_object)):
                self.triangle_object[i].rou = values[i]
        
    def get_global_matrix_index(self, n, e):
        """

        :param n: which local id of the point 0, 1, 2 --> 1, 2, 3
        :param e: which element.
        :return: int -->global id
        """
        return self.triangle[e][n]
    
    def calculate_global_matrix(self):
        """calculate the global matrix.
        """
        n_point = len(self.point)
        self.global_matrix = np.zeros((n_point, n_point))
        for e in range(len(self.triangle_object)):
            ke = self.triangle_object[e].ke
            for i in range(3):
                for j in range(3):
                    self.global_matrix[self.get_global_matrix_index(i,e), self.get_global_matrix_index(j,e)] += ke[i, j]

    def calculate_derivative_global_matrix(self):
        """calculate the derivative of the global matrix.
        """
        n_point = len(self.point)
        self.del_global_matrix = np.zeros((n_point, n_point))
        for e in range(len(self.triangle_object)):
            ke = self.triangle_object[e].del_ke
            for i in range(3):
                for j in range(3):
                    self.del_global_matrix[self.get_global_matrix_index(i,e), self.get_global_matrix_index(j,e)] += ke[i, j]

    def calculate_modified_matrix(self, reference_index, inj_idx, matrix_type=0):
        """
        modify the global matrix with:
            1> Cauchy boundary condition 
                   setting the corresponding row and column of the master
                   matrix to 0, with 1 at the diagonal, and setting the
                   corresponding element of the current vector to 0. 
            2> Dirichlet boundary condition (known surface voltages).
             
        
        Args:
            reference_index (int): the index of reference point 
            matrix_type (1/0 int): 0 for global matrix and 1 for derivative one.

        Returns:
            np.ndarray: modified matrix
        """
        if matrix_type == 0:
           res = self.global_matrix.copy()
           r_id = (inj_idx + 12) % 16
           res[r_id][:] = 0
           res[:][r_id] = 0
           res[r_id][r_id] = 1 
            
        if matrix_type == 1:
            res = self.del_global_matrix
        

        
        
        return res
            
    
    def get_modified_matrix_and_b(self, reference_index, injected_point):
        """
        get the modified global matrix and b.
           
        Args:
            reference_index (_type_): the index of reference point 

        Returns:
            np.ndarray: modified matrix, b
        """
        
        n_point = len(self.point)
        self.b = np.zeros([n_point, 1])
        b = self.b.copy()
        b[injected_point] = self.current
        b[(injected_point + 8)%16] = - self.current
        
        return self.calculate_modified_matrix(reference_index, injected_point, 0), b
    
    
        
    
    def calculate_voltage_vector(self, inject_idx=0):
        """get the solution of the forward problem:
                1> matrxi of voltage: 37*16 s*p
                2> vector of voltage: vec(V) [37*16] *1

        Args:
            inject_idx (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        Y, b = self.get_modified_matrix_and_b(12, int(inject_idx))
        # print(np.linalg.pinv(Y) @ b) 
        # 这里计算的结果solve结果相同
        return np.linalg.solve(Y, b)
    
    
    def p_times_observe(self, p=16):
        """16 times observe.

        Args:
            p (int, optional): what times to observe. Defaults to 16.

        Returns:
            voltage matrix, voltage vector: the matrix of voltage and the vector of one after reshaping.
        """
        
        voltage_matrix = self.calculate_voltage_vector(0)
        voltage_vector = self.calculate_voltage_vector(0)
        for i in range(1, p):
            voltage_matrix = np.concatenate((voltage_matrix, self.calculate_voltage_vector(i)), axis=1)
            voltage_vector = np.concatenate((voltage_vector, self.calculate_voltage_vector(i)), axis=0)
        return voltage_matrix, voltage_vector
    
    def get_inv_Y(self):
        from scipy import linalg
        return linalg.inv()
    
    def calculate_derivate_of_Y_to_jth_rou(self, e):
        """calculate the derivative of the global matrix.

        Args:
            e (int): derivative of global matrix (Y) with respect to eth rou.
        Returns:
            np.ndarray 37*37: the derivative of the global matrix with respect to eth rou.
        """
        n_point = len(self.point)
        #self.del_global_matrix = np.zeros((n_point, n_point))
        del_global_matrix = np.zeros((n_point, n_point))
        ke = self.triangle_object[e].del_ke
        for i in range(3):
            for j in range(3):
                del_global_matrix[self.get_global_matrix_index(i,e), self.get_global_matrix_index(j,e)] += ke[i, j]
        return del_global_matrix
    
    def change_rou(self):
        """change value of a certain location rou.
        """
        self.triangle_object[41].rou = 100
        self.triangle_object[42].rou = 1000000000000000000000000
        self.triangle_object[54].rou = 1000000000000000000000000
    
    def rechange_rou(self):
        """change value of a certain location rou.
        """
        self.triangle_object[41].rou = 2
        self.triangle_object[42].rou = 2
        self.triangle_object[54].rou = 2
    
    def model_initialize(self):
        """Initialize the model prarmeters.
        """
        self.set_point_triangle()
        self.generate_triangle_object()
         
    
    def forward(self, p=16):
        self.set_parameters()
        self.calculate_global_matrix()
        #self.calculate_derivative_global_matrix()
        
        matrix, vector = self.p_times_observe(p)
        
        return matrix, vector
    
    def backword(self):
        matrix_t = generate_matrix_t()
        matrix, vector = self.forward()
        print((matrix_t @ vector)[0:24])
        print(vector[37:53])
    
    
    def testx(self):
        self.model_initialize()
        self.forward()
        
        
        
    
    def model_draw(self):
        
        dw = DrawModel(self.triangle, self.point)
        dw.draw_fea()
        
        
if __name__ == "__main__":
    fea = FEAModel()
    #fea.testx()
    #fea.model_draw()


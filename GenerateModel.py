"""
    This model is for 16 times observe.
        1. We select reference node to relativly invariable.
        2. We calculate the difference of voltages between every two boundary nodes except excitation nodes.
            Note: there will be 4 voltages cut.
            
"""

from asyncio.proactor_events import _ProactorBasePipeTransport
from webbrowser import get
from scipy.misc import derivative
from EntityClass import Triangle
from GeneratePoint import Point
from FunctionSet import *
from GeneratePointandTriangle import GeneratePointandTriangle
from DrawFem import DrawModel
np.set_printoptions(suppress=True, threshold=np.sys.maxsize)

from scipy import linalg as linalg


class FEAModel:
    
    def __init__(self, count_layer=3, model_radius=2):
        """_summary_

        Args:
            count_layer (int, optional): the number of layers. Defaults to 3.
            model_radius (int, optional): the radius of the model. Defaults to 2.
        """
        
        if type(count_layer) == int and type(model_radius) in [int, float]:
            self.count_layer = count_layer
            self.model_radius = model_radius
            
            
            self.triangle = None  # save the triangle elements. (List)
            self.point_id = None # save the points id.  (List)
            self.point = None # save the <class>Point. (List)
            self.coordinate = None # save the coordinates. (List)
            self.triangle_object = [] # save the list of <object> triangles.
            
            
            self.current = 0.1 # current injected: I = 0.1
            
            self.default_reference_node = 15 # the difault id of reference node.
            self.initialized_flag = 0
            
            self.global_matrix = None
            
            self.changed_rou = []

            
            
            
    # initialize the model.
    def set_point_triangle(self):
        """
            Generate the points and triangles and initialize the parameters.
            Including:
                1. Generate the <object>Points  and <object> Triangles.
                2. Get points id List.     --> self.point_id
                3. Get points object List. --> self.point
                4. Get coordinates List.   --> self.coordinate
                5. Get Triangle List.      --> self.triangle
        
        """
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
    
    def model_initialize(self):        
        """Initialize the model prarmeters,
        including:
            Points and Triangles (will not be changed.)
                1> Save Points info: 
                    self.point     
                    self.point_id
                    self.coordinate
                2> Save the Triangles info:
                    self.triangle
                    self.triangle_object
                    (each object including: a, b, c,area and rou.)
        """
        if self.initialized_flag == 0:
            self.set_point_triangle()
            self.generate_triangle_object()
            self.initialized_flag = 1
            return 0
        else:
            print("The model has already initialized!")
            return 1
    
    
    
    # calculate the esm and desm.
    def set_parameters(self):
        """calculate the :
            1> element stiffness matrix
            2> derivative of element stiffness matrix
        """
        for trgo in self.triangle_object:
            trgo.calculate_changed_parameters()

    #calculate the global matrix 
    def get_global_matrix_index(self, n, e):
        """

        :param n: which local id of the point 0, 1, 2 --> 1, 2, 3
        :param e: which element.
        :return: int -->global id
        """
        return self.triangle[e][n]
    
    def calculate_global_matrix(self):
        """
            calculate the global matrix.
            save parameters: 
                    self.global_matrix.
        """
        n_point = len(self.point)
        self.global_matrix = np.zeros((n_point, n_point))
        for e in range(len(self.triangle_object)):
            ke = self.triangle_object[e].ke
            for i in range(3):
                for j in range(3):
                    self.global_matrix[self.get_global_matrix_index(i,e), self.get_global_matrix_index(j,e)] += ke[i, j]

    # YV = b, get Y and b for solving V.
    def get_Y(self, inj_idx, matrix_type=0):
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
            res[self.default_reference_node, :] = 0
            res[:, self.default_reference_node] = 0
            res[self.default_reference_node, self.default_reference_node] = 1
        
        return res
    
    def get_b(self, inj_idx, skip=8):
        """get the currents vector b.

        Args:
            inj_idx (int): the index of reference point.
            skip (int, optional): 
            the distance between injection and out,
                    in adjacent mode, skip = 1,
                    in opposition mode, skip = 8.
                    Defaults to 8.

        Returns:
            numpy ndarray: the currents vector b.
        """ 
        n_point = len(self.point)
        b = np.zeros([n_point, 1])
        b[inj_idx] = self.current
        b[(inj_idx + skip)%16] = - self.current
        return b
        
    # set resistivity method.      
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
    
    def cal_rou_with_del(self,del_rou):
        """add the delta rou into rou.

        Args:
            del_rou (numpy ndarray): the delta rou.
        """
        for i in range(len(del_rou)):
            self.triangle_object[i].rou += del_rou[i]
    
    # Solve the forward: f:R --> V
    def forward(self, inj_idx, rou=None):
        """Solve the forward problem:
        
        Args:
            rou (list/numpy array): the values of resistivities.
            inj_idx (int): the current injection point id(0-16).
        Returns:
            numpy ndarray, numpy ndarray: the voltages of every points in this model.
        """
        # update the rou.
        if rou is not None:
            self.set_all_resistivity(rou)
            
        self.set_parameters() # calculate the esm and desm.
        self.calculate_global_matrix() # calculate the global matrix.
        Y = self.get_Y(inj_idx)
        b = self.get_b(inj_idx)
        
        
        return linalg.solve(Y, b)
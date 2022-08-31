# FEA  v2 $\qquad$$\qquad$

## Entity Class

### 1.创建一个Point实体类，用于实例化每一个point，其中每一个Point包含以下属性： 


+ point_id&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用于保存Point的全局标识符&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;type: int  
+ point_coordinate&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用于保存Point的坐标&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;type: Lsit
+ point_id_in_layer&nbsp;&nbsp;&nbsp;每个节点在该层中的逻辑id&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;type: int

+ 包含以下方法
 * __init__(point_id, point_id_in_layer, point_coordinate)
 * get_coordinate() 返回Point坐标
 * get_x() 返回横坐标
 * get_y() 返回纵坐标
 * get_z() 返回z坐标
 * get_id() 返回全局id
 * get_log_id() 返回Point所在层的逻辑id

### 2.创建一个Triangle实体类，用于保存三角形单元

+ including the following attribute:
 + point(id) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;三角形三个点的编号
  + point1 
  + point2
  + point3
 + coordinate &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;三个点的坐标
  + coordinate1
  + coordinate2
  + coordinate3
  + x1,y1,z1,x2,y2,z2,x3,y3,z3
  
 + parameters 
  + a1,a2,a3,b1,b2,b3,c1,c2,c3
  + rou ($\rho$) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;电阻率
  + ke &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;单元刚度矩阵
  + del_ke &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;单元刚度矩阵的偏导数
  
+ including the following methods
 + __init__(self, triangle, point)
 + calculate_area_2(p1, p2, p3) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;计算三角形面积的二倍
 + calculate_changed_parameters(self) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;计算当前参数下的单元刚度矩阵
  + calculate_element_stiffness_matrix() &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;计算单元刚度矩阵
  + calculate_derivative_element_stiffness_matrix() &nbsp;&nbsp;计算单元刚度矩阵的导数

### 再创建一个Edge实体类，用于实例化每一个edge，其中每一个edge包含以下属性： 

+ edge &nbsp;用于保存边所包含的节点集合&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;type: set
 + edge = set(pt_1, pt_2)
     pt_1 pt_2 均为边所包含的节点id

+ 包含以下方法
 * __init__(pt_1, pt_2)
 * is_equal(edge_target) 判断原边是否与目标边相同 True/False
 * get_point() 返回边中所有节点组成的List

### 然后创建一个FEA模型类，用于实现FEA模型

+ including the following attribute
 + count_layer &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 模型层数
 + model_radius&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 模型半径
 + point_id&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; point id 的list
 + point&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; point list
 + coordinate &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 坐标 list
 + triangle &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 三角形（顶点list）
  + excitation_count&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 激励数
  + current&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 电流值
  + triangle_object &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 三角形对象list
  + triangle_parameters &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 三角形参数list
  
  + golbal_matrix
  + b
  + voltage_matrix
  + del_global_matrix
  + jacobian
  + v0

#### including the following methods

+ set_point_triangle(self)
 + 利用GeneratePointandTriangle 类生成 Points和三角形，并保存：
 -  &nbsp; triangle &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;三角形 List
 -  &nbsp; point    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Point List
 -  &nbsp; corrdinate &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;坐标 List
 -  &nbsp; point_id Point &nbsp;&nbsp;&nbsp;编号 List
<br>from class example \<gpt> of GeneratePointandTriangle:
  + get_triangle_list()
  + get_object_list()
  + get_coordinate_list()
  + get_point_list() 
   
+ generate_triangle_object(self) <br>
 1> calculate a, b, c, area <br>
 2> set default rou <br>
 3> save them in List[t_obj,...].
+ set_parameters(self) <br>
    calculate the :
            1> element stiffness matrix
            2> derivative of element stiffness matrix
+ set_all_resistivity(self, values):
        set resistivity for all elements.
                1> set all elements with a certain number.
                2> set them to different values
        Args:
            values (int/float/list/np.array): modified value(s).
+ get_global_matrix_index(self, n, e)
      return: int -->global id
+ calculate_global_matrix(self):
      calculate the global matrix.
+ calculate_derivative_global_matrix(self):
      calculate the derivative of the global matrix.
+ calculate_modified_matrix(self, reference_index, matrix_type=0):

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
            
+ get_modified_matrix_and_b(self, reference_index, injected_point):

      get the modified global matrix and b.
           
        Args:
            reference_index (_type_): the index of reference point 

        Returns:
            np.ndarray: modified matrix, b
+ calculate_voltage_vector(self, inject_idx=0):
           get the solution of the forward problem:
                1> matrxi of voltage: 37*16 s*p
                2> vector of voltage: vec(V) [37*16] *1

        Args:
            inject_idx (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
+ p_times_observe(self, p=16)
+ calculate_derivative_of_jth_rou(self, j):
        calculate the derivative of the matrix fo jth rou
+ calculate_q(self, v)
        计算Q矩阵
+ testq(self, v)
        用于测试Q矩阵的计算过程
+ calculate_a_column_q(self, v, idx)
        计算一列Q矩阵的结果
+ calculate_a_column_del_f(self, idx)
        计算一列F矩阵导数的结果
+ calculate_all_del_f(self)
        计算整个F矩阵
+ calculate_all_q(self, v)
        用于测试、计算整个Q矩阵
+ generate_v0(self)
        未使用，用于生成带有随机噪声的测量结果
+ model_initialize(self)
        生成模型
+ forward(self, p=16):
        正问题求解过程
+ change_rou(self)
        用于测试，修改部分位置rou的值
+ backward(self)
        逆问题求解

### 生成顶点和三角形的过程

+ class GeneratePointModel

+ class GeneratePointandTriangle

+ class GenerateTriangleModel

### 绘制
+ class DrawModel

- 下图是在两个不懂参考点以及两个不同激励电流位置所得到的边界电压值，其中第三张图标出了增大的电阻位置

![image.png](attachment:image.png)

![image.png](attachment:image.png)

![image.png](attachment:image.png)


```python

```

+ count_layer&nbsp;&nbsp;模型的剖分层数(int)
+ model_radius&nbsp;模型的半径(float)
+ coordinate &nbsp;&nbsp;保存所有点的坐标(list[list[], list[], ...])
+ triangle&nbsp;&nbsp;&nbsp;&nbsp; 保存所有剖分后的三角形(List)  
    
+ 包含以下方法
 * get_layer_radius(self, layer_id) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;layer_id -->  layer_radius
 * get_coordinate(self, point_log_id, layer_id) &nbsp;&nbsp;param --> [x, y, 0]
 * get_triangle_count() &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;model --> the number of triangle  type: int
 * get_model_parameter()&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; model --> model parameters
 * generate_point() &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;model --> generate model point
 * generate_layer_triangle(layer_id) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;layer_id --> generate triangles(layer)
 * generate_triangle() &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;model --> generate all FEA element triangles
 * initialize(self) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;model --> initialized model
 * draw_fea() &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;model --> figure of FEA triangulation

* 包含以下静态方法
 + get_sum_point_count(layer_count) &nbsp;&nbsp; layer_count --> 所有层的节点数目（不包含圆心）
 + get_layer_point_count(layer_id)&nbsp;&nbsp;&nbsp;&nbsp; layer_id&nbsp;&nbsp;&nbsp; --> 该层的节点数目 √
 + generate_element_triangle(point_a, point_b, point_c) param --> triangle (np.ndarray)
 + generate_triangle_in_one_quadrant(type_t, quadrant, current_start_point, previous_start_point, layer_id)  &nbsp;&nbsp;&nbsp;&nbsp;param --> np.ndarray  生成某一层中某一象限的三角形
 + get_several_layers_point_count(layer_n, layer_m) param --> 获得从第n+1层到第m层的节点总数

#### 节点生成

+ generate_point(self)
 * sum_point_count  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;point的总数
 * current_layer &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;遍历过程中当前的层数
 * previous_threshold &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;遍历当前位置所在层的节点总数和之前遍历过所有层的节点总数之和
 * threshold &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;获得包含 Point坐标的模型
 
 
+ 逐层生成节点，从外向内

#### 生成一层中某一个象限的三角形

+ generate_triangle_in_one_quadrant(type_t, quadrant, current_start_point, previous_start_point, layer_id)
 * type_t:     &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;which type of triangle to generate &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;values = 1, 2
 * quadrant: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;from which quadrant &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;values = 1, 2, 3, 4
 * current_start_point:  &nbsp; &nbsp;the first point in this layer (rightmost point on the X-axis)
 * previous_start_point:&nbsp;&nbsp;&nbsp;the first point in previous layer
 

#### 生成一层的三角形

+ generate_layer_triangle(layer_id)
 * layer_id 生成三角形的层号

+ result:


![1657246196131.png](attachment:1657246196131.png)

#### 生成所有的三角形 & 初始化模型 & 绘制figure

+ generate_triangle()
+ initialize()
+ draw_fea()

### v1 生成的结果

![image.png](attachment:image.png)

### v2 生成的结果

![image.png](attachment:image.png)

#### 计算总体刚度矩阵

+ calculate_global_matrix()

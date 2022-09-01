
# EIT Model  

## Entity Class

### 1. Create an entity Class of Point 

+ including following attributes.

|attribute name|description| type|
|:-----------: | :-------: | :-: |
| point_id | save the golbal identifier| int|
|point_coordinate|save the coordinate| List|
|point_id_in_layer|save the logical id in a certain layer| int|


+ inclduing following methods.

|method name|description| 
|:-----------: | :-------: |
|\_\_init__| init| 
|get_coordinate| returns the coordinate of a certain point|
|get_x |returns the abscissa|
|get_y |returns the ordinate|
|get_z |returns the z-axis coordinate|
|get_id|returns the global id|
|get_log_id|returns the logical id in a certain layer|


### 2. Create a entity class of Triangle to save the triangle elements


+ including the following attribute:
<h4></h4>   <!--标题-->
<table border="1" width="500px" cellspacing="10">
<tr>
    <th align="left">attribute name</th>
    <th align="center">description</th>
    <th align="right">type</th>
</tr>
<tr>
    <td colspan="3" align="center">Point information</td>
</tr>
<tr>
    <td>point1</td>
    <td rowspan="3">the global id of 3 points</td>
    <td rowspan="3"> &ltclass&gt Point</td>
</tr>
<tr>
    <td>point2</td>
</tr>
<tr>
    <td>point3</td>
</tr>
<tr>
    <td>coordinate1</td>
    <td rowspan="3">the coordinate of 3 points</td>
    <td rowspan="3">List [x: float, y: float, z: float]</td>
</tr>
<tr>
  <td>coordinate2</td>
</tr>
<tr>
  <td>coordinate3</td>
</tr>
<tr>
    <td>x<sub>1</sub> y<sub>1</sub> z<sub>1</sub></td>
    <td rowspan="3">the coordinates representerd in number</td>
    <td rowspan="3"> float</td>
</tr>
<tr>
    <td>x<sub>2</sub> y<sub>2</sub> z<sub>2</sub></td>
</tr>
<tr>
    <td>x<sub>3</sub> y<sub>3</sub> z<sub>3</sub></td>
</tr>
<tr>
    <td colspan="3" align="center">Triangle parameters</td>
</tr>
<tr>
    <td>a<sub>1</sub> b<sub>1</sub> c<sub>1</sub></td>
    <td rowspan="3">the parameters for calculating element stiffness matrix</td>
    <td rowspan="3"> float</td>
</tr>
<tr>
    <td>a<sub>2</sub> b<sub>2</sub> c<sub>2</sub></td>
</tr>
<tr>
    <td>a<sub>3</sub> b<sub>3</sub> c<sub>3</sub></td>
</tr>
<tr>
  <td>rou</td>
  <td>the resistivity</td>
  <td>float</td>
</tr>
<tr>
  <td>ke</td>
  <td>the element stiffness matrix of a certain triangle element</td>
  <td>float</td>
</tr>
<tr>
  <td>del_ke</td>
  <td>the derivative of element stiffness matrix of a certain triangle element with respect to its resistivity</td>
  <td>float</td>
</tr>

</table>
<!--在表格td中，有两个属性控制居中显示
	align——表示左右居中——left，center，right
	valign——控制上下居中——left，center，right
	width——控制单元格宽度，单位像素
	cellspacing——单元格之间的间隔，单位像素
-->
  
+ including the following methods

|method name|description| 
|:-----------| :-------: |
|\_\_init__| initialize| 
|calculate_area_2| calculate twice the area of a triangle|
|calculate_changed_parameters<br> &nbsp;&nbsp;including:<br> 1.&nbsp;calculate_element_stiffness_matrix<br> 2.&nbsp;calculate_derivative_element_stiffness_matrix |calculate the ke and the derivative of ke based on current parameters|

 

### Create an entity class of Edge to instantiate every edges
+ including the following attributes： 

|attribute name|description| type|
|:-----------: | :------- | :- |
| edge<br><br>Note: edge = set(pt_1, pt_2) | save the points set contained by a certain edge<br><br>pt_1 pt_2 is the global id of the points|set<br><br>|



+ including the following methods

|method name|description| 
|:-----------: | :-------: |
|\_\_init__| init| 
|is_equal| returns True if the target edge contains the same points with the original edge, else return False|
|get_point| return the points list contained by a certain edge.


## Model class: Create an EIT model to implement the EIT model

+ ### including the following attribute

|attribute name|description| type|
|:-----------: | :------- | :- |
| count_layer|the total number of layers| int|
|model_radius|theradius of the model|float|
|point_id|the list of points' id|list [int, ...]|
|point|the list of point's objects|list [Point, ...]|
|coordinate|the list of the coordinates of every point|list [list, ...]|
|triangle|the list of the triangles [p1, p2, p3]|list|
|triangle_object|the list of the triangle's objects|list [Triangle, ...]|
|current|the intensity of electric current|float|
|default_reference_node|the default reference node id|int|
|initialized_flag|1 if the model is initialized<br> 0 for not.| int(0,1)|
|global_matrix|save the original global stiffness matrix|numpy ndarray|
|changed_rou|save the rou in every iterations|list|

+ ### including the following methods
<table border="1" cellspacing="10">
<tr>
    <th align="left">function name</th>
    <th align="center">description</th>
    <th align="right">return data</th>
    <th align="left">save and set data</th>
</tr>
<tr>
    <td>set_point_triangle</td>
    <td>Generate the points andtriangles<br>using the example (gpt) of &ltclass&gtGeneratePointandTriangle</td>
    <td>1.&nbsp;triangle<br>2.&nbsp;point<br>3.&nbsp;coordinate<br>4.&nbsp;point_id </td>
    <td></td>
</tr>
<tr>
    <td>generate_triangle_object</td>
    <td>implements the triangles object from &ltclass&gtTriangle</td>
    <td>triangle_objecte</td>
    <td></td>
</tr>
<tr>
    <td>model_initialize</td>
    <td>Initialize the model prarmeters, including<br>&nbsp;&nbsp;1.&nbsp;Save points information<br>&nbsp;&nbsp;1.&nbsp;Save triangles information</td>
    <td>1: if the model has already initialized<br>0: ininialized successfully.</td>
    <td></td>
</tr>
<tr>
    <td>set_parameters</td>
    <td>set parameters of every triangles.<br>including<br>&nbsp;&nbsp;1.&nbsp;calculate element stiffness matrix for every triangles.<br>&nbsp;&nbsp;2.&nbsp;calculate derivate of element stiffness matrix.</td>
    <td></td>
    <td>1.&nbsp;element stiffness matrix<br>2.&nbsp;derivate of element stiffness matrix</td>
</tr>
<tr>
    <td>get_global_matrix_index:
</td>
    <td>get the index of global stiffness matrix for every  elements in every elements stiffness matrixs</td>
    <td>index of the global matrix for a certain element</td>
    <td></td>
</tr>
<tr>
    <td>calculate_global_matrix</td>
    <td>calculate the global stiffness matrix.</td>
    <td></td>
    <td>global matrix</td>
</tr>
<tr>
    <td>get_Y</td>
    <td>
        modify the global matrix adding the boundary codition.
    </td>
    <td>modified matrix</td>
    <td></td>
</tr>
<tr>
    <td>get_b</td>
    <td>get the currents vector b.</td>
    <td>>vector (b)</td>
    <td</td>
</tr>
<tr>
    <td>set_all_resistivity</td>
    <td>
        set resistivity for all elements in two different ways.
        <br>&nbsp;&nbsp;1> set all elements with a certain number.
        <br>&nbsp;&nbsp;2> set them to different values
    </td>
    <td></td>
    <td>triangle.rou</td>
</tr>
<tr>
    <td>cal_rou_with_del</td>
    <td>add the delta rou into rou.</td>
    <td></td>
    <td>triangle.rou</td>
</tr>
<tr>
    <td>forward</td>
    <td>Solve the forward problem</td>
    <td>voltages(solved by YV=b)</td>
    <td></td>
</tr>
<tr>
    <td>p_times_observe</td>
    <td>p times observe.(default: p = 6)</td>
    <td>
        voltage_matrix
        <br>voltage_vector
    </td>
    <td></td>
</tr>
<tr>
    <td>change_rou</td>
    <td>change values of a certain location rou.</td>
    <td></td>
    <td>triangle.rou</td>
</tr>
<tr>
    <td>rechange_rou</td>
    <td>Restore the values of a certain location rou.</td>
    <td></td>
    <td>triangle.rou</td>
</tr>
<tr>
    <td>get_v0</td>
    <td>get the voltages matrix and vector with a certain changed of rou.</td>
    <td>
        v0_matrix
        <br>v0_vector
    </td>
    <td></td>
</tr>
<tr>
    <td>get_derivative_of_Y_to_eth_rou</td>
    <td>calculate the derivative of the global matrix.</td>
    <td>del_Y</td>
    <td></td>
</tr>
<tr>
    <td>get_a_column_Q</td>
    <td>get jth column of matrix Q.</td>
    <td>q_column</td>
    <td></td>
</tr>
<tr>
    <td>get_matrix_Q</td>
    <td>Get matrix Q under a certain number of projection angles.</td>
    <td>matrix_Q</td>
    <td></td>
</tr>
<tr>
    <td>get_matrix_f_and_del</td>
    <td>get the matrix f and it derivative.</td>
    <td>
        matrix_f
        <br>matrix_del_f
    </td>
    <td></td>
    
</tr>
<tr>
    <td>backward</td>
    <td>Solving the inverse problem.</td>
    <td></td>
    <td></td>
</tr>
<tr>
    <td>print_rou</td>
    <td>print the list of all rou of every elements.</td>
    <td></td>
    <td>update rou.</td>
</tr>
<tr>
    <td>save_rou</td>
    <td>Save the rou of every elements in every iterations.</td>
    <td></td>
    <td>changed_rou</td>
</tr>
<tr>
    <td>run</td>
    <td>run the model with 3 parameters:
        <br>&nbsp;count_layer = 3
        <br>&nbsp;model_radius: 2 
        <br>&nbsp;defalut: rou = 2
    </td>
    <td></td>
    <td></td>
</tr>
<tr>
    <td>model_draw</td>
    <td>
        draw the model.
        <br>showing the resistivitie of every elements using different color.
    </td>
    <td></td>
    <td></td>
</tr>

<tr>
    <td>model_draw_test1</td>
    <td>Because the variation of color is not obvious in the figure, I'd like to use nonlinear RGB values to show resistivities. </td>
    <td></td>
    <td></td>
</tr>

</table>



GeneratePointandTriangle:
  + get_triangle_list()
  + get_object_list()
  + get_coordinate_list()
  + get_point_list() 
   
+  <br>
 1> calculate a, b, c, area <br>
 2> set default rou <br>
 3> save them in List[t_obj,...].



### 生成顶点和三角形的过程

+ class GeneratePointModel

+ class GeneratePointandTriangle

+ class GenerateTriangleModel

### 绘制
+ class DrawModel




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

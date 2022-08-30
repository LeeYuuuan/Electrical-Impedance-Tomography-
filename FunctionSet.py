import numpy as np
import matplotlib.pyplot as plt

def get_sum_point_count(layer_count: int) -> int:
    """

    :return: get the sum number of the points in all layers (with out the zero layer which has only one point [0,0,0])
    """
    if layer_count == 0:
        return 1
    else:
        return 6 * layer_count + 2 * layer_count * layer_count
    
def get_layer_point_count(layer_id: int) -> int:
    """
    get the count number of the points in its layer
    获得第layer_number 层的节点总数
    :param layer_id: which layer the point count of to return
    :return: the point count of this layer
    """
    if layer_id == 0:
        return 1
    return 8 + 4 * (layer_id - 1)

def generate_element_triangle(point_a: int, point_b: int, point_c: int) ->np.ndarray:
    """
    Get a triangle element
    :param point_a: Point id of A
    :param point_b: Point id of B
    :param point_c: Point id of C
    :return: np.ndarray [A, b, C]
    
    NOTE: A B C Counterclockwise
    """
    triangle = np.ndarray([1, 3], dtype="uint64")
    triangle[0, 0] = point_a
    triangle[0, 1] = point_b
    triangle[0, 2] = point_c
    return triangle

def get_several_layers_point_count(layer_n, layer_m):
    """
    获得从第n+1层到第m层的节点总数
    :param layer_n: 第n层的编号
    :param layer_m: 第m层编号
    :return: 节点总数
    """
    count = 0
    if layer_n >= layer_m:
        return 0
    elif layer_n < layer_m:
        for ly in range(layer_n + 1, layer_m + 1):
            count += get_layer_point_count(ly)

    return count



def generate_triangle_in_one_quadrant(type_t, quadrant, current_start_point, previous_start_point, layer_id):
    """
    generate triangles in certain layer from a certain quadrant
    生成一层中某一象限的三角形
    :param type_t: which type of triangle to generate values = 1, 2
    :param quadrant: from which quadrant values = 1, 2, 3, 4
    :param current_start_point: the first point in this layer (rightmost point on the X-axis)
    :param previous_start_point: the first point in previous layer
    :param layer_id: in which layer
    :return: np.ndarray n*3
    """
    point_count = int(get_layer_point_count(layer_id) / 4)

    if layer_id == 1:
        point_a = current_start_point.get_id()
        point_b = point_a + 1
        point_c = previous_start_point.get_id()
        triangle = generate_element_triangle(point_a, point_b, point_c)
        for i in range(1, 7):
            triangle = np.concatenate((triangle, generate_element_triangle(point_a + i, point_b + i, point_c)), axis=0)
        triangle = np.concatenate((triangle, generate_element_triangle(point_a, point_a + 7, point_c)), axis=0)
        return triangle

    if current_start_point.get_log_id() == 0 and type_t == 1:
        point_a = current_start_point.get_id() + (quadrant - 1) * point_count
        point_b = point_a + 1
        point_c = previous_start_point.get_id() + (quadrant - 1) * (point_count - 1)
        triangle = generate_element_triangle(point_a, point_b, point_c)
        tg_temp = np.ndarray([1, 3], dtype="uint64")

        for i in range(1, point_count - 1):
            tg_temp[0, 0] = point_a + i
            tg_temp[0, 1] = point_b + i
            tg_temp[0, 2] = point_c + i
            triangle = np.concatenate((triangle, tg_temp), axis=0)
        if quadrant in [1, 2, 3]:
            tg_temp[0, 0] = point_a + point_count - 1
            tg_temp[0, 1] = point_b + point_count - 1
            tg_temp[0, 2] = point_c + point_count - 1
            triangle = np.concatenate((triangle, tg_temp), axis=0)
            return triangle
        if quadrant == 4:
            tg_temp[0, 0] = current_start_point.get_id()
            tg_temp[0, 1] = point_a + point_count - 1
            tg_temp[0, 2] = previous_start_point.get_id()

            triangle = np.concatenate((triangle, tg_temp), axis=0)
            return triangle

    if current_start_point.get_log_id() == 0 and type_t == 2:
        point_a = previous_start_point.get_id() + (quadrant - 1) * (point_count - 1)
        point_b = point_a + 1
        point_c = current_start_point.get_id() + 1 + (quadrant - 1) * point_count

        triangle = generate_element_triangle(point_a, point_b, point_c)
        tg_temp = np.ndarray([1, 3], dtype="uint64")
        for i in range(1, point_count - 2):
            tg_temp[0, 0] = point_a + i
            tg_temp[0, 1] = point_b + i
            tg_temp[0, 2] = point_c + i
            triangle = np.concatenate((triangle, tg_temp), axis=0)
        if quadrant in [1, 2, 3]:
            tg_temp[0, 0] = point_a + point_count - 2
            tg_temp[0, 1] = point_b + point_count - 2
            tg_temp[0, 2] = point_c + point_count - 2
            triangle = np.concatenate((triangle, tg_temp), axis=0)
            return triangle
        if quadrant == 4:
            tg_temp[0, 0] = point_a + point_count - 2
            tg_temp[0, 1] = previous_start_point.get_id()
            tg_temp[0, 2] = point_c + point_count - 2
            triangle = np.concatenate((triangle, tg_temp), axis=0)
            return triangle


def get_matrix_t(point_count):
    tran = np.zeros([12*16, point_count*16], dtype=int)
    count = 0
    for i in range(16):

        for pivot in range(16):
            pivot_next = (pivot + 1) % 16
            if (pivot % 4 ==0 or pivot_next % 4 == 0):
                if (pivot % 8 ==0 or pivot_next % 8 == 0):
                    tran[count, i * point_count + pivot]+= 1
                    tran[count, i * point_count + pivot_next] += -1
                    count += 1
                    
            else:
                tran[count, i * point_count + pivot]+= 1
                tran[count, i * point_count + pivot_next] += -1
                    
                count += 1
    return tran
                

def generate_matrix_t():
    tran = np.zeros([12*16, 37*16], dtype=int)
    count = 0
    for inj in range(16):
        
        for obs in range(16):
            if (obs - inj) % 4 != 0:
                tran[count, obs + 37 * inj] = 1
                count += 1
    return tran

def draw_bar(data):
    """Draw the bar figure for a certain data.

    Args:
        data (List/nunpy ndarray): the data.
    """
    plt.bar(list(range(len(data))), data, width=0.6)
    plt.show()

def get_matrix_T():
    """get matrix T

    Returns:
        numpy ndarray: matrix T.
    """
    pass
    #return matrix_T


if __name__ =="__main__":
    print(generate_matrix_t().shape)
    for i in range(50):
       # print(generate_matrix_t()[i])
       pass
            


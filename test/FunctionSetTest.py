from FunctionSet import *

def test_get_sum_point_count():
    print("===============test_get_sum_point_count===============")
    for i in range(4):
        
        print("sum point count for ", i, " layers:", get_sum_point_count(i))
    print("======================================================")
    print()

def test_generate_element_triangle():
    print("==========test_generate_element_triangl==========")
    print("triangle: ",generate_element_triangle(1, 2, 3))
    print("=================================================")
    print()

def test_get_several_layers_point_count():
    print("========test_get_several_layers_point_count========")
    for i in range(4):
        for j in range(i, 4):
            print("the count of point in ", i, "to", j, "layers:", get_several_layers_point_count(i, j))
    print("===================================================")
    print()
    
def test_get_matrix_t():
    print("========test_get_matrix_t========")
    print(get_matrix_t(36).shape)
    print("================================")
    
test_get_sum_point_count()
test_generate_element_triangle()
test_get_several_layers_point_count()
test_get_matrix_t()

    
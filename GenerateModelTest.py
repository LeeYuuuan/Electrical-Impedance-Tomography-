
from GenerateModel import *
import matplotlib.pyplot as plt
def test_forward():
    """test if the forward function can 
        return the right voltage matrix
        after change the rou.
    """
    fea = FEAModel()
    fea.model_initialize()

    fea.change_rou()
    
    matrix, vector = fea.forward()

    plt.bar(list(range(16)), matrix[0:16,1], width=0.6)
    plt.show()
    print(matrix)
    fea.model_draw()
    
    fea.rechange_rou()
    
    matrix, vector = fea.forward()

    plt.bar(list(range(16)), matrix[0:16][1], width=0.6)
    plt.show()
    print(matrix)
    fea.model_draw()
    print(matrix.shape)
    print(matrix[0:16][1].shape)


def test_backword():
    fea = FEAModel()
    fea.model_initialize()
    fea.backword()

def test_del_jth_rou_Y():
    fea = FEAModel()
    fea.model_initialize()
    fea.forward()
    #print(fea.calculate_derivate_of_Y_to_jth_rou(0))
    #print(fea.triangle[0])
    #print(fea.triangle_object[0].del_ke)
    #print(fea.global_matrix)
    from scipy import linalg
    L = np.linalg.cholesky(fea.global_matrix)
    LT = L.T
    print(np.linalg.inv(LT) @ np.linalg.inv(L) @ fea.global_matrix)
    #print(fea.global_matrix @ linalg.pinv(fea.global_matrix))
    
if __name__ == "__main__":
    
    test_forward()
    
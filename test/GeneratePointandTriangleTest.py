
from GeneratePointandTriangle import *

def test_GeneratePointandTriangle():
    gpt = GeneratePointandTriangle(3, 2)
    gpt.initialize_parameters()
    
    gpt.draw_pic()
    print(gpt.triangle)
    

#test_GeneratePointandTriangle()
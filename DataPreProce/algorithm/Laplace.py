'''
    Implementation of Laplace operator
'''
import numpy as np


def Laplace_operator(data):
    '''
        Laplace arithmetic implementation
    '''
   
    laplace = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    high, wide = data.shape
    data_extension = np.zeros((high+2, wide+2))
    result = np.zeros((high, wide))
    ## Copy the old data to the expanded new data
    data_extension[1:high+1, 1:wide+1] = data
    ## laplace Convolution operation
    for i in range(1,high+1):
        for j in range(1,wide+1):
            result[i-1, j-1] = np.abs(np.sum(np.multiply(data_extension[i-1:i+2, j-1:j+2], laplace)))
    return result

if __name__ == "__main__":
    data = np.arange(100).reshape(10,10)
    result = Laplace_operator(data)
    # print(result)
    
    

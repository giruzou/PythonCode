#NNetwork
#Author S.Terasaki
#Data 20.7.2016 
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1.0/(1+np.exp(-x))

def step_func(x):
    if x>0:
        return 1
    else:
        return 0

def identity_func(x):
    return x

class Layer():
    """
    func is activating funciton
    weight is weight vector its type is supposed to be np.array
    bias is bias its type is supposed to benp.array
    """
    alpha=0.01
    def __init__(self,func,weight,bias):
        self.f=func
        self.w=weight
        self.b=bias
    def set_unit_value(self,u):
        self.u=u        
    def pass_next_layer(self):
        return self.f(self.w.dot(self.u)+self.b)
    def _upd_w(self,w):
        self.w=w
    def _upd_b(self,b):
        self.b=b
    def __str__(self):
        return "w=\n%s\nb=\n%s"%(self.w,self.b)
        
class NNetwork():        
    pass
            
def prepare_test_param():
    w=np.array(([0,-1,1],
                [1,0,1],
                [0,0,1]))
    #set b and x as column vector
    b=np.array([1,
                1,
                1]).reshape((-1,1))
    x=np.array([1,
                0,
                -1]).reshape((-1,1))
    return w,b,x
    
def prepare_input_param():
    w,b,input_value=prepare_input_param()
    print('input_value\n %s'%input_value)
    input_layer=Layer(identity_func,w,b)
    print(input_layer)
    input_layer.set_unit_value(input_value)
    print("nextlay=\n%s"%input_layer.pass_next_layer())
    return input_layer    
    
def prepare_random_param():
    
    #make 3 by 3 matrix
    w=np.random.rand(3,3)
    #make column vector
    b=np.random.rand(3,1)
    #initialize input value
    x=np.random.rand(3,1)
    return w,b,x

def prepare_input_layer():
    #3 by 3 identity matrix
    w=np.identity(3)
    #3 by 1 zero vector  
    b=np.zeros(3:1) 
    #create 3 by 1 vector
    x=np.array([1,
                0,
                -1]).reshape((-1,1))
    return w,b,x

def prepare_mediant_layer():
    print('start\n')
    w,b,input_value=prepare_test_param()
    print('input_value\n %s'%input_value)
    mediant_layer=Layer(identity_func,w,b)
    print(input_layer)
    mediant_layer.set_unit_value(input_value)
    print("nextlay=\n%s"%mediant_layer.pass_next_layer())
    return mediant_layer

def main():
    prepare_input_layer()
if __name__=='__main__':
    main()
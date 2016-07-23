#NNetwork
#Author S.Terasaki
#Data 20.7.2016 
import numpy as np
import matplotlib.pyplot as plt

def differential(f,a):
    return (f(a+h)-f(a))/h

def test_get_local_minimum(f,init_pt):
    plt.plot(init_pt,f(init_pt),"bo")
    xs=[]
    x_old=init_pt
    xs.append(init_pt)
    for i in range(100):
        x_new=x_old-epsilon * differential(f,x_old)
        print(x_new)
        xs.append(x_new) 
        #update x
        x_old=x_new
    plt.plot(xs,map(f,xs))
    plt.plot(xs,map(f,xs),"g*")
    plt.xlim(-np.pi,np.pi)
    plt.ylim(-1.5,1.5)
    xs_f=np.arange(-np.pi,np.pi,0.01)
    ys_f=map(f,xs_f)
    plt.plot(xs_f,ys_f)
    plt.plot(x_new,f(x_new),"ro")
    plt.show()

def sigmoid(x):
    return 1.0/(1+np.exp(-x))
#usage for ndarray of numpy :print(np.vectorize(step_func)(np.array([-1,0,1])))
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
    def set_unit(self,u):
        self.u=u      
    def set_unit_from_previous_layer(self,u):
        self.u=self.w.dot(u)+self.b  
    def pass_next_layer(self):
        #activate unit
        return self.f(self.u)
    def get_w(self):
        return self.w
    def get_b(self):
        return self.b
    def get_u(self):
        return self.u
    def _upd_w(self,w):
        self.w=w
    def _upd_b(self,b):
        self.b=b
    def __str__(self):
        return "w=\n%s\nb=\n%s\nu=\n%s\nf(u)=\n%s\n"%(self.w,self.b,self.u,self.f(self.u))
        
class NNetwork():        
    def __init__(self,layers):
        self.layers=layers
    def _register_weights(self):
        self.ws=[lay.get_w for lay in self.layers]
    def _register_bias(self):
        self.bs=[lay.get_b for lay in self.layers]

def prepare_input_param():
    #3 by 3 identity matrix
    w=np.identity(3)
    #3 by 1 zero vector  
    b=np.zeros([3,1]) 
    return w,b,identity_func    

def prepare_mediant_param():
    w=np.array(([0,-1,1],
                [1,0,1],
                [0,0,1]))
    #set b and x as column vector
    b=np.array([1,
                1,
                1]).reshape((-1,1))
    return w,b,sigmoid
        
def prepare_mediant_param_random():
    
    #make 3 by 3 matrix
    w=np.random.rand(3,3)
    #make column vector
    b=np.random.rand(3,1)
    #initialize input value
    return w,b,sigmoid

def prepare_output_param():
    w=np.array(([0,-1,1],
                [1,0,1],
                [0,0,1]))
    #set b and x as column vector
    b=np.array([1,
                1,
                1]).reshape((-1,1))
    return w,b,sigmoid

def prepare_input_layer():
    w,b,id_func=prepare_input_param()
    input_layer=Layer(id_func,w,b)
    return  input_layer

def prepare_mediant_layer(input_layer):
    w,b,sig=prepare_mediant_param()
    mediant_layer=Layer(sig,w,b)
    mediant_layer.set_unit_from_previous_layer(input_layer.pass_next_layer())
    return mediant_layer

def prepare_output_layer(mediant_layer):
    w,b,sig=prepare_output_param()
    output_layer=Layer(sig,w,b)
    output_layer.set_unit_from_previous_layer(mediant_layer.pass_next_layer())
    return output_layer

def network_output(x):
    input_layer=prepare_input_layer()
    input_layer.set_unit(x)
    print("input_layer=\n%s"%input_layer)
    mediant_layer=prepare_mediant_layer(input_layer)
    print("mediant_layer=\n%s"%mediant_layer)
    output_layer=prepare_output_layer(mediant_layer)
    print("output_layer=\n%s"%output_layer)
    return output_layer.pass_next_layer()

def get_square_error(input_value,teaching_set):
    return np.sum((network_output(input_value)-teaching_set)**2)/2.0

def main():
    #create 3 by 1 vector
    input_value=(np.array([1,
                           2,
                           3]).reshape((-1,1)))
    teaching_set=(np.array([0,
                            0,
                            1]).reshape((-1,1)))
    output_value=network_output(input_value)
    print("output_value=\n%s"%output_value)               
    print("square error=\n%s"%get_square_error(input_value,teaching_set))
    
def diff_square_error(layer_index,unit_index):
    pass

if __name__=='__main__':
    main()
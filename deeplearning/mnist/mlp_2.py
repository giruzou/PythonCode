
__author__="SatoshiTerasaki<terasakisatoshi.math@gmai.com"
__date__='2017/05/05'

import numpy as np 
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.datasets import fetch_mldata

#functions
def sigmoid(x):
    return 1/(1+np.exp(-x))

def deriv_sigmoid(x):
    return sigmoid(x) * (1-sigmoid(x))

def softmax(xs):
    """
    calc softmax function
    note that np.sum(arr,axis=1,keepdims=True) behaves as follow:
    >>> mat=np.arange(12).reshape(3,4)
    >>> mat
    >>> array([[0,1,2,3],
               [4,5,6,7],
               [8,9,10,11]])
    >>> np.sum(mat,axis=1,keepdims=True)
    >>> array([ 6],
              [22],
              [38])
    """
    exp_x=np.exp(xs)
    if exp_x.ndim<=1:
        return exp_x/np.sum(exp_x,keepdims=True)
    else:
        return exp_x/np.sum(exp_x,axis=1,keepdims=True)

def cross_entropy_error(y, t):
    """
    reference Deep Learning From Scratch
    https://github.com/oreilly-japan/deep-learning-from-scratch
    """
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
        
    # 教師データがone-hot-vectorの場合、正解ラベルのインデックスに変換
    if t.size == y.size:
        t = t.argmax(axis=1)
             
    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t])) / batch_size

def numerical_gradient(f, x):
    """
    reference Deep Learning From Scratch
    https://github.com/oreilly-japan/deep-learning-from-scratch
    """
    h = 1e-4 # 0.0001
    grad = np.zeros_like(x)
    
    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:
        idx = it.multi_index
        tmp_val = x[idx]
        x[idx] = float(tmp_val) + h
        fxh1 = f(x) # f(x+h)
        
        x[idx] = tmp_val - h 
        fxh2 = f(x) # f(x-h)
        grad[idx] = (fxh1 - fxh2) / (2*h)
        
        x[idx] = tmp_val # 値を元に戻す
        it.iternext()   
        
    return grad


#create dataset 
def get_mnist_data():
    """
    load data on your directry ~/scikit_learn_data/mldata/
    if data does'nt exist, it downloads the data from site.
    """
    mnist=fetch_mldata('MNIST original')
    return mnist

def divide_mnist_data(mnist=None):
    """
    load mnist dataset
    input:None
    output:split these data into train valid and test data.
    """
    if not mnist:
        mnist=get_mnist_data()

    mnist_X,mnist_y=shuffle(mnist.data,mnist.target, random_state=42)
    #normalize
    mnist_X=mnist_X/255.0
    train_X, test_X, train_y, test_y = train_test_split(mnist_X, mnist_y,
                                                        test_size=0.2,
                                                        random_state=42)
    #choose valid data from <test_size> % of train set
    train_X, valid_X, train_y, valid_y = train_test_split(train_X, train_y,
                                                          test_size=0.2,
                                                          random_state=42)

    return train_X,valid_X,test_X,train_y,valid_y,test_y

class MultiPerceptron(object):
    def __init__(self):
        in_size=28*28
        hidden_size=40
        out_size=10
        self.parameters={}
        # Layer1 weights
        W1 = np.random.uniform(low=-0.08, high=0.08, size=(in_size, hidden_size)).astype('float32')
        b1 = np.zeros(hidden_size).astype('float32')
        # Layer2 weights
        W2 = np.random.uniform(low=-0.08, high=0.08, size=(hidden_size, out_size)).astype('float32')
        b2 = np.zeros(out_size).astype('float32')

        for key,value in locals().items():
            self.parameters[key]=value

    def check_parameters(self):
        for key,value in self.parameters.items():
            print('key=',key)
            print('value=',value)
    def __call__(self,xs=None):
        if xs==None:
            self.check_parameters()
        else:
            ys=self.predict(xs)
            return ys

    def predict(self,xs):
        W1,W2=self.parameters['W1'],self.parameters['W2']
        b1,b2=self.parameters['b1'],self.parameters['b2']
        z0=xs
        u1=np.matmul(z0,W1)+b1
        z1=sigmoid(u1)
        u2=np.matmul(z1,W2)+b2
        z2=sigmoid(u2)
        ys=softmax(z2)
        return ys

    def evaluate(self,xs,ts):
        ys=self.predict(xs)
        print(ys-ts)

    def loss(self,xs,ts):
        ys=self.predict(xs)
        return cross_entropy_error(ys,ts)

    def calc_grads(self,xs,ts):
        loss_fun = lambda W : self.loss(xs,ts)

        grads={}
        grads['W1']=numerical_gradient(loss_fun,self.parameters['W1'])
        grads['b1']=numerical_gradient(loss_fun,self.parameters['b1'])
        grads['W2']=numerical_gradient(loss_fun,self.parameters['W2'])
        grads['b2']=numerical_gradient(loss_fun,self.parameters['b2'])

        return grads

        
def convert_teach_vector(ts):
    label_list=np.identity(10)
    return [label_list[t] for t in list(map(int,ts))]

def _main():
    network=MultiPerceptron()
    #show init parameters
    #network()
    #get data
    mnist=get_mnist_data()
    train_X,valid_X,test_X,train_y,valid_y,test_y=divide_mnist_data()
    result=train_y[1:10]

    print(result)
    print(convert_teach_vector(result))

def main():
    network=MultiPerceptron()
    #show init parameters
    #network()
    #get data
    mnist=get_mnist_data()
    train_X,valid_X,test_X,train_y,valid_y,test_y=divide_mnist_data()

    test=test_X[1:10]
    result=train_y[1:10]

    print(result)
    ts=convert_teach_vector(result)

    print(network.evaluate(test,ts))

if __name__ == '__main__':
    main()
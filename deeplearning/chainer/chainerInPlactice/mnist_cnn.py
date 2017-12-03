import numpy as np 

from chainer import datasets
from chainer import Chain, Variable
from chainer import iterators, optimizers, training
from chainer.training import extensions

import chainer.functions as F 
import chainer.links as L 

class CnnModel(Chain):
    def __init__(self):
        super(CnnModel,self).__init__(
            cn1=L.Convolution2D(1,20,5),
            cn2=L.Convolution2D(20,50,5),
            fc1=L.Linear(800,500),
            fc2=L.Linear(500,10),
        )

    def __call__(self,x,t):
        return F.softmax_cross_entropy(self.fwd(x),t)

    def fwd(self,x):
        h1=F.max_pooling_2d(F.relu(self.cn1(x)),2)
        h2=F.max_pooling_2d(F.relu(self.cn2(h1)),2)
        h3=F.dropout(F.relu(self.fc1(h2)))
        return self.fc2(h3)

def main():
    train, test = datasets.get_mnist(ndim=3)
    model=CnnModel()
    optimizer=optimizers.Adam()
    optimizer.setup(model)
    minibatch_size=1000
    iterator = iterators.SerialIterator(train, minibatch_size)
    updater=training.StandardUpdater(iterator,optimizer)
    loops=(10,'epoch')
    trainer = training.Trainer(updater,loops)
    trainer.extend(extensions.ProgressBar())
    print('start to train')
    trainer.run()
    print('finish to train')

    print("lets predict")
    counter=0
    for t in test:
        img,label=t
        x=Variable(np.array([img]))
        predict = np.argmax(model.fwd(x).data)
        if predict==label:
            counter+=1
    print("done")
    print(counter/len(test))

if __name__ == '__main__':
    main()
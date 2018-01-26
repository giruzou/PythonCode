import chainer
import chainer.functions as F
import chainer.links as L
from chainer import training, datasets, iterators, optimizers
from chainer.training import extensions
import numpy as np

DEVICE = -1
BATCH_SIZE = 10


class MNISTCONV(chainer.Chain):

    def __init__(self):
        super(MNISTCONV, self).__init__()
        with self.init_scope():
            self.c1 = L.Convolution2D(1, 8, ksize=3)
            self.l1 = L.Linear(13*13*8, 10)

    def __call__(self, x, t=None, train=True):
        h1 = self.c1(x)
        h2 = F.relu(h1)
        h3 = F.max_pooling_2d(h2, 2)
        h4 = self.l1(h3)
        if train:
            return F.softmax_cross_entropy(h4, t)
        else:
            return F.softmax(h4)


def train():
    model = MNISTCONV()
    if DEVICE >= 0:
        chainer.cuda.get_device_from_id(DEVICE).use()
        chainer.cuda.check_cuda_available()
        model.to_gpu()
    train, test = chainer.datasets.get_mnist(ndim=3)
    train_iter = iterators.SerialIterator(train, BATCH_SIZE, shuffle=True)
    test_iter = iterators.SerialIterator(test, 1, repeat=False, shuffle=False)

    optimizer = optimizers.Adam()
    optimizer.setup(model)

    updater = training.StandardUpdater(train_iter, optimizer, device=DEVICE)
    trainer = training.Trainer(updater, (5, 'epoch'), out='result')
    trainer.extend(extensions.Evaluator(test_iter, model, device=DEVICE))
    trainer.extend(extensions.ProgressBar())

    trainer.run()

    chainer.serializers.save_hdf5('result/mnistconv.hdf5', model)

def predict():
    model=MNISTCONV()
    chainer.serializers.load_hdf5('result/mnistconv.hdf5',model)
    train, test = chainer.datasets.get_mnist(ndim=3)
    counter=0
    acc=0
    for t in test:
        counter+=1
        x,ans = t
        result=model(np.array([x]),train=False).data[0]
        if ans==np.argmax(result):
            acc+=1
    print(acc/counter)
def main():
    #train()
    predict()
if __name__ == '__main__':
    main()

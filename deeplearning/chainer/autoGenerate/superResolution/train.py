import chainer
import chainer.functions as F
import chainer.links as L
from chainer import training, datasets, iterators, optimizers
from chainer.training import extensions
import numpy as np
from PIL import Image
import os
DEVICE = 0

if DEVICE >= 0:
    import cupy as xp
else:
    xp = np

class SuperResolution(chainer.Chain):
    def __init__(self):
        w1 = chainer.initializers.Normal(scale=0.0378, dtype=None)
        w2 = chainer.initializers.Normal(scale=0.3536, dtype=None)
        w3 = chainer.initializers.Normal(scale=0.1179, dtype=None)
        w4 = chainer.initializers.Normal(scale=0.1890, dtype=None)
        w5 = chainer.initializers.Normal(scale=0.0001, dtype=None)
        super(SuperResolution, self).__init__()
        with self.init_scope():
            self.c1 = L.Convolution2D(
                1, 56, ksize=5, stride=1, pad=0, initialW=w1)
            self.l1 = L.PReLU()
            self.c2 = L.Convolution2D(
                56, 12, ksize=1, stride=1, pad=0, initialW=w2)
            self.l2 = L.PReLU()
            self.c3 = L.Convolution2D(
                12, 12, ksize=3, stride=1, pad=1, initialW=w3)
            self.l3 = L.PReLU()
            self.c4 = L.Convolution2D(
                12, 12, ksize=3, stride=1, pad=1, initialW=w3)
            self.l4 = L.PReLU()
            self.c5 = L.Convolution2D(
                12, 12, ksize=3, stride=1, pad=1, initialW=w3)
            self.l5 = L.PReLU()
            self.c6 = L.Convolution2D(
                12, 12, ksize=3, stride=1, pad=1, initialW=w3)
            self.l6 = L.PReLU()
            self.c7 = L.Convolution2D(
                12, 56, ksize=1, stride=1, pad=1, initialW=w4)
            self.l7 = L.PReLU()
            self.c8 = L.Deconvolution2D(
                56, 1, ksize=9, stride=3, pad=4, initialW=w5)

    def __call__(self, x, t=None, train=True):
        h1 = self.l1(self.c1(x))
        h2 = self.l2(self.c2(h1))
        h3 = self.l3(self.c3(h2))
        h4 = self.l4(self.c4(h3))
        h5 = self.l5(self.c5(h4))
        h6 = self.l6(self.c6(h5))
        h7 = self.l7(self.c7(h6))
        h8 = self.c8(h7)
        if train:
            return F.mean_squared_error(h8, t)
        else:
            return h8


class SRUpdater(training.StandardUpdater):
    def __init__(self, train_iter, optimizer, device):
        super(SRUpdater, self).__init__(
            train_iter,
            optimizer,
            device=device
        )

    def update_core(self):
        batch = self.get_iterator('main').next()
        optimizer = self.get_optimizer('main')
        x_batch = []
        y_batch = []
        for img in batch:
            hpix = np.array(img, dtype=np.float32) / 255.0
            y_batch.append([hpix[:, :, 0]])
            low = img.resize((16, 16), Image.NEAREST)
            lpix = np.array(low, dtype=np.float32) / 255.0
            x_batch.append([lpix[:, :, 0]])
        xs = xp.array(x_batch, dtype=xp.float32)
        ys = xp.array(y_batch, dtype=xp.float32)
        optimizer.update(optimizer.target, xs, ys)


def collect_train_patch(traindir):
    images = []

    fs = os.listdir(traindir)
    for f in fs:
        img = Image.open('train/' + f).resize((320, 320)).convert('YCbCr')
        cur_x = 0
        while cur_x <= 320 - 40:
            cur_y = 0
            while cur_y <= 320 - 40:
                rect = (cur_x, cur_y, cur_x + 40, cur_y + 40)
                cropimg = img.crop(rect).copy()
                images.append(cropimg)
                cur_y += 20
            cur_x += 20
    return images


BATCH_SIZE = 1024
RESUME=True

def train():
    model = SuperResolution()
    if DEVICE >= 0:
        chainer.cuda.get_device_from_id(DEVICE).use()
        chainer.cuda.check_cuda_available()
        print("USEDEVICE", DEVICE)
        model.to_gpu()

    images = collect_train_patch('train')

    train_iter = iterators.SerialIterator(images,  BATCH_SIZE, shuffle=True)
    optimizer = optimizers.Adam()
    optimizer.setup(model)

    updater = SRUpdater(train_iter, optimizer, device=DEVICE)
    snapshot_interval=(500, 'epoch')
    trainer = training.Trainer(updater, (10000, 'epoch'), out='result')
    trainer.extend(extensions.snapshot(
        filename='snapshot_epoch_{.updater.epoch}.npz'),
                   trigger=snapshot_interval)
    trainer.extend(extensions.ProgressBar())
    trainer.extend(extensions.snapshot_object(model,'model_epoch_{.updater.epoch}.npz'), trigger=snapshot_interval)
    if RESUME:
        # Resume from a snapshot
        chainer.serializers.load_npz('result/snapshot_epoch_25.npz', trainer)
    trainer.run()

    chainer.serializers.save_hdf5('model.hdf5', model)


def main():
    train()


if __name__ == '__main__':
    main()

import chainer
from chainer import training
import numpy as np
xp = chainer.cuda.cupy if chainer.cuda.available else np
import chainer.functions as F

class Updater(training.StandardUpdater):

    def __init__(self, train_iter, optimizer, device):
        super(Updater, self).__init__(
            train_iter,
            optimizer,
            device=device)

    def loss_dis(self, dis, y_fake, y_real):
        batchsize = len(y_fake)
        L1 = F.sum(F.softplus(-y_real))/batchsize
        L2 = F.sum(F.softplus(y_fake))/batchsize
        loss = L1+L2
        return loss

    def loss_gen(self, gen, y_fake):
        batchsize = len(y_fake)
        loss = F.sum(F.softplus(-y_fake))/batchsize
        return loss

    def update_core(self):
        batch = self.get_iterator('main').next()
        src = self.converter(batch, self.device)
        optimizer_gen = self.get_optimizer('opt_gen')
        optimizer_dis = self.get_optimizer('opt_dis')
        gen = optimizer_gen.target
        dis = optimizer_dis.target

        rnd = np.random.uniform(-1, 1, (src.shape[0], 100))
        rnd = xp.array(rnd, dtype=xp.float32)
        x_fake = gen(rnd)
        y_fake = dis(x_fake)
        y_real = dis(src)

        optimizer_dis.update(self.loss_dis, dis, y_fake, y_real)
        optimizer_gen.update(self.loss_gen, gen, y_fake)

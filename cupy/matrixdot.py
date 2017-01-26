import numpy as np 
import chainer
from chainer import cuda
import time 
xp=cuda.cupy
from matplotlib import pyplot as plt 

def do_something(n,mat):
	for i in range(n):
		mat=mat.dot(mat)
		mat=mat-mat.dot(mat)

def cpucalc(n):
	start=time.time()
	mat=np.arange(n*n).reshape(n,n)
	do_something(n,mat)
	end=time.time()
	elapsed=end-start
	print("CPU end-start=%s"%elapsed)
	return elapsed

def gpucalc(n):
	start=time.time()
	mat=xp.arange(n*n).reshape(n,n)
	do_something(n,mat)
	end=time.time()
	elapsed=end-start
	print("GPU end-start=%s"%elapsed)
	return elapsed
def main():
	cs=[]
	gs=[]
	iteration=500
	step=50
	for n in range(1,iteration,step):
		print(n)
		gs.append(gpucalc(n))
		cs.append(cpucalc(n))

	fig,ax=plt.subplots()
	ax.plot([i for i in range(1,iteration,step)],gs,color="green")
	ax.plot([i for i in range(1,iteration,step)],cs,color="blue")
	plt.show()

if __name__ == '__main__':
	main()
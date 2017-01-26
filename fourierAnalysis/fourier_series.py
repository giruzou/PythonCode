import numpy as np 
from matplotlib import pyplot as plt 
from scipy import integrate

Pi=np.pi
T=2*Pi
N= 90

naive=None
approx_series=None
explicit_series=None
semi_explicit=None
a_func=None

def getVarName( var, symboltable, error=None ) :
    """
    Return a var's name as a string.\nThis funciton require a symboltable(returned value of globals() or locals()) in the name space where you search the var's name.\nIf you set error='exception', this raise a ValueError when the searching failed.
    """
    for k,v in symboltable.items() :
        if id(v) == id(var) :
            return k
    else :
        if error == "exception" :
            raise ValueError("Undefined function is mixed in subspace?")
        else:
            return error

def step_func(xs):
	return np.where(xs<0,0,1)

def plot_func(funcs):
	fig,ax=plt.subplots()
	for func in funcs:
		xs=np.linspace(-T/2,T/2,100)
		ys=func[0](xs)
		ax.plot(xs,ys,label=func[1])
	ax.legend()
	plt.savefig("fourier.png")

def get_fourier(func):
	ts=np.linspace(-T/2,T/2,1000)
	A0=integrate.simps((lambda t:func(t)/T)(ts),ts) 
	As=np.array([integrate.simps((lambda t:2*func(t)*np.cos(2*n*Pi*t/T)/T)(ts),ts) for n in range(1,N)],dtype=np.float64)
	Bs=np.array([integrate.simps((lambda t:2*func(t)*np.sin(2*n*Pi*t/T)/T)(ts),ts) for n in range(1,N)],dtype=np.float64)
	Explicit_Bs=np.array([(1-(-1)**n)/(n*Pi) for n in range(1,N)])
	print(Explicit_Bs)
	cos_part=lambda t : np.array([np.cos(2*n*Pi*t/T) for n in range(1,N)],dtype=np.float64)
	sin_part=lambda t : np.array([np.sin(2*n*Pi*t/T) for n in range(1,N)],dtype=np.float64)

	global naive,approx_series,explicit_series,semi_explicit,a_func
	naive=lambda t: A0+As.dot(cos_part(t))+Bs.dot(sin_part(t))
	approx_series=lambda t: A0+Bs.dot(sin_part(t))
	semi_explicit=lambda t: A0+Explicit_Bs.dot(sin_part(t))

	explicit_series=lambda t: 1/2 + sum([2*np.sin((2*m-1)*t)/((2*m-1)*Pi) for m in range(1,N)])
	a_func=lambda t:As.dot(cos_part(t))
	plot_func((func,getVarName(func,globals())) for func in [step_func,naive,approx_series,explicit_series,semi_explicit,a_func])

def main():
	get_fourier(step_func)
if __name__ == '__main__':
	main()
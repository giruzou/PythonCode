import numpy as np 


def solveeq_gauss(a,b,x):
    """
    solve equation ax=b using simple gauss method
    """
    #define extended coefficient matrix as 'a'
    a=np.concatenate([a,b],axis=1)
    #push forward
    (row,col)=a.shape
    for j in range(row):
        for i in range(j+1,row):
            p= a[i,j] /a[j,j]
            a[i]-=p*a[j]
    #back forward
    for i in range(row)[::-1]:
        x[i]=(a[i,col-1]-np.dot(a[i,i+1:row],x[i+1:row]))/a[i,i]

def main():
    a=np.matrix([[2,4,6],
                 [1,-1,5],
                 [4,1,-2]],dtype='float64')
    b=np.matrix([28,7,21],'float64').T
    x=np.empty(3)

    solveeq_gauss(a,b,x)
    print(x)
if __name__ == '__main__':
    main()
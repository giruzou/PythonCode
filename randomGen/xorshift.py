
def outer():
    x=1
    def inner(x):
        x+=1
        return x
    x= inner(x)
    return x




def xor64(x=88172645463325252):
    x=x^(x<<13)
    x=x^(x>>7)
    x=x^(x<<17)
    return x

def main1():
    r=0
    for i in range(30):
        if i==0:
            r=xor64()
        else:
            r=xor64(r)
        print(r)


def main():
    x=outer()
    print(x)
    x=outer()
    print(x)
    
if __name__ == '__main__':
    main()
 

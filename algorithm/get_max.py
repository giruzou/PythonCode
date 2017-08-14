from measure import get_elappsed_time

@get_elappsed_time
def printhi():
    print("HI")
def main():
    res=printhi()
    print(res)
if __name__ == '__main__':
    main()
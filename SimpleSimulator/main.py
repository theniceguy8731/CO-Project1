bin=list()

if __name__=='__main__':
    while True:
        try:
            l=input()
        except EOFError:
            break
        else:
            bin+=[l]


pc=0
bin=[]
regz=[0,0,0,0,0,0,0,0]
def mem_dump():
    for i in range(len(bin)):
        print(bin[i],end='')
        if i!=len(bin)-1:
            print()

def print_state():
    #print pc
    print(format(pc, '07b'), end ="        ")
    # print regz
    for i in range(len(regz)):
        print(format(regz[i], '016b'), end ="")
        if i!=len(regz)-1:
            print(" ",end='')
    print()

if __name__=='__main__':
    while True:
        try:
            l=input()
        except EOFError:
            break
        else:
            bin+=[l]

    #filling the file with zeroes so as to store memory later using st instruction
    for i in range(len(bin), 128):
        bin += ["0" * 16]
    
    while True:
        inst=bin[pc]

        #additon
        if inst[:5]=='00000':
            regz[7]=0
            regz[int(inst[7:10],2)]=regz[int(inst[10:13],2)]+regz[int(inst[13:16],2)]
            #overflow
            if regz[int(inst[7:10],2)]>=65536:
                regz[7]=8
                regz[int(inst[7:10],2)]=0
            print_state()
        #subtration
        elif inst[:5]=='00001':
            regz[7]=0
            regz[int(inst[7:10],2)]=regz[int(inst[10:13],2)]-regz[int(inst[13:16],2)]
            #overflow
            if regz[int(inst[10:13],2)]-regz[int(inst[13:16],2)]<0:
                regz[7]=8
                regz[int(inst[7:10],2)]=0
            print_state()
        #multiply
        elif inst[:5]=='00110':
            regz[7]=0
            regz[int(inst[7:10],2)]=regz[int(inst[10:13],2)]*regz[int(inst[13:16],2)]
            #overflow
            if regz[int(inst[7:10],2)]>=65536:
                regz[7]=8
                regz[int(inst[7:10],2)]=0
            print_state()
        #xor
        elif inst[:5]=='01010':
            regz[7]=0
            regz[int(inst[7:10],2)]=regz[int(inst[10:13],2)]^regz[int(inst[13:16],2)]
            print_state()
        #or
        elif inst[:5]=='01011':
            regz[7]=0
            regz[int(inst[7:10],2)]=regz[int(inst[10:13],2)]|regz[int(inst[13:16],2)]
            print_state()
        #and
        elif inst[:5]=='01100':
            regz[7]=0
            regz[int(inst[7:10],2)]=regz[int(inst[10:13],2)]&regz[int(inst[13:16],2)]
            print_state()
######################################################################################################
        #move immediate
        elif inst[:5]=='00010':
            regz[7]=0
            regz[int(inst[6:9],2)]=int(inst[9:16],2)
            print_state()
        #right shift
        elif inst[:5]=='01000':
            regz[int(inst[6:9],2)]=regz[int(inst[6:9],2)]>>int(inst[9:16],2)
            regz[7]=0
            print_state()
        #left shift
        elif inst[:5]=='01001':
            regz[int(inst[6:9],2)]=regz[int(inst[6:9],2)]<<int(inst[9:16],2)
            regz[7]=0
            print_state()
######################################################################################################
        #move register
        elif inst[:5]=='00011':
            regz[int(inst[10:13],2)]=regz[int(inst[13:16],2)]
            regz[7]=0
            print_state()
        #divide
        elif inst[:5]=='00111':
            regz[7]=0
            if regz[int(inst[13:16],2)]==0:
                regz[0]=0
                regz[1]=0
                regz[7]=8
            else:
                regz[0]=regz[int(inst[10:13],2)]//regz[int(inst[13:16],2)]
                regz[1]=regz[int(inst[10:13],2)]%regz[int(inst[13:16],2)]
            print_state()
        #invert
        elif inst[:5]=='01101':
            regz[7]=0
            regz[int(inst[10:13],2)]= ~regz[int(inst[13:16],2)]
            print_state()
        #compare    
        elif inst[:5]=='01110':
            regz[7]=0
            if regz[int(inst[10:13],2)]==regz[int(inst[13:16],2)]:
                regz[7]=1
            elif regz[int(inst[10:13],2)]<regz[int(inst[13:16],2)]:
                regz[7]=4
            else:
                regz[7]=2
            print_state()
######################################################################################################
        #load
        elif inst[:5]=='00100':
            regz[7]=0
            regz[int(inst[6:9], 2)] = int(bin[int(inst[9:], 2)], 2)
            print_state()
        #store
        elif inst[:5]=='00101':
            bin[int(inst[9:], 2)] = format(regz[int(inst[6:9], 2)], '016b')
            regz[7]=0
            print_state()
######################################################################################################
        #unconditional jump
        elif inst[:5]=='01111':
            regz[7]=0
            print_state()
            pc = int(inst[9:], 2) - 1
        #jump if less than
        elif inst[:5]=='11100':
            if regz[7]==4:
                regz[7]=0
                print_state()
                pc = int(inst[9:], 2) - 1
            else:
                regz[7]=0
                print_state()
        #jump if greater than
        elif inst[:5]=='11101':
            if regz[7]==2:
                regz[7]=0
                print_state()
                pc = int(inst[9:], 2) - 1
            else:
                regz[7]=0
                print_state()
        #jump if equal
        elif inst[:5]=='11111':
            if regz[7]==1:
                regz[7]=0
                print_state()
                pc = int(inst[9:], 2) - 1
            else:
                regz[7]=0
                print_state()
######################################################################################################
        #halt
        elif inst[:5]=='11010':
            regz[7]=0
            print_state()
            break
        else:
            print(inst[:5])
            print("invalid entry")
            break

        pc+=1

mem_dump()

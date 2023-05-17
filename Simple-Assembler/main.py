error_present=False #check for error in the code
halt_present=False #check if the code has halt in it
varz={} #dictionary of variable
labels={} #dictionary of labels
inst=[] # list of instruction line numbers
mms=['ad', 'su', 'mu', 'xo', 'or', 'an', 'mo', 'rs', 'ls', 'mo', 'di', 'no', 'cm', 'ld', 'st', 'jm', 'jl', 'jg', 'je', 'hl']
sp_sym=',$#@!%^&*()\{\}[]-+=\|;:""<>,?/`~'
op_codes={'A':{'add':'00000','sub':'00001','mul':'00110','xor':'01010','or':'01011','and':'01100'},'B':{'mov':'00010','rs':'01000','ls':'01001'},'C':{'mov':'00011','div':'00111','not':'01101','cmp':'01110'},'D':{'ld':'00100','st':'00101'},'E':{'jmp':'01111','jlt':'11100','jgt':'11101','je':'11111'},'F':{'hlt':'11010'}}
regs={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','R6':'110','FLAGS':'111'}
file=open('errors.txt','w')
#functions for some specific checks
#these are the functions to check specific types of instructions
#removes the label from the starting of the instruction if required
def rem_label(s):
    if ':' in s:
        return s[s.index(':')+2:].strip()
    return s
#now we will proceed with functions which check specific type of instructions
def check_a(s,n):
    if s[:3] in op_codes['A'].keys() or s[:2] in op_codes['A'].keys():
        if len(s.split(' '))==4:
            temp_flag=True
            for reg in s.split(' ')[1:]:
                if reg not in regs.keys():
                    temp_flag=False
            if not temp_flag:
                print_inst_error(1,n)

        else:
            print_inst_error(1,n)
    else:
        print_inst_error(100,n)
    return

def check_b(s,n):
    if s[:3] in op_codes['B'].keys() or s[:2] in op_codes['B'].keys():
        if len(s.split(' '))==3:
            if s.split(' ')[1] not in regs.keys():
                print_inst_error(1,n)
            if s.split(' ')[2][0]!='$' or int(s.split(' ')[2][1:]) not in range(0,127):
                print_inst_error(5,n)
        else:
            print_inst_error(1,n)
    else:
        print_inst_error(100,n)
    return

def check_c(s,n):
    if s[:3] in op_codes['C'].keys():
        if len(s.split(' '))==3:
            if s.split(' ')[1] not in regs.keys() or s.split(' ')[2] not in regs.keys() or s.split(' ')[1]=='FLAGS':
                print_inst_error(1,n)
        else:
            print_inst_error(1,n)
    else:
        print_inst_error(100,n);
    return
def check_d(s,n):
    if s[:2] in op_codes['D'].keys():
        if len(s.split(' '))==3:
            if s.split(' ')[1] not in regs.keys():
                print_inst_error(1,n)
            if s.split(' ')[2] not in varz and s.split(' ')[2] in labels:
                print_inst_error(6,n)
            elif s.split(' ')[2] not in varz:
                print_inst_error(2,n)
            
        else:
            print_inst_error(1,n)
    else:
        print_inst_error(100,n);
    return

def check_e(s,n):
    if s[:3] in op_codes['E'].keys() or s[:2] in op_codes['E'].keys():
        if len(s.split(' '))==2:
            if s.split(' ')[1] not in labels and s.split(' ')[1] in varz:
                print_inst_error(7,n)
            elif s.split(' ')[1] not in labels:
                print_inst_error(3,n)

        else:
            print_inst_error(1,n)
    else:
        print_inst_error(100,n)
    return
def check_f(s,n):
    s=rem_label(s).strip()
    if s[:3]=='hlt':
        global halt_present
        halt_present=True
        if len(s.split(' '))!=1:
            print_inst_error(1,n)
    else:
        print_inst_error(100,n)
    return

#this function check for unwanted symbols between word which are general syntax errors
def sym_check(st):
    for x in sp_sym:
        if x in st:
            return False
    return True
#main function to do checking as far as instructions are considered
def inst_check(list):
    for i in inst:
        temp_inst=rem_label(list[i])
        if temp_inst[:2] in mms[:6]:
            check_a(temp_inst,i)
        elif temp_inst[:2] in mms[6:9] and '$' in temp_inst:
            check_b(temp_inst,i)
        elif temp_inst[:2] in mms[9:13]: 
            check_c(temp_inst,i)
        elif temp_inst[:2] in mms[13:15]:
            check_d(temp_inst,i)
        elif temp_inst[:2] in mms[15:19]:
            check_e(temp_inst,i)
        elif temp_inst[:2] in mms[19:20]:
            check_f(temp_inst,i)
    return
#this function is a common function it will be called with the given error code to print the error in the error file
def print_inst_error(n,linen=0):
    global error_present
    if not error_present:
        error_present=True
    linen+=1
    if n==1:
        print(f"error : typos in instruction name or register name on line {linen}\n")
    elif n==2:
        print(f"error : use of undefined variable {linen}\n")        
    elif n==3:
        print(f"error : use of undefined labels {linen}\n")
    elif n==4:
        print(f"error : illegal use of flags register {linen}\n")
    elif n==5:
        print(f"error : illegal immediate values {linen}\n")
    elif n==6:
        print(f"error : misuse of labels as variable  {linen}\n")
    elif n==7:
        print(f"error : misuse of variables as labels  {linen}\n")
    elif n==8:
        print(f"error : variables not declared at the beginning \n")
    elif n==9:
        print(f"error : missing halt instruction at the end\n")
    elif n==10:
        print(f"error : halt not being used as last instruction or more than one halt {linen}\n")
    else:
        print(f'error : general syntax error {linen}\n')
    return
#this classifies and saves each statement given to it according to its correct place
def classify(s,n):
    # checking : to find labels
    if ':' in s:
        if s.index(':')!=0:
            labels[s[:s.index(':')]]=n
            inst.append(n)
            return 'label'
        else:
            print_inst_error(100,n)
    #finding var to checking for variables
    
    if s[:3]=='var':
        if len(s.split(' '))==2:
            if sym_check(s.split()[1]):
                varz[s.split()[1]]=n
                return 'var'
    #to check if an instruction is from ISA
    if s[:2] in mms:
        inst.append(n)
        return 'inst'
    
    return 'None'
#the main error checking code which calls all other functions
def error_check(list):
    #we will first parse through the instruction to find its type
    #storing the number on which labels and variables are present
    for l in range(len(list)):
        ty=classify(list[l],l)
        if ty=='None':
            print_inst_error(100,l)
        # till here we have classified and saved all the instructions
        # according to their classification into var declaration
        # instruction and label and otherwise general error
        
    inst_check(list)
    for l in range(len(list)):
        if 'FLAGS' in list[l]:
            st=rem_label(list[l])
            if st[:3]!='mov':
                print_inst_error(4,l)
    try:
        if max(varz.values())!=len(varz.values())-1:
            print_inst_error(8)
    except:
        pass
    if not halt_present:
        print_inst_error(9)
    for l in range(len(list)-1):
        if 'hlt'==rem_label(list[l]):
            print_inst_error(10,l)
    if len(final_list)>128:
        print_inst_error(100)
#########################################################################################################
#########################################################################################################
#########################################################################################################
#5 bits for opcode, 2 unused, 3 registors 3 bit each
def conv_a(s,n):
    bin=''
    for x in op_codes['A'].keys():
        if s[:3]==x:
            bin+=op_codes['A'][x]
        elif s[:2]==x:
            bin+=op_codes['A'][x]
    bin+='0'*2
    y,a,b,c=s.split(' ')
    bin+=regs[a]
    bin+=regs[b]
    bin+=regs[c]
    print_bin(bin)
    return
#5 bits for opcode, 1 unused, 1 registors 3 bit, 1 imm
def conv_b(s,n):
    bin=''
    for x in op_codes['B'].keys():
        if s[:3]==x:
            bin+=op_codes['B'][x]
        elif s[:2]==x:
            bin+=op_codes['B'][x]
    bin+='0'*1
    y,a,b=s.split(' ')
    b=b[1:]
    bin+=regs[a]
    bin+=format(int(b),'07b')
    print_bin(bin)
    return
#5 bits for opcode, 5 unused, 2 registors 3 bit each
def conv_c(s,n):
    bin=''
    for x in op_codes['C'].keys():
        if s[:3]==x:
            bin+=op_codes['C'][x]
        elif s[:2]==x:
            bin+=op_codes['C'][x]
    bin+='0'*5
    y,a,b=s.split(' ')
    bin+=regs[a]
    bin+=regs[b]
    print_bin(bin)
    return
#5 bits for opcode, 1 unused, 1 registors 3 bit, variable in place of mem address
def conv_d(s,n):
    bin=''
    for x in op_codes['D'].keys():
        if s[:3]==x:
            bin+=op_codes['D'][x]
        elif s[:2]==x:
            bin+=op_codes['D'][x]
    bin+='0'*1
    y,a,b=s.split(' ')
    bin+=regs[a]
    global len_without_varz
    bin+=format(len_without_varz+varz[b],"07b")
    print_bin(bin)
    return
#5 bits for opcode, 4 unused, 1 mem address
def conv_e(s,n):
    bin=''
    for x in op_codes['E'].keys():
        if s[:3]==x:
            bin+=op_codes['E'][x]
        elif s[:2]==x:
            bin+=op_codes['E'][x]
    bin+='0'*4
    y,b=s.split(' ')
    bin+=format(labels[b]-len(varz),"07b")
    print_bin(bin)
    return
#5 bits for opcode, 11 unsued
def conv_f(s,n):
    bin=''
    for x in op_codes['F'].keys():
        if s[:3]==x:
            bin+=op_codes['F'][x]
        elif s[:2]==x:
            bin+=op_codes['F'][x]
    bin+='0'*11
    print_bin(bin)
    return
#this  will print the binary code to stdout
def print_bin(s):
    print(s)
    return
#main conversion for binary text file
def bin_gen(list):
    for i in range(len(list)):
        temp_inst=rem_label(list[i])
        if i in inst:
            temp_inst=rem_label(list[i])
            #type a
            if temp_inst[:2] in mms[:6]:
                conv_a(temp_inst,i)
                #type b
            elif temp_inst[:2] in mms[6:9] and '$' in temp_inst:
                conv_b(temp_inst,i)
                #type c
            elif temp_inst[:2] in mms[9:13]: 
                conv_c(temp_inst,i)
                #type d
            elif temp_inst[:2] in mms[13:15]:
                conv_d(temp_inst,i)
                #type e
            elif temp_inst[:2] in mms[15:19]:
                conv_e(temp_inst,i)
                #type f
            elif temp_inst[:2] in mms[19:20]:
                conv_f(temp_inst,i)
                #type g
    return

#########################################################################################################
#########################################################################################################
#########################################################################################################
#main running 
if __name__=='__main__':
    #string to store code
    list=''
    #taking inputt
    while True:
    # f=open('./assembler/file.txt',"r")
    # list = f.read()
        try:
            x=input()
            list+=(x+'\n')
        except EOFError:
            break
    i=1
    temp_len=len(list)
    #modifying the format of the code to account for irregularaties
    interim=''
    interim+=list[0]
    while i<temp_len:
        if list[i]=='\n' and list[i-1]==':':
            interim+=' '
        else:
            interim+=list[i]
        temp_len=len(list)
        i=i+1
    interim=interim.replace('\t',' ')
    list=interim.split('\n')
    for l in range(len(list)):
        list[l]=list[l].strip()
     #the final list with all the instructions stored as members of the list
    final_list=[]
    for l in range(len(list)):
        if len(list[l])!=0:
            final_list.append(list[l])
    # first we need to check the errors in the code
    error_check(final_list)
    len_without_varz=len(final_list)-len(varz)
    if not error_present:
        #after checking for errors,we finally convert the code to binary
        bin_gen(final_list)
file.close()

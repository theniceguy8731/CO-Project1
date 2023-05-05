varz={}
labels={}
inst=[]
mms=['ad', 'su', 'mu', 'xo', 'or', 'an', 'mo', 'rs', 'ls', 'mo', 'di', 'no', 'cm', 'ld', 'st', 'jm', 'jl', 'jg', 'je', 'hl']
sp_sym=',$#@!%^&*()\{\}[]-+=\|;:""<>,.?/`~'
op_codes={'A':{'add':'00000','sub':'00001','mul':'00110','xor':'01010','or':'01011','and':'01100'},'B':{'mov':'00010','rs':'01000','ls':'01001'},'C':{'mov':'00011','div':'00111','not':'01101','cmp':'01110'},'D':{'ld':'00100','st':'00101'},'E':{'jmp':'01111','jlt':'11100','jgt':'11101','je':'11111'},'F':{'hlt':'11010'}}
regs={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','R6':'110','FLAGS':'111'}
file=open('errors.txt','w')
#these are the functions to check specific types of instructions
def check_a(s,n):

    return
def check_b():
    return
def check_c():
    return
def check_d():
    return
def check_e():
    return
def check_f():
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
        if list[i][:2] in mms[:6]:
            check_a(list[i],i)
        elif list[i][:2] in mms[6:9] and '$' in list[i]:
            check_b(list[i],i)
        elif list[i][:2] in mms[9:13]: 
            check_c(list[i],i)
        elif list[i][:2] in mms[13:15]:
            check_d(list[i],i)
        elif list[i][:2] in mms[15:19]:
            check_e(list[i],i)
        elif list[i][:2] in mms[19:20]:
            check_f(list[i],i)
    return
#this function is a common function it will be called with the given error code to print the error in the error file
def print_inst_error(n):
    if n==1:
        pass
    elif n==2:
        pass
    elif n==3:
        pass
    elif n==4:
        pass
    elif n==5:
        pass
    elif n==6:
        pass

    return
#this classifies and saves each statement given to it according to its correct place
def classify(s,n):
    if s[-1]==':':
        if sym_check(s[:-1]):
            labels[s.strip(':')]=n
            return 'label'
    
    if s[:3]=='var':
        if len(s.split(' '))==2:
            if sym_check(s.split()[1]):
                varz[s.split()[1]]=n
                return 'var'
    
    if s[:2] in mms:
        inst.append(n)
        return 'inst'
    
    return 'None'

def error_check(list):
    for l in range(len(list)):
        ty=classify(list[l],l)
        if ty=='None':
            file.write(f'General syntax error: line {l}\n')
        # till here we have classified and saved all the instructions
        # according to their classification into var declaration
        # insturction and label and otherwise general errors
    inst_check(list)

def bin_gen():
    
    return


if __name__=='__main__':
    f=open('file.txt',"r")
    list = f.read().split('\n')
    for l in range(len(list)):
        list[l]=list[l].strip()
    final_list=[]
    for l in range(len(list)):
        if len(list[l])!=0:
            final_list.append(list[l])

    error_check(final_list)
    bin_gen()
    print(final_list)

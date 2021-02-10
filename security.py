import sys, getpass, random, string

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def Get_Master_Password(count= 0): 
    try:
        if count < 3:
            #password = input("Master Password: ")
            password1 = getpass.getpass("Master Password: ")
            password2 = getpass.getpass("Confirm Password: ")
            if password1 != password2:
                count +=1
                print(f"{bcolors.OKBLUE}Error!!  Enter same password{bcolors.ENDC}")
                password1 = Get_Master_Password(count = count)
                return password1
            else:
                return password1
        else:
            print(f"{bcolors.FAIL}3 unsuccessful attempt{bcolors.ENDC}")
            sys.exit()
    except KeyboardInterrupt:
        print(f"{bcolors.FAIL}User Interrupt{bcolors.ENDC}")
        sys.exit()

def Ask_Password(userpassword, user_name ,count = 0):
    if count < 3:
        password = getpass.getpass(f"MasterPassword: ")
        
        if password != userpassword:
            count += 1
            print("Incorrect Password, try again")
            pass_value = Ask_Password(userpassword,user_name,count = count)
            return pass_value
        else:
            return True
    else:
        print(f"{bcolors.FAIL}3 unsuccessful attempt")
        sys.exit()

def Generate_Password(len=8):
    password_charectors = string.ascii_letters + string.punctuation+ string.digits
    password = ''.join(random.choice(password_charectors) for i in range(len))
    return password



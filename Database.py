import pandas as pd
import sys, os
import Encryption as en
file_name = "Database.csv"

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



class UserData:
    def __init__(self):
        self.password = None
        self.key = None

    def Create_User_Database(self):
        self.app = None
        self.login_id = None
        self.password = None
        self.user_data = {"App": self.app,
                          "LoginId": self.login_id,
                          "Password": self.password
                          }
        self.user_data_base = pd.DataFrame(self.user_data,
                                           columns=["App", "LoginId", "Password"])
        self.user_data_base.to_csv(f"Database.csv", index=False)
        print(f"{bcolors.OKBLUE}User DataBase created{bcolors.ENDC}")

    def Add_Password(self):
 
        self.user_data_base = pd.read_csv("Database.csv")
        self.user_data = {"App": self.app,
                          "LoginId": self.login_id,
                          "Password": self.password}
        #partial_data_base = self.user_data_base[self.user_data_base["App"] == self.app]
        #print(type(partial_data_base))
        #print(existing_login
        self.user_data_base = self.user_data_base.append(self.user_data,
                                                         ignore_index=True)
        self.user_data_base.to_csv("Database.csv", index=False)
        print(f"{bcolors.OKBLUE}{self.app} is added to the database{bcolors.ENDC}")
        en.encrypt(self.key, file_name)

    def Return_Password(self):
        try:
            self.user_data_base = pd.read_csv(file_name)
            app_list = list(self.user_data_base["App"])
            app_found = []
            applen = len(self.app)
            for _ in app_list:
                if self.app in _.lower()[:applen]:
                    app_found.append(_)
            if len(app_found) == 1:
                self.app = app_found[0]
                datas = self.user_data_base[self.user_data_base["App"] == self.app]
                self.login_id = list(datas["LoginId"])[0]
                self.password = list(datas["Password"])[0]
            elif len(app_found) > 1:
                print(
                    f"{bcolors.WARNING}{len(app_found)} accound found{bcolors.ENDC}")
                login_list = []
                for i in range(len(app_found)):
                    datas = self.user_data_base[self.user_data_base["App"] == app_found[i]]
                    login_id = list(datas["LoginId"])[i]
                    login_list.append(login_id)
                    print(f"{i}:{login_id}")
                indx = int(input(f"{bcolors.OKGREEN}Number:{bcolors.ENDC}"))
                self.login_id = login_list[indx]
                self.password = list(
                    self.user_data_base[self.user_data_base["LoginId"] == self.login_id]["Password"])[0]
            en.encrypt(self.key, file_name)
            return self.login_id, self.password
        except Exception as err:
            #print(err)
            print(f"{bcolors.FAIL}Data not found!{bcolors.ENDC}")
            en.encrypt(self.key, file_name)
            sys.exit()

    def Remove_Password(self):
        try:
            self.user_data_base = pd.read_csv(file_name)
            self.app = input(f"{bcolors.OKGREEN}App:{bcolors.ENDC} ")
            app_list = list(self.user_data_base["App"])
            app_found = []
            applen = len(self.app)
            for _ in app_list:
                if self.app in _.lower()[:applen]:
                    app_found.append(_)
            if len(app_found) == 0:
                raise ValueError
            elif len(app_found) == 1:
                self.app = app_found[0]
                print(
                    f"{bcolors.WARNING}This will remove your data and can't be restored!!{bcolors.ENDC}")
                try:
                    check = str(input(
                        f"{bcolors.OKGREEN}Continue removing {self.app} [Yes/No]:{bcolors.ENDC} ")).lower()
                    if check[0] == "y":
                        self.user_data_base = self.user_data_base[self.user_data_base["App"] != self.app]
                        self.user_data_base.to_csv(
                            "Database.csv", index=False)
                        print(
                            f"{bcolors.OKBLUE}{self.app} Removed from database{bcolors.ENDC}")
                    else:
                        print(f"{bcolors.FAIL}Cancelling!!")
                        en.encrypt(self.key, file_name)
                        sys.exit()
                except Exception as err:
                    print(f"{bcolors.WARNING} No when default")
                    en.encrypt(self.key, file_name)
                    sys.exit()
            elif len(app_found) > 1:
                print(
                    f"{bcolors.WARNING}[{len(app_found)} Account found]{bcolors.ENDC}")
                login_list = []
                for i in range(len(app_found)):
                    datas = self.user_data_base[self.user_data_base["App"] == app_found[i]]
                    login_id = list(datas["LoginId"])[i]
                    login_list.append(login_id)
                    print(f"{i}:{login_id}")
                indx = int(input(f"{bcolors.OKGREEN}Number:{bcolors.ENDC} "))
                self.login_id = login_list[indx]
                datas = self.user_data_base[self.user_data_base["LoginId"]
                                            == self.login_id]
                self.app = list(datas["App"])[0]
                print(
                    f"{bcolors.WARNING}This will remove your data and can't be restored!!{bcolors.ENDC}")
                try:
                    check = str(input(
                        f"{bcolors.OKGREEN}Continue removing {self.app} [Yes/No]:{bcolors.ENDC} ")).lower()
                    if check[0] == "y":
                        self.user_data_base = self.user_data_base[self.user_data_base["LoginId"]
                                                                  != self.login_id]
                        self.user_data_base.to_csv(
                            "Database.csv", index=False)
                        print(f"{bcolors.OKBLUE}{self.app} Removed from database")
                        en.encrypt(self.key, file_name)
                        sys.exit()
                    else:
                        print(f"{bcolors.FAIL}Cancelling!!")
                        en.encrypt(self.key, file_name)
                        sys.exit()
                except Exception as err:
                    print(err)
                    print(f"{bcolors.WARNING} No when default")
                    en.encrypt(self.key, file_name)
                    sys.exit()
        except Exception as err:
            print(f"{bcolors.FAIL}Data not found")
            en.encrypt(self.key, file_name)
            sys.exit()

    def Remove_User(self):
        user_list = pd.read_csv(file_name)
        print(
            f"{bcolors.WARNING}This will remove all your user data and can't be restored!{bcolors.ENDC}")
        check = str(
            input(f"{bcolors.OKGREEN}Continue [Yes/No]:{bcolors.ENDC} ")).lower()
        try:
            if check[0] == "y":
                os.remove("Database.csv")
                print(
                    f"{bcolors.OKBLUE}All data  is removed from the system")
                sys.exit()
            else:
                print(f"{bcolors.FAIL}Cancelling!!")
                sys.exit()
        except Exception as err:
            print(f"{bcolors.WARNING}No when default")
            sys.exit()

    def List_Passwords(self):
        self.user_data_base = pd.read_csv(file_name)
        self.app = self.user_data_base["App"]
        self.login_id = self.user_data_base["LoginId"]
        result = {"App": self.app,
                  "Login Id": self.login_id}
        result = pd.DataFrame(result, columns=["App", "Login Id"])
        print(result)
        en.encrypt(self.key, file_name)


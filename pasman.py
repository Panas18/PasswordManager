from Database import UserData
import Database as db
import argparse
import sys
import pyperclip
import getpass
import pandas as pd
import security as sc
import Encryption as En
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


class User:
    def __init__(self):
        self.data = UserData()

    def Identify_User(self):
        try:
            try:
                self.data.user_data_base = pd.read_csv(file_name)
                self.data.password = getpass.getpass("MasterPassword: ")
                global key
                key = En.Generate_Key(self.data.password)
                self.data.key = key
                En.decrypt(key, file_name)
                self.data.user_data_base = pd.read_csv(file_name)
                return True
            except Exception as err:
                print(f"{bcolors.FAIL}Incorrect Password{bcolors.ENDC}")
                return False
                sys.exit()
        except KeyboardInterrupt:
            print(f"{bcolors.FAIL}User Interrupt!{bcolors.ENDC}")
            sys.exit()
try:
    U = User()
    U.data.user_data_base = pd.read_csv(file_name)
except FileNotFoundError:
    print(f"{bcolors.OKBLUE}Database not created!!!{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}Enter a MasterPassword to create database{bcolors.ENDC}")
    password = sc.Get_Master_Password()
    U.data.Create_User_Database()
    key = En.Generate_Key(password)
    En.encrypt(key, file_name)
    sys.exit()

parser = argparse.ArgumentParser(description="CLI Password Manager")


parser.add_argument("-a", "--add_password", action='store_true',
                    help="Add new password")
parser.add_argument("-v", "--view_password", action='store_true',
                    help="View saved password and login id")
parser.add_argument("-l", "--list_passwords", action='store_true',
                    help="Remove a stored password ")
parser.add_argument("-R", "--remove_all", action='store_true',
                    help="Remove all data stored in the system")
parser.add_argument("-r", "--remove_pass", action='store_true',
			help="Remove a stored password")

args = parser.parse_args()


if len(sys.argv) > 1:
    try:
        if args.add_password:
            try:
                U = User()
                pass_value = U.Identify_User()
                if pass_value:
                    U.data.app = input(
                        f"{bcolors.OKGREEN}App:{bcolors.ENDC} ")
                    U.data.login_id = input(
                        f"{bcolors.OKGREEN}Login Id:{bcolors.ENDC} ")
                    partial_data_base = U.data.user_data_base[U.data.user_data_base["App"] == U.data.app]
                    login_id = list(partial_data_base["LoginId"])
                    try:
                        if U.data.login_id in login_id:
                            raise ValueError
                        check = str(
                            input(f"{bcolors.OKGREEN}Generate Password? [Yes/No:]{bcolors.ENDC} ")).lower()
                        if check[0] == "y":
                            try:
                                pass_length = int(
                                    input(f"{bcolors.OKGREEN}Password Length:{bcolors.ENDC} "))
                                U.data.password = sc.Generate_Password(
                                    len=pass_length)
                            except Exception as err:
                                print(
                                    f"{bcolors.WARNING}password Length is 8 when defult{bcolors.ENDC}")
                                U.data.password = sc.Generate_Password()
                        else:
                            U.data.password = input(
                                f"{bcolors.OKGREEN}Password:{bcolors.ENDC} ")
                        U.data.Add_Password()
                    except ValueError:
                        print("App and LoginId already exists")
                        En.encrypt(key, file_name)
                        sys.exit()
            except Exception as err:
                print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")
                # print(err)

                sys.exit()

        if args.view_password:
            U = User()
            pass_value = U.Identify_User()
            if pass_value:
                U.data.app = str(
                    input(f"{bcolors.OKGREEN}App:{bcolors.ENDC} ")).lower().split(".")[0]
                login_id, password = U.data.Return_Password()
                print(f"Login Id:{bcolors.WARNING} {login_id}{bcolors.ENDC}")
                try:
                    pyperclip.copy(password)
                    print(f"{bcolors.OKBLUE}Password is copied to your clipboard{bcolors.ENDC}")
                    check = str(
                        input((f"{bcolors.OKGREEN}View Password? [Yes/No]:{bcolors.ENDC} "))).lower()
                    if check[0] == "y":
                        print(f"Password:{bcolors.WARNING} {password}{bcolors.ENDC}")
                    else:
                        sys.exit()
                except Exception as err:
                    print(f"{bcolors.WARNING}No when default{bcolors.ENDC}")
                    sys.exit()

        if args.list_passwords:
            U = User()
            pass_value = U.Identify_User()
            if pass_value:
                U.data.List_Passwords()

        if args.remove_pass:
            U = User()
            pass_value = U.Identify_User()
            if pass_value:
                U.data.Remove_Password()

        if args.remove_all:
            U = User()
            pass_value = U.Identify_User()
            if pass_value:
                U.data.Remove_User()

    except KeyboardInterrupt:
        print(f"{bcolors.FAIL}User Interrupt{bcolors.ENDC}")
        En.encrypt(key, file_name)
        sys.exit()
else:
    print(f"{bcolors.FAIL}Please Enter an argument")
    print(f"Run -h for help{bcolors.ENDC}")

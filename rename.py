#!/usr/bin/python3
import os , secrets, sys
  
os.chdir(sys.argv[1]) 
print(os.getcwd()) 
  
  
for f in os.listdir(): 
    f_name, f_ext = os.path.splitext(f) 
    f_new_name = filetoken = str(secrets.token_hex(2)) 
  
    new_name = '{}{}'.format(f_new_name, f_ext) 
    os.rename(f, new_name) 
    print(f"{f_name}{f_ext} --> {new_name}")


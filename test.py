import verify_creds_confi
import create_creds_confi

username_ok = False
password_ok = False 

if not verify_creds_confi.verify_user_existance("ion"):
    username_ok = True
if len("aaaaaaaaaa") > 5:
    password_ok = True

print(username_ok and password_ok)
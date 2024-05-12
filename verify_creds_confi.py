import configparser
import bcrypt


def verify_user_existance(entered_username): 
    # Retrieve the hashed password from the configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Check if entered_username is in config.ini file
    if entered_username in config:
        return True
    else:
        return False 
    

def verify_user_login(entered_username, entered_password):
    # Retrieve the hashed password from the configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Check if entered_username is in config.ini file
    if entered_username in config:
        stored_password_hash = config[entered_username]['Password']
        # Verify the entered password
        if bcrypt.checkpw(entered_password.encode('utf-8'), stored_password_hash.encode('utf-8')):
            return True
        else:
            return False
    else:
        return False
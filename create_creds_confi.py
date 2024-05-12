import configparser
import bcrypt


def save_to_config(username, hashed_password, file_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)

    # Create a new section for the user
    config[username] = {
        'Username': username,
        'Password': hashed_password.decode('utf-8')  # Convert bytes to string for storage
    }

    # Save the configuration to the file
    with open(file_path, 'w') as config_file:
        config.write(config_file)


def encrypt_pw(pw):
    # create hashed passwords
    hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
    return hashed_pw


def delete_from_config(username, file_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)

    # Check if the username exists in the configuration
    if username in config:
        # Remove the section for the specified user
        config.remove_section(username)
        # Save the updated configuration to the file
        with open(file_path, 'w') as config_file:
            config.write(config_file)
        print(f"Deleted credentials for '{username}' from {file_path}")
    else:
        print(f"No credentials found for '{username}' in {file_path}")
import os

def read_key_value_pairs(file_path):
    """Read key-value pairs from a text file."""
    key_value_pairs = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split(': ', 1)
                key_value_pairs[key] = value
    return key_value_pairs

def set_user_environment_variables(key_value_pairs):
    """Set environment variables for the current user on Windows."""
    for key, value in key_value_pairs.items():
        command = f'setx {key} "{value}"'
        os.system(command)

def main():
    file_path = 'test.txt'

    key_value_pairs = read_key_value_pairs(file_path)
    set_user_environment_variables(key_value_pairs)

if __name__ == "__main__":
    main()

"""
Create a file utils/safefile.py and define a class SafeFile that:

Mimics with open(...) as f behavior.

Prints/logs a message when opening and closing the file.

Ensures file closure even when exceptions occur.

🧩 Test case: Use SafeFile to write UAV-like sensor logs to disk safely.
"""

class SafeFile():
    def __init__(self, file_path, mode='r'):
        self.log__path = file_path
        self.mode = mode
        try:
            self.f = open(file_path, mode)
            print(f"Successfully open {file_path} in {mode} mode")
        except:
            self.f = None
            print(f"Failed to open the file {file_path}: {OSError}")

    def write_single_line(self, string):
        self.f.write(string+'\n')

    def read_single_line(self):
        string = self.f.read()
        return string
    
    def write_lines(self, liststring):
        self.f.writelines(liststring)

    def read_lines(self):
        list_string = self.f.readlines()
        return list_string

    def reset_readwrite_pointer(self):
        try:
            self.f = open(self.log_path, self.mode)
            print(f"Read Write pointer reset, will overwrite existing content\n")
        except:
            self.f = None
            print(f"Failed to open the file {self.log_path}: {OSError}")

    def change_access_mode(self, access_mode):
        try:
            self.mode = access_mode
            self.f = open(self.log_path, self.mode)
            print(f"Successfully reopen {self.log_path} in {self.mode}\n")
        except:
            self.f = None
            print(f"Failed to open the file {self.log_path}: {OSError}")

if __name__ == "__main__":
    sensor_log = SafeFile("./sensor_data.csv", "r")
    data = sensor_log.read_lines()
    print(data)
    

    

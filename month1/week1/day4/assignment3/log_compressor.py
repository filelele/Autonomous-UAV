import sys
import subprocess
bash_path = r'/usr/bin/bash'

def compress_and_timestamp():
    files_path = " ".join(sys.argv[1:])
    command = f"""
    time=$(date +"%Y%m%d_%H%M%S")\\
    && tar -czf log_backup_$time.tar.gz {files_path}
    """
    print(command)
    compress = subprocess.run(command, shell=True, capture_output=True, text=True)
    print("STDOUT: ", compress.stdout)
    print("STDOUT: ", compress.stderr)
    
if __name__ == "__main__":
    compress_and_timestamp()


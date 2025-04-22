import numpy as np
import subprocess
import decorator

class SensorDataLogger:

    def __init__(self, sensor_name, log_file_path="./"):
        self.sensor_name = sensor_name
        self.log_file_path = log_file_path
        self.data_buffer = []

    @decorator.log_call
    @decorator.timeit
    def add_data(self, data_array):
        self.data_buffer.append(data_array)

    @decorator.log_call
    @decorator.timeit
    def save_to_file(self):
        for data in self.data_buffer:
            line = np.array2string(data, separator=', ', formatter={'float_kind': lambda x: f"{x:.6f}"})
            line = line.strip('[]')
            # print(f"Line {line} will be passed to script.\n")
            save_to_csv_script = r"./save_to_csv.sh"
            result = subprocess.run(['/usr/bin/bash', save_to_csv_script, self.log_file_path, line], capture_output=True, text=True)
            # print("STDOUT:", result.stdout)
            # print('\n')
            # print("STDERR:", result.stderr)
            # print('\n')
    
    def clear(self):
        self.data_buffer = []

if __name__ == "__main__":
    sensorX = SensorDataLogger("sensorx")
    for i in range(10):
        sensorX.add_data(np.random.uniform(0,255,(256,256)))
    
    sensorX.save_to_file()
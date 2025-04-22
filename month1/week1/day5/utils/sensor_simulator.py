import safefile
import subprocess
import numpy as np
import decorator
import os

class Sensor(safefile.SafeFile):
    def __init__(self, name='default', data_dim=(1,1), log_dir='.', log_format='csv', max_buffer=10):
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        read_date = subprocess.run(['date +%Y%m%d_%H%M%S'],shell=True, capture_output=True, text=True)
        log_name = name + '-' + read_date.stdout
        log_path = f"{log_dir}/{log_name}.{log_format}"
        super().__init__(log_path, mode='a+')

        self.name = name
        self.data_dim = data_dim
        self.buffer = []
        self.buffer_size = max_buffer

    @decorator.timeit
    def readData(self, iterate=1):
        "Gen fake data"
        if (iterate+len(self.buffer)) <= self.buffer_size:
            for i in range(iterate):
                self.buffer.append(np.random.uniform(0,1,self.data_dim))
        else:
            num_read = self.buffer_size - len(self.buffer)
            print("Not enough space, will read {num_read} times till full.\n")
            while not(len(self.buffer) > self.buffer_size):
                self.buffer.append(np.random.uniform(0,1,self.data_dim))
    
    def __str__(self):
        return f"name:{self.name}\nlog_path:{self.log__path}\ndata_dim:{self.data_dim}\nbuffer_size:{self.buffer_size}\nbuffer_in_use:{len(self.buffer)}\n"
    
    def clearData(self):
        self.buffer = []

    @decorator.timeit
    def writeData(self):
        for i in range(len(self.buffer)):
            self.write_single_line((np.array2string(self.buffer[i], separator=',')).strip('[]'))
        
        self.clearData()

if __name__ == "__main__":
    voice_senseX = Sensor('senseX', (1,20), './logs', 'csv', 10)
    print(voice_senseX)
    voice_senseX.readData(iterate=8)
    voice_senseX.writeData()
    voice_senseX.readData(iterate=12)
    voice_senseX.writeData()
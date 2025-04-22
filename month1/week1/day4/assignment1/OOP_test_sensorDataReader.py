import sensorDataReader
import numpy as np

if __name__ == "__main__":
    soundWaveReader = sensorDataReader.SensorDataLogger("soundWaveX", "./")
    for i in range(10):
        a = np.random.uniform(0,1, size=(1,20))
        soundWaveReader.add_data(a)

    soundWaveReader.save_to_file()

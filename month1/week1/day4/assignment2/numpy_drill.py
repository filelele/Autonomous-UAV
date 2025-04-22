import numpy as np
import subprocess
bash_path = r"/usr/bin/bash"

if __name__ == "__main__":
    arr = np.random.rand(100,5)
    mean = np.mean(arr, axis=0)
    mean_result = np.array2string(mean, separator=', ', formatter={'float_kind': lambda x: f"{x:.6f}"})
    mean_result = "Mean by column:\n" + mean_result

    std = np.std(arr, axis = 0)
    std_result = np.array2string(std, separator=', ', formatter={'float_kind': lambda x: f"{x:.6f}"})
    std_result = "Standard deviation by column:\n" + std_result

    arr_normalized = (arr - np.mean(arr))/(np.max(arr) - np.min(arr))
    arr_normalized_result = np.array2string(arr_normalized, separator=', ', formatter={'float_kind': lambda x: f"{x:.6f}"})
    arr_normalized_result = "Normalized:\n" + arr_normalized_result

    to_save = [mean_result, std_result, arr_normalized_result]
    script_path = r"./save_to_csv.sh"
    for i in to_save:
        save_result = subprocess.run([bash_path, script_path, i], capture_output=True, text=True)
        print("STDOUT: ", save_result.stdout)
        print("STDERR: ", save_result.stderr)


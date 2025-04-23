🧑‍🏫 Assignment: Day 7 – Mini Project: CLI Tool to Batch Process Images with Filters + Logging  
📅 Track: Month 1 – Week 1 – Day 7  
🎯 Theme: Build your first small robotics-ready image processing utility using what you've learned this week.  

---

🎯 **Objectives**  
By the end of this assignment, you will:  
- Apply Python’s CLI tools (`argparse`) for user interaction.  
- Use OpenCV and NumPy to apply image filters.  
- Implement logging, decorators, and file I/O for production-level tools.  
- Structure the project to be modular and extensible—robotics pipeline-ready.  

---

📦 **Project Brief**  
Build a command-line interface (CLI) tool that takes a folder of images and:  
1. Applies one or more image filters (e.g., grayscale, Canny edge, blur).  
2. Saves the output to a new folder with logs of operations performed.  
3. Can be reused as a base for UAV CV tasks like dataset preprocessing.  

---

📋 **Requirements**  

🔹 **Command-Line Interface**  
Use `argparse` to accept:  
- `--input_dir`: Path to input folder with `.jpg` or `.png` files.  
- `--output_dir`: Where filtered images will be saved.  
- `--filter`: Filter to apply (`gray`, `canny`, `blur`).  
- `--log`: Enable logging output to a `.txt` file.  

🔹 **Image Filtering**  
Use OpenCV to support:  
- **Grayscale**: `cv2.cvtColor`  
- **Canny Edge Detection**: `cv2.Canny`  
- **Gaussian Blur**: `cv2.GaussianBlur`  

🔹 **Logging**  
- Log each image's filename and what filter was applied.  
- Use the `@log_call` and `@timeit` decorators from Day 5.  

---

🔹 **Folder Structure**  
```
cli_filter_tool/
├── main.py
├── filters.py
├── utils/
│   ├── decorators.py
│   └── logger.py
├── logs/
│   └── processing_log.txt
├── input_images/
└── output_images/
```

---

📂 **Deliverables**  
- **Project Folder**: Submit the `cli_filter_tool/` folder structured as described above.  
- **`main.py`**: Handles argument parsing and orchestrates the image processing pipeline.  
- **`filters.py`**: Contains filter functions implemented using OpenCV.  
- **`decorators.py`**: Reuse your `@log_call` and `@timeit` decorators from Day 5.  
- **Example Log File**: Provide a sample `logs/processing_log.txt` that includes timestamps and details of filters applied.  

---

🧠 **Bonus (Optional)**  
- Add support for batch resizing images before filtering using a `--resize` argument (e.g., `--resize 256x256`).  
- Implement a subprocess-based mode to process each image in a separate process for improved performance.  


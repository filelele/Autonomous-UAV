import time
import functools

def log_call(func):
    """
    log the function name and input arguments before execution
    """
    @functools.wraps(func)
    def wrapper(*args, **kargs):
        print("Passed in the following:\n")
        for arg in args:
            print(str(arg) + '\t')
        for key,value in kargs.items():
            print(f"{key}:{value}\t")
        
        func(*args, **kargs)

    return wrapper

def timeit(func):
    """
    measure the execution times and log the run time of function(up to days)
    """
    @functools.wraps(func)
    def wrapper(*args, **kargs):
        start = time.perf_counter_ns()
        func(*args, **kargs)
        end = time.perf_counter_ns()

        duration_ns = end - start

        duration = []
        
        duration.append(duration_ns//(24*60*60*(10**9))) #Day
        duration_ns-=duration[0]*24*60*60*(10**9)

        duration.append(duration_ns//(60*60*(10**9))) #Hour
        duration_ns-=duration[1]*60*60*(10**9)

        duration.append(duration_ns//(60*(10**9))) #Minute
        duration_ns-=duration[2]*60*(10**9)

        duration.append(duration_ns//(10**9)) #Second
        duration_ns-=duration[3]*(10**9)

        duration.append(duration_ns//(10**6)) #Milisec
        duration_ns-=duration[4]*(10**6)

        duration.append(duration_ns//(10**3)) #Microsec
        duration_ns-=duration[5]*(10**3)

        duration.append(duration_ns) #Nanosec

        print(f""" 
              Profiling: {duration[0]} Days, {duration[1]} Hours, {duration[2]} Minutes,\n 
              {duration[3]} Seconds,\n 
              {duration[4]} Miliseconds,\n
              {duration[5]} Microseconds,\n 
              {duration[6]} Nanoseconds.
              """)
    
    return wrapper
        


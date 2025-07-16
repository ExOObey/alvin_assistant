import time
import logging

def profile(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logging.info(f"Function {func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper

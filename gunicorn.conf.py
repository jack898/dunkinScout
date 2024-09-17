import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = '0.0.0.0:8000'
accesslog = '-'
capture_output = True

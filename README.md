# IrisTerminal-Python
Python version of the IrisTerminal

Run libcsp-python/examples/buildall.py with python 3 to create python bindings.
Python 3.7.16 is confirmed to be working.

Run the terminal with
LD_LIBRARY_PATH=./libcsp-python/build PYTHONPATH=./libcsp-python/build python3 main.py {PORT} 115200

It should send a ping to CDH (4).


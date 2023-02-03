'''Run all tests in test folder and generate coverage report

HOW TO USE:
run this file from ./dagea/ directory and see results in the terminal
'''

import os

os.system('cmd /k "coverage run -m unittest discover -p "*_test.py"')  # run all files with test pattern
os.system('cmd /k "coverage report -i"') # report in text format
os.system('cmd /c "coverage xml -i"')     # report in .xml 
'''Run all tests in test folder and generate coverage report

HOW TO USE:
run this file from ./dagea directory and see results in the terminal
'''

import os
import sys

# sys.path.append('C:/Users/alice/Documents/GitLab/dagea/src/pythonModules')	# add src folder to pythonpath
os.system('cmd /k "python -m coverage run -m unittest discover -p "*_test.py"')  # run all files with test pattern
os.system('cmd /k "cd test | coverage report"') # report in text format
os.system('cmd /c "coverage xml | cd .."')     # report in .xml 
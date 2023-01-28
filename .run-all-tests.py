'''Run all tests in test folder and generate coverage report

HOW TO USE:
run this file from ./dagea directory and see results in the terminal
'''

import os
import sys

# sys.path.append('C:/Users/alice/Documents/GitLab/dagea/src/pythonModules')	# add src folder to pythonpath
os.system('cmd /k "coverage run -m pytest test/"')  # run all files with test pattern
os.system('cmd /k "coverage report --omit:test/__init__.py"') # report in text format
os.system('cmd /c "coverage xml"')     # report in .xml 
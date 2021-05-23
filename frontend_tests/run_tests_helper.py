bashCommand = "python -m unittest discover ./frontend_tests/"
import subprocess
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

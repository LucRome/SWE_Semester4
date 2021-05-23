import subprocess
bashCommand = "python -m unittest discover ./frontend_tests/"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

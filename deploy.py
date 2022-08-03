import glob
import shutil
import os

files = [
    "code.py",
    "scd30.py",
    os.path.join("font", "Helvetica-Bold-16.bdf")
]

path = "."
destination = 'd:\\'

destination = os.path.abspath(destination)

def deploy(file_name):
    source = os.path.join(path, file_name)
    final_destination = os.path.join(destination, file_name)
    print("Copying {} to {}".format(source, final_destination))
    shutil.copy(source, final_destination)

for file in files:
    deploy(file)

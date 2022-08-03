import glob
import shutil
import os

files = [
    "code.py",
    "scd30.py"
]

folders = [
    "lib",
    "font"
]

path = "."
destination = 'd:\\'

destination = os.path.abspath(destination)

def deploy(file_name):
    source = os.path.join(path, file_name)
    final_destination = os.path.join(destination, file_name)
    print("Copying {} to {}".format(source, final_destination))
    shutil.copy(source, final_destination)

def deployFolder(folder):
    print("Folder: {}".format(folder))
    searchGlob = os.path.join(folder, "*")
    listFromGlob = glob.glob(searchGlob, recursive=True)
    for item in listFromGlob:
        if(os.path.isdir(item)):
            deployFolder(item)
            continue
        deploy(item)

for file in files:
    deploy(file)

for folder in folders:
    deployFolder(folder)
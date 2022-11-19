#! python
import glob
import shutil
import os
import filecmp
import subprocess



files = [
    "code.py"
]

folders = [
    "font",
    "pages",
    "sensors",
    "views",
    "bmps"
]

path = "."
destination = 'd:\\'

destination = os.path.abspath(destination)

def deploy(file_name):
    source = os.path.join(path, file_name)
    final_destination = os.path.join(destination, file_name)
    
    if (source.__contains__(".mpy")):
        print("Removing", source)
        os.remove(source)
        return

    # if (file_name.__contains__(".py") 
    #         # and not file_name.__contains__("__") 
    #         and not file_name.__contains__("code.py") 
    #         and not file_name.__contains__("bdf")):
    #     subprocess.call('mpy-cross.static-x64-windows-7.3.2.exe {}'.format(source))
    #     source_name, _ = os.path.splitext(source)
    #     source = source_name + ".mpy"
    #     dest_name, _ = os.path.splitext(final_destination)
    #     final_destination = dest_name + ".mpy"
        

    file_directory = os.path.dirname(final_destination)
    if(not os.path.exists(file_directory)):
        print("Making directory: {}".format(file_directory))
        os.makedirs(file_directory, exist_ok=True)
    if(os.path.exists(final_destination) and filecmp.cmp(source, final_destination, shallow=False)):
        print("no change {}".format(final_destination))
        return
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

# if not os.path.exists(mcross.exe):
#     wget https://adafruit-circuit-python.s3.amazonaws.com/bin/mpy-cross/mpy-cross.static-x64-windows-7.3.2.exe

for file in files:
    deploy(file)

for folder in folders:
    deployFolder(folder)

import shutil 
import os
import glob

FilePath = os.path.dirname(os.path.abspath(__file__))
baseSource = FilePath + "/plant-database-master/"
destination = FilePath + "/plant-database-master/json"

i=1
while i<7:
    dir = baseSource + "/json"+str(i)
    files = glob.iglob(os.path.join(dir, "*.json"))
    for file in files:
        if os.path.isfile(file):
            shutil.move(file, destination)
    os.rmdir(dir)
    i +=1

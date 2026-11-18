import os
import time
from os import listdir
from os.path import isfile, join


def last_access(path):
    """Print regular-file access times in listdir order without sorting."""
    files_list = [f for f in listdir(path) if isfile(join(path, f))]
    for k in files_list:
        print(k)
        access_time = os.path.getatime(path + "\\" + k)
        local_time = time.ctime(access_time)
        print("Last access time(Local time):", local_time)


if __name__ == "__main__":
    print("ENTER THE PATH TO FOLDER")
    path = input()
    last_access(path)

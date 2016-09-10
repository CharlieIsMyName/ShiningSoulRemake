from glob import *
def globfolder():
    folder=glob("*")
    for i in range(len(folder)):
        if "." in folder[i]:
            folder[i]=0
    while True:
        if 0 in folder:
            del folder[folder.index(0)]
        else:
            break
    return folder
foldername=globfolder()
print (foldername)

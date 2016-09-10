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
#up,upright,right,downright,down,downleft,left,upleft=0,1,2,3,4,5,6,7
#pic=[0]*8
#for n in foldername:
   # pic[eval(n)]=glob(n+"/*.png")
print (globfolder())

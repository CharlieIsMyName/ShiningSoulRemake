from glob import *
from pygame import *
screen=display.set_mode((800,600))
frameselfstatus=[0,0,0]#dx,dy,frstun
myClock = time.Clock()
running=True
#######################################
def globfolder(name):
    if name=="":
        folder=glob("*")
    else:
        folder=glob(name+"/*")
    for i in range(len(folder)):
        if "." in folder[i]:
            folder[i]=0
    while True:
        if 0 in folder:
            del folder[folder.index(0)]
        else:
            break
    return folder
def directinstr(status):
    a=""
    if status[1]==1:
        a=a+"down"
    elif status[1]==-1:
        a=a+"up"
    if status[0]==1:
        a=a+"right"
    elif status[0]==-1:
        a=a+"left"
    return eval(a)
def mode(s):
    global sprmode
    return sprmode.index(s)
##################load image##################
foldername=globfolder("")
up,upright,right,downright,down,downleft,left,upleft=0,1,2,3,4,5,6,7
sprmode=["bladeatk","bladecharge","bladedamage","bladedead","bladerunning","bladestanding","dart","dartatk","dartdamage","dartdead","dartrunning","dartstanding"]
#0bladeatk,1bladecharge,2bladedamage,3bladedead,4bladerunning,5bladestanding,6dart,7dartatk,8dartdamage,9dartdead,10dartrunning,11dartstanding
pic=[0]*8
for n in foldername:
    pic[eval(n)]=globfolder(n)
for x in range(len(pic)):
    for y in range(len(pic[x])):
        pic[x][y]=glob(pic[x][y]+"/*.png")
for x in range(len(pic)):
    for y in range(len(pic[x])):
        for z in range(len(pic[x][y])):
            pic[x][y][z]=image.load(pic[x][y][z]).convert_alpha()
###################main########################
while running:
    for evnt in event.get():                
        if evnt.type == QUIT:
            running = False
    keys = key.get_pressed()
    selfdirectionx,selfdirectiony=0,0
    if keys[K_UP]:
            selfdirectiony=-1
    if keys[K_DOWN]:
            selfdirectiony=1
    if keys[K_RIGHT]:
            selfdirectionx=1
    if keys[K_LEFT]:
            selfdirectionx=-1
##############################################################################################################################
    if (selfdirectionx,selfdirectiony)!=(0,0):
        frameselfstatus[0],frameselfstatus[1]=selfdirectionx,selfdirectiony## all the direct and mode can get from the main
    if (frameselfstatus[0],frameselfstatus[1])!=(0,0):
        draw.rect(screen,(0,0,0),(0,0,800,600),0)
        screen.blit(pic[directinstr(frameselfstatus)][mode("bladestanding")][0],(400,300))

        
    myClock.tick(60)
    display.flip()
quit()

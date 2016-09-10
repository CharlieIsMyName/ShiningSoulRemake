from pygame import *
from glob import *
def drtoul(pic,x,y):
    return (x-pic.get_width(),y-pic.get_height())
screen = display.set_mode((1200,800))
pics=[]
pics.append(glob("bladeatk/*.png"))
pics.append(glob("bladecharge/*.png"))
pics.append(glob("bladedamage/*.png"))
pics.append(glob("bladedead/*.png"))
pics.append(glob("bladerunning/*.png"))
pics.append(glob("dart/*.png"))
pics.append(glob("dartatk/*.png"))
pics.append(glob("dartdamage/*.png"))
pics.append(glob("dartdead/*.png"))
pics.append(glob("dartrunning/*.png"))
frame=[0]*10
Framedelay=15
framedelay=Framedelay
pic=[]
for i in range(10):
    pic.append([0]*(len(pics[i])))
for x in range(10):
    for y in range(len(pic[x])):
        pic[x][y]=image.load(pics[x][y])
for i in range(10):
    frame[i]=len(pics[i])-1
framen=[0]*10
while True:
    draw.rect(screen,(0,0,0),(0,0,1000,800))
    for i in range(10):
        screen.blit(pic[i][framen[i]],drtoul(pic[i][framen[i]],0+i*100,400+200*(-1)**i))
    framedelay-=1
    if framedelay==0:
        for i in range(10):
            framen[i]+=1
            framedelay=Framedelay
    for i in range(10):
        if framen[i]>frame[i]:
            framen[i]=0
    display.flip()

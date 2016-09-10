#Charlie Wang
#FP: survival game
#This game allows the player to walk on a big map, find enemies
#and defeat them, levelup skills, and tries to survive as long
#as possible
from pygame import *
from math import *
from random import *
from glob import *
#---------------functions----------------------------#
def nuke():#for testing
    if keys[K_i]:
        while mapenemyx!=[]:
            AIgetkilled(0)                
def note(a):#returns if the number put in is -,0,or+ by returning -1,0,1
    if a==0:
        return 0
    else:
        return abs(a)//a  
def dist(x1,y1,x2,y2):#return the distance between two points
    return ((x1-x2)**2+(y1-y2)**2)**0.5
def remove(rlist,unit):#remove the an element of a list
    tem=rlist[:]
    if unit in tem:
        del tem[tem.index(unit)]
    return tem
def midpointrect(x,y,l,h):#create a rect that the midpoint is x,y
    return Rect(x-l//2,y-h//2,l,h)
def treeblockrect(x,y):#put in the topleft corner of a tree and return a tree's blocking rect
    return Rect(x+135,y+170,99,88)
def collideanyrect(rec,reclist):#return if the rect collide with any of the rect in the list or not
    for r in reclist:
        if rec.colliderect(r)==True and rec!=r:
            return True
    return False
#direction: a cooridinate [x,y] that represents the direction that AI will go. for example, [-1,-1] means going left and up
def getdirect(ex,ey,sx,sy):     #return all the possible direction that will go
    d=[note(sx-ex),note(sy-ey)] #let d be the main direction
    if abs(sx-ex)<51:   #
        d[0]=0          #avoiding the AI changing the direction
    if abs(sy-ey)<51:   #too frequently
        d[1]=0          #
    if d[0]==0:
        return [d]+[[-1,d[1]],[1,d[1]]]#
    if d[1]==0:
        return [d]+[[d[0],1],[d[0],-1]]#returns a 2dlist of the main direction and two other dorections on its side. for example:[[0,-1],[-1,-1],[1,-1]]
    if d[0]==d[1] or d[0]==-d[1]:
        return [d]+[[0,d[1]],[d[0],0]] #
def choosedirect(d,sx,sy,ex,ey,exlist,eylist,blockrect,enemysize,ve):#check which direction in the 2dlist from getdirect() works and return it
    direct=d[:]
    erectlist=[0]*len(exlist)
    for i in range(len(exlist)):
        erectlist[i]=midpointrect(exlist[i],eylist[i],enemysize,enemysize)#list of all enemys
    for i in range(3):
        ox,oy=ex,ey
        x,y=AImove(sx,sy,ex,ey,ve,direct[i])
        if collideanyrect(midpointrect(x,y,enemysize,enemysize),remove(erectlist+blockrect,midpointrect(ox,oy,enemysize,enemysize)))==True:#if it doesnt work after 
            direct[i]=0                                                                                                                    #the move,remove the direct
    for i in range(3):
        if direct[i]!=0:#return the first direction that works
            return direct[i]
        if i==2:#if none of them works,AI should not move
            return [0,0]
def AImove(sx,sy,ex,ey,ve,direct):                              #moves AI by using the direction got from
    global enemyatkrange , selfsize, enemysize , enemystatus    #choosedirect()
    if abs(direct[0])==abs(direct[1])==1:
        ex+=int(ve*direct[0]/(2**(1/2)))#keep the speed constant
        ey+=int(ve*direct[1]/(2**(1/2)))
    elif direct[0]==0:
        ey+=ve*direct[1]
    elif direct[1]==0:
        ex+=ve*direct[0]
    return ex,ey
def moveself(mapselfx,mapselfy,exlist,eylist,esize,blockrect):#move the character with keyboard
    mapox,mapoy=mapselfx,mapselfy
    global selfsize,selfdirectionx,selfdirectiony,vself,keys
    if keys[K_UP]:
            selfdirectiony=-1
    if keys[K_DOWN]:
            selfdirectiony=1
    if keys[K_RIGHT]:
            selfdirectionx=1
    if keys[K_LEFT]:
            selfdirectionx=-1
    if abs(selfdirectionx)==abs(selfdirectiony)==1:
        mapselfx+=int(selfdirectionx*vself/(2**0.5))#keep the speed constant
        mapselfy+=int(selfdirectiony*vself/(2**0.5))
    else:
        mapselfx+=int(selfdirectionx*vself)
        mapselfy+=int(selfdirectiony*vself)
    erectlist=exlist[:]
    for i in range(len(exlist)):
        erectlist[i]=midpointrect(exlist[i],eylist[i],esize,esize)
    if collideanyrect(midpointrect(mapselfx,mapselfy,selfsize,selfsize),erectlist+blockrect)==True:
        return mapox,mapoy
    return mapselfx,mapselfy
def backtorange(mpselfx,mpselfy,selfsize,mapsize):#anything that is out of the map will be pull back to the map
    if mpselfx<selfsize//2:
        mpselfx=selfsize//2
    if mpselfx+selfsize//2>mapsize[0]:
        mpselfx=mapsize[0]-selfsize//2
    if mpselfy<selfsize//2:
        mpselfy=selfsize//2
    if mpselfy+selfsize//2>mapsize[1]:
        mpselfy=mapsize[1]-selfsize//2
    return mpselfx,mpselfy
def screenoutputdata(mpselfx,mpselfy,mpenemyx,mpenemyy,mptreex,mptreey,mpblock,mapsize,knife):          #change everything from the coordinate on the map to 
    scrmpx,scrmpy,scrselfx,scrselfy,screnemyx,screnemyy,scrtreex,scrtreey,scrblock=0,0,0,0,[],[],[],[],[]#the cooridinate on the actual screen
    global resolution,selfsize,enemysize
    if mpselfx<resolution[0]//2:                   #find out the scr coordinate of the character
        scrselfx=mpselfx
    elif mapsize[0]-mpselfx<resolution[0]//2:
        scrselfx=resolution[0]-(mapsize[0]-mpselfx)
    else:
        scrselfx=resolution[0]//2
    if mpselfy<resolution[1]//2:
        scrselfy=mpselfy
    elif mapsize[1]-mpselfy<resolution[1]//2:
        scrselfy=resolution[1]-(mapsize[1]-mpselfy)
    else:
        scrselfy=resolution[1]//2                   #############################################
    scrmpx,scrmpy=scrselfx-mpselfx,scrselfy-mpselfy#change everything else
    for n in knife:
        n[4],n[5]=n[2]+scrmpx,n[3]+scrmpy
    for i in range(len(mptreex)):
        scrtreex.append(scrmpx+mptreex[i])
        scrtreey.append(scrmpy+mptreey[i])
        scrblock.append(treeblockrect(scrmpx+mptreex[i],scrmpy+mptreey[i]))
    for i in range(len(mpenemyx)):
        screnemyx.append(scrmpx+mpenemyx[i])
        screnemyy.append(scrmpy+mpenemyy[i])
    return mpselfx,mpselfy,scrmpx,scrmpy,scrselfx,scrselfy,screnemyx,screnemyy,scrtreex,scrtreey,scrblock,knife
def directgetatked(sx,sy,sz,ex,ey,ez):#returns a direction that the AI is atk later
    if midpointrect(sx,sy,sz,sz).colliderect(midpointrect(ex,ey,3*ez,3*ez))==True:#if character in atkrange
       cr=[]
       for x in range(3):
           for y in range(3):
               if midpointrect(ex+(x-1)*ez,ey+(y-1)*ez,ez,ez).colliderect(midpointrect(sx,sy,sz,sz))==True:
                   cr.append([x-1,y-1])
       return cr[0]
    return False
def globfolder(name):#globals all the folder under a certain folder(it can also be "" which means the main folder)
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
def directinstr(status):#trun a direction in coordinate form into a var which relates to a certain position in sprite pics list
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
def checkallclear():#check if all enemies are dead
    if len(mapenemyx)==0:
        return True
    return False
def characterblit(ima,pt,lock,sz):#blit character/enemy sprite with a corner(tl,tr,dl,dr,mid) locked
    x=pt[0]#pt is the midpoint of character/enemy/knife
    y=pt[1]
    l=sz[0]
    h=sz[1]
    if lock=="tl":
        screen.blit(ima,(x-l//2,y-h//2))
    if lock=="tr":
        btrx,btry=x+l//2,y-h//2
        screen.blit(ima,(btrx-ima.get_width(),btry))
    if lock=="dl":
        dlx=x-l//2
        dly=y+h//2
        screen.blit(ima,(dlx,dly-ima.get_height()))
    if lock=="dr":
        drx=x+l//2
        dry=y+h//2
        screen.blit(ima,(drx-ima.get_width(),dry-ima.get_height()))
    if lock=="mid":
        screen.blit(ima,(x-ima.get_width()//2,y-ima.get_height()//2))
def mode(status,cha):#return the mode of character/enemy in a string and them turn it into a number by using the sprmode list
    global selfsprmode
    global enesprmode
    if cha=="self":
        mo=""
        if status[5]==0:
            mo=mo+"blade"
        elif status[5]==1:
            mo=mo+"dart"
        mo=mo+status[4]
        return selfsprmode.index(mo)
    elif cha=="enemy":
        return enesprmode.index(status[4])
def enesprsize(status):#the size of the enemy sprite changes when the direction is not the same so this function use direction to adjust the size of the enemy
    if (status[0],status[1])!=(0,0):
        if status[1]==0:
            return (130,61)
        elif status[0]==0:
            return (110,127)
        else:
            return (130,130)
def enemygenerater():#generate enemies in random position for each round
    global mapselfx,mapselfy,mapblockrect,gamelevel
    n=2+gamelevel*1#number of enemies
    counter=0
    enex,eney=[],[]
    while True:
        x,y=randint(0,mapsize[0]),randint(0,mapsize[1])
        for r in mapblockrect:
            if midpointrect(x,y,enemysize,enemysize).colliderect(r)==False:
                counter+=1
        for i in range(len(enex)):
            if midpointrect(x,y,enemysize,enemysize).colliderect(midpointrect(enex[i],eney[i],enemysize,enemysize))==False:
                counter+=1
        if midpointrect(x,y,enemysize,enemysize).colliderect(midpointrect(mapselfx,mapselfy,selfsize,selfsize))==False:
            counter+=1
        if counter==len(mapblockrect)+len(enex)+1 and (abs(x-mapselfx)>400 or abs(y-mapselfy)>300):#if no enemies overlaps. no enemy--tree overlaps and enemy is not in the screen
            enex.append(x)
            eney.append(y)
        counter=0
        if len(enex)==n:
            return enex,eney
def drawself():#draw the character
    if (frameselfstatus[0],frameselfstatus[1])!=(0,0):
        scrframe=selfpic[directinstr(frameselfstatus)][mode(selfstatus,"self")]#select the list of pictures acording to the mode and the direction of the character
        characterblit(scrframe[frameselfstatus[3]],(scrselfx,scrselfy),lock[directinstr(frameselfstatus)][mode(selfstatus,"self")],(70,100))
        if frameselfstatus[2]==0:
            frameselfstatus[2]+=selfframedelay#delay the bliting so it will not be extremly fast
            frameselfstatus[3]=(frameselfstatus[3]+1) % len(scrframe)#sprites are in a loop
    if frameselfstatus[2]>0:
        frameselfstatus[2]-=1
def drawenemy():#draw all the enemies and it works the same way as drawself()
    for i in range(len(screnemyx)):
        if (frameenemystatus[i][0],frameenemystatus[i][1])!=(0,0):
            scrframe=enemypic[directinstr(frameenemystatus[i])][mode(enemystatus[i],"enemy")]
            characterblit(scrframe[frameenemystatus[i][3]],(screnemyx[i],screnemyy[i]),enemylock[directinstr(frameenemystatus[i])][mode(enemystatus[i],"enemy")],enesprsize(frameenemystatus[i]))
            if frameenemystatus[i][2]==0:
                frameenemystatus[i][2]+=enemyframedelay
                frameenemystatus[i][3]=(frameenemystatus[i][3]+1) % len(scrframe)
        if frameenemystatus[i][2]>0:
            frameenemystatus[i][2]-=1
def drawknife():#draw all the knifes in the air
    for n in selfknife:
        scrframe=selfpic[directinstr(n)][11][0]#11 means mode("knife")
        characterblit(scrframe,(n[4],n[5]),"mid",(50,50))#size really dosenot matter because lock is "mid"
        n[6]+=1
        if n[6]>kniferange:
            del selfknife[selfknife.index(n)]
def drawhpbar():#draw the health bar on the screen
    screen.blit(hpbarpic,(47,24))
    draw.rect(screen,(16,248,216),(94,30,selfstatus[2]/1.0/selfhp*120,12),0)
    hpprint=hpfont.render("%-5i"%(selfstatus[2]), True, (0, 0, 0))
    screen.blit(hpprint,(90,50))
    hpprint=hpfont.render("/", True, (0, 0, 0))
    screen.blit(hpprint,(145,50))
    hpprint=hpfont.render("%-5i"%(selfhp), True, (0, 0, 0))
    screen.blit(hpprint,(180,50))
def drawround():#draw the round number on the screen
    roundnum=hpfont.render("ROUND %i"%(gamelevel), True, (255, 0, 0))
    screen.blit(roundnum,(600,20))
def drawbladeblock():#whenever "blade block" works, it will tell the player by showing him/her the word "block" on the top of the character
    global showblock
    for i in range(len(showblock)):
        if showblock[i]>0:
            screen.blit(bladeblockpic,(scrselfx-50,scrselfy-100))
            showblock[i]-=1
def AIgetkilled(i):#if an AI get killed, remove all the data about it
    del mapenemyx[i],mapenemyy[i],screnemyx[i],screnemyy[i],enemystatus[i],frameenemystatus[i]
    enemydeadsound.play()
def selfmodechanging():#change the type of motion of the character based on the keyboard action
    global selfstatus,scrmode,frameselfstatus
    if selfstatus[2]<=0:
        selfstatus[4]="dead"
        selfstatus[2]=0
        frameselfstatus[3]=0#avoid crushing
    if selfstatus[3]==0 and selfstatus[4]!="dead":
        if keys[K_a] and not okeys[K_a]:#switch weapon
            selfstatus[5]+=1
            selfstatus[5]=selfstatus[5] % 2
        if keys[K_z] and not okeys[K_z]:#atk
            selfstatus[4]="atk"
            if selfstatus[5]==0:              #the character should not atk "continueously" and it should be controled by attack speed
                selfstatus[3]+=selfbladeatkcd
            elif selfstatus[5]==1:
                selfstatus[3]+=selfdartatkcd
        elif (keys[K_UP] or keys[K_DOWN] or keys[K_RIGHT] or keys[K_LEFT]):#this is mainly for sprites bliting
            selfstatus[4]="move"
        if (not keys[K_a] and not keys[K_z] and not (keys[K_UP] or keys[K_DOWN] or keys[K_RIGHT] or keys[K_LEFT])) or (selfstatus[4]=="atk" and selfstatus[3]==0):
            selfstatus[4]=""                    #doing nothing                                                                  #makes a break between two atks 
    if selfstatus[3]>0:#stun recover
        selfstatus[3]-=1
    if selfstatus[4]=="dead":
        scrmode="gameover"
        mixer.music.stop()
def enemymodechanging():#change the type of motion of the enemy based on the AI functions
    global enemystatus
    for i in range(len(enemystatus)):
        if enemystatus[i][3]==0 and enemystatus[i][4]!="dead":
            if directgetatked(mapselfx,mapselfy,selfsize,mapenemyx[i],mapenemyy[i],enemysize)==False and enemystatus[i][4]!="preatk":
                enemystatus[i][4]="move"
            if  directgetatked(mapselfx,mapselfy,selfsize,mapenemyx[i],mapenemyy[i],enemysize)!=False and oenemystatus[i][4]!="preatk" and enemystatus[i][3]==0:
                enemystatus[i][4]="preatk"          #give player time to escape
                enemystatus[i][3]+=enemypreatkstun  #
                enemystatus[i][0],enemystatus[i][1]=directgetatked(mapselfx,mapselfy,selfsize,mapenemyx[i],mapenemyy[i],enemysize)[0],directgetatked(mapselfx,mapselfy,selfsize,mapenemyx[i],mapenemyy[i],enemysize)[1]
            if enemystatus[i][4]=="preatk" and enemystatus[i][3]==0:#deal damage
                enemystatus[i][4]="atk"
        if enemystatus[i][2]<=0:
            enemystatus[i][4]="dead"
        if enemystatus[i][3]>0:
            enemystatus[i][3]-=1
        if enemystatus[i][4]=="dead":
            AIgetkilled(i)
            break
def selfrege():#selfregeneration
    global regecounter,selfstatus
    regecounter+=1
    if regecounter>59 and selfstatus[2]<selfhp:
        selfstatus[2]+=1
        regecounter=0
def enemymove():#use choosedirect,getdirect,AImove to move enemy
    global mapenemyx,mapenemyy,enemydirect,enemystatus
    for i in range(len(mapenemyx)):
        if enemystatus[i][4]=="move":
            enemydirect[i]=choosedirect(getdirect(mapenemyx[i],mapenemyy[i],mapselfx,mapselfy),mapselfx,mapselfy,mapenemyx[i],mapenemyy[i],mapenemyx,mapenemyy,mapblockrect,enemysize,venemy)
            enemystatus[i][0],enemystatus[i][1]=enemydirect[i][0],enemydirect[i][1]
            mapenemyx[i],mapenemyy[i]=AImove(mapselfx,mapselfy,mapenemyx[i],mapenemyy[i],venemy,enemydirect[i])
def selfmove():#use moveself() to move the character
    global selfstatus,mapselfx,mapselfy
    if selfstatus[4]=="move":
        mapselfx,mapselfy=moveself(mapselfx,mapselfy,mapenemyx,mapenemyy,enemysize,mapblockrect)
        if (selfdirectionx,selfdirectiony)!=(0,0):
            selfstatus[0],selfstatus[1]=selfdirectionx,selfdirectiony
def getframedata():#get the information from status in order to draw the character/enemy
    global frameselfstatus,frameenemystatus
    if (selfstatus[0],selfstatus[1])!=(0,0):
        frameselfstatus[0],frameselfstatus[1]=selfstatus[0],selfstatus[1]
    for i in range(len(mapenemyx)):
        if (enemystatus[i][0],enemystatus[i][1])!=(0,0):
            frameenemystatus[i][0],frameenemystatus[i][1]=enemystatus[i][0],enemystatus[i][1]
def block():#returns T/F that if block is active or not based on the level of bladeblock
    prob=bladeblock*5
    tem=randint(1,100)
    if tem<=prob:
        return True
    return False
def AIatk():#if mode of enemy is deal damage, deal damage to the same direction of preatk
    global selfstatus,enemystatus,showblock
    for i in range(len(enemystatus)):
        if oenemystatus[i][4]=="preatk" and enemystatus[i][4]=="atk" and selfstatus[4]!="dead":
            enemyatkrect=midpointrect(mapenemyx[i]+enemystatus[i][0]*enemysize,mapenemyy[i]+enemystatus[i][1]*enemysize,enemyatkrange,enemyatkrange)
            tem=block()
            if midpointrect(mapselfx,mapselfy,selfsize,selfsize).colliderect(enemyatkrect)==True and selfstatus[4]!="dead":
                if (selfstatus[5]==0 and tem==False) or selfstatus[5]==1:#if blade block not active or chara is using dart
                    getdamagesound.play()
                    selfstatus[4]="damage"######
                    selfstatus[2]-=enemyatk
                    if selfstatus[2]<0:
                        selfstatus[2]=0
                    selfstatus[3]=enemyatkstun########
            enemystatus[i][3]+=enemyatkcd
            if tem==True and selfstatus[5]==0:
                showblock.append(20)
                blocksound.play()
def dartmodeatk():#check if the dart hit or not in dart mode
    global selfstatus,selfknife,enemystatus,frameenemystatus
    if selfstatus[5]==1 and selfstatus[4]=="atk" and selfstatus[3]==selfdartatkcd-1:#create dart
        selfknife.append([selfstatus[0],selfstatus[1],mapselfx,mapselfy,0,0,0,0])
        knifesound.play()
    for n in selfknife:#move dart
        if n[0]!=0 and n[1]!=0: 
            n[2],n[3]=n[2]+n[0]*vknife/(2**0.5),n[3]+n[1]*vknife/(2**0.5)
        else:
            n[2],n[3]=n[2]+n[0]*vknife,n[3]+n[1]*vknife
        n[7]=midpointrect(n[2],n[3],knifesize,knifesize)
    for n in selfknife:#deals damage
        for i in range(len(mapenemyx)):
            if n[7].colliderect(midpointrect(mapenemyx[i],mapenemyy[i],enemysize,enemysize)):
                hitsound.play()
                enemystatus[i][3]=selfdartatkstun
                enemystatus[i][2]-=selfdartatk
                enemystatus[i][4]="damage"
                frameenemystatus[i][3]=0
                del selfknife[selfknife.index(n)]
                break
def blademodeatk():#checks if deals damage to enemy on blade mode
    global selfstatus, enemystatus, frameenemystatus,mapselfatkrect
    if selfstatus[4]=="atk" and selfstatus[5]==0:
        mapselfatkrect=midpointrect(mapselfx+selfstatus[0]*selfsize,mapselfy+selfstatus[1]*selfsize,selfatkrange,selfatkrange)
        if selfstatus[3]==10:
            bladesound.play()
    if mapselfatkrect!=0:
        for i in range(len(mapenemyx)):
            if selfstatus[5]==0 and mapselfatkrect.colliderect(midpointrect(mapenemyx[i],mapenemyy[i],enemysize,enemysize))==True and oselfstatus[4]!="atk" and selfstatus[4]=="atk":
                hitsound.play()
                enemystatus[i][3]=selfbladeatkstun
                enemystatus[i][2]-=selfbladeatk
                enemystatus[i][4]="damage"
                selfstatus[2]+=bladelifesteal*4
                if selfstatus[2]>selfhp:
                    selfstatus[2]=selfhp
                frameenemystatus[i][3]=0
def allbacktorange():#use backtorange to both enemy and character
    global mapselfx,mapselfy,mpenenyx,mpenemyy
    mapselfx,mapselfy=backtorange(mapselfx,mapselfy,selfsize,mapsize)
    for i in range(len(mapenemyx)):
        mapenemyx[i],mapenemyy[i]=backtorange(mapenemyx[i],mapenemyy[i],enemysize,mapsize)
def framereset():#reset the framepic position everytime the mode changes so it wont crush
    global frameselfstatus,frameenemystatus
    for i in range(len(enemystatus)):
        if enemystatus[i][4]!=oenemystatus[i][4]:
            frameenemystatus[i][3]=0
    if selfstatus[4]!=oselfstatus[4]:
        frameselfstatus[3]=0
def levelupreset():#update the datas of the character after levelup the skills
    global mapx,mapy,mapselfx,mapselfy,mapselfox,mapselfoy,mapselfatkrect,scrselfx,scrselfy,selfknife,maptreex,maptreey,scrtreex,scrtreey,mapblockrect,scrblockrect
    global mapenemyx,mapenemyy,mapenemyox,mapenemyoy,screnemyx,screnemyy,vself,venemy,vknife,selfsize,enemysize,selfhp,enemyhp,selfstatus,enemystatus,oenemystatus
    global selfatkrange,enemyatkrange,selfbladeatkcd,selfdartatkcd,selfbladeatkstun,selfdartatkstun,enemypreatkstun,enemyatkcd,enemyatkstun,knifesize,kniferange,selfdirectionx,selfdirectiony
    global enemyatk,selfbladeatk,selfdartatk,mapsize,selflevel,gamelevel,enemydirect,frameselfstatus,selfframedelay,frameenemystatus,enemyframedelay
    global bladepowerup,bladestun,bladelifesteal,bladeblock,dartpowerup,dartatkspeedup,dartstun,dartrangeup,movespeedup,movespeedupcredit,maxhp
    vself=4+movespeedup*2
    selfhp=100+maxhp*30

    selfdartatkcd=int(27/1.0/(dartatkspeedup*0.6+1))


    selfbladeatkstun=30+bladestun*15
    selfdartatkstun=15+dartstun*8
    kniferange=10+dartrangeup*3
    selfbladeatk=40+bladepowerup*6
    selfdartatk=20+dartpowerup*5
def allreset():#reset everything when you restart the game
    global mapx,mapy,mapselfx,mapselfy,mapselfox,mapselfoy,mapselfatkrect,scrselfx,scrselfy,selfknife,maptreex,maptreey,scrtreex,scrtreey,mapblockrect,scrblockrect
    global mapenemyx,mapenemyy,mapenemyox,mapenemyoy,screnemyx,screnemyy,vself,venemy,vknife,selfsize,enemysize,selfhp,enemyhp,selfstatus,enemystatus,oenemystatus
    global selfatkrange,enemyatkrange,selfbladeatkcd,selfdartatkcd,selfbladeatkstun,selfdartatkstun,enemypreatkstun,enemyatkcd,enemyatkstun,knifesize,kniferange,selfdirectionx,selfdirectiony
    global enemyatk,selfbladeatk,selfdartatk,mapsize,selflevel,gamelevel,enemydirect,frameselfstatus,selfframedelay,frameenemystatus,enemyframedelay
    global bladepowerup,bladestun,bladelifesteal,bladeblock,dartpowerup,dartatkspeedup,dartstun,dartrangeup,movespeedup,movespeedupcredit,maxhp
    mapx,mapy=0,0
    mapselfx,mapselfy=400,300
    mapselfox,mapselfoy=0,0
    mapselfatkrect=0
    scrselfx,scrselfy=0,0
    selfknife=[]
    maptreex,maptreey=[],[]
    scrtreex,scrtreey=[],[]
    mapblockrect=[]
    scrblockrect=[]
    mapenemyx,mapenemyy=[],[]
    mapenemyox,mapenemyoy=[],[]
    screnemyx,screnemyy=[],[]
    for i in range(len(blockpos)):
        if i%2==0:
            maptreex.append(int(blockpos[i]))
            mapblockrect.append(treeblockrect(int(blockpos[i]),int(blockpos[i+1])))
        else:
            maptreey.append(int(blockpos[i]))
    vself=4
    venemy=2
    vknife=20
    selfsize=50
    enemysize=60
    selfhp=100
    enemyhp=100
    selfatkrange=80
    enemyatkrange=75
    selfbladeatkcd=20
    selfdartatkcd=27
    selfbladeatkstun=15#stun the enemy
    selfdartatkstun=15
    enemypreatkstun=25#stun enemy itself
    enemyatkcd=14
    enemyatkstun=15
    knifesize=30
    kniferange=10
    selfdirectionx,selfdirectiony=0,0
    enemyatk=10
    selfbladeatk=40
    selfdartatk=20
    gamelevel=1
    mapsize=(4000,3000)
    mapenemyx,mapenemyy=enemygenerater()
    selfstatus=[1,0,selfhp,0,"",0]#0 dx,1 dy,2 hp,3 stuntime,4 mode,5.blade(0)or dart(1) !!!!and mode can be "atk" "move" "dead"
    enemystatus,oenemystatus=[0]*len(mapenemyx),[0]*len(mapenemyx)
    for i in range(len(mapenemyx)):
        enemystatus[i]=[1,0,enemyhp,0,""]#0 dx,1 dy,2 hp,3 stuntime,4 mode !!!!and mode can be "preatk"(allow player to escape) "atk" "move" "dead"
    scrtreex,scrtreey=[0]*len(maptreex),[0]*len(maptreex)
    mapenemyox,mapenemyoy,screnemyx,screnemyy,enemydirect=[0]*len(mapenemyx),[0]*len(mapenemyx),[0]*len(mapenemyx),[0]*len(mapenemyx),[0]*len(mapenemyx)
    scrblockrect=scrtreex
    frameselfstatus=[0,0,0,0]#dx,dy,frstun,frame
    selfframedelay=5
    frameenemystatus=[0]*len(mapenemyx)
    for i in range(len(mapenemyx)):
        frameenemystatus[i]=[0,0,0,0]#dx,dy,frstun,frame
    bladepowerup=0
    bladestun=0
    bladelifesteal=0
    bladeblock=0
    dartpowerup=0
    dartatkspeedup=0
    dartstun=0
    dartrangeup=0
    movespeedup,movespeedupcredit=0,0#allow to level up every 10 gamelevels else it will be too overpower
    maxhp=0
    mixer.music.load("sound/background.wav")
    mixer.music.play(-1)
def roundreset():#reset the enemys and their status at the beginning of each round
    global mapx,mapy,mapselfx,mapselfy,mapselfox,mapselfoy,mapselfatkrect,scrselfx,scrselfy,selfknife,maptreex,maptreey,scrtreex,scrtreey,mapblockrect,scrblockrect
    global mapenemyx,mapenemyy,mapenemyox,mapenemyoy,screnemyx,screnemyy,vself,venemy,vknife,selfsize,enemysize,selfhp,enemyhp,selfstatus,enemystatus,oenemystatus
    global selfatkrange,enemyatkrange,selfbladeatkcd,selfdartatkcd,selfbladeatkstun,selfdartatkstun,enemypreatkstun,enemyatkcd,enemyatkstun,knifesize,kniferange,selfdirectionx,selfdirectiony
    global enemyatk,selfbladeatk,selfdartatk,mapsize,selflevel,gamelevel,enemydirect,frameselfstatus,selfframedelay,frameenemystatus,enemyframedelay,endingpic,scrmode
    global scrmode,bladepowerup,bladestun,bladelifesteal,bladeblock,dartpowerup,dartatkspeedup,dartstun,dartrangeup,movespeedup,movespeedupcredit,maxhp
    endingpic=screen.subsurface(Rect(0,0,800,600)).copy()
    venemy=2+0.08*gamelevel
    if venemy>5:
        venemy=5
    enemyhp=100+8*gamelevel
    enemyatkcd=14
    enemyatk=10+0.5*gamelevel
    gamelevel+=1
    mapenemyx,mapenemyy=enemygenerater()
    enemystatus,oenemystatus=[0]*len(mapenemyx),[0]*len(mapenemyx)
    for i in range(len(mapenemyx)):
        enemystatus[i]=[1,0,enemyhp,0,""]#0 dx,1 dy,2 hp,3 stuntime,4 mode !!!!and mode can be "preatk"(allow player to escape) "atk" "move" "dead"
        oenemystatus[i]=[1,0,enemyhp,0,""]
    mapenemyox,mapenemyoy,screnemyx,screnemyy,enemydirect=[0]*len(mapenemyx),[0]*len(mapenemyx),[0]*len(mapenemyx),[0]*len(mapenemyx),[0]*len(mapenemyx)
    frameenemystatus=[0]*len(mapenemyx)
    for i in range(len(mapenemyx)):
        frameenemystatus[i]=[0,0,0,0]#dx,dy,frstun,frame
    scrmode="levelup"
    if gamelevel%5==0 and ogamelevel!=gamelevel:#every 5 level you get a credit
        movespeedupcredit+=1
    levelupsound.play()
def levelup():#the levelup screen of the game
    global scrmode,bladepowerup,bladestun,bladelifesteal,bladeblock,dartpowerup,dartatkspeedup,dartstun,dartrangeup,movespeedup,movespeedupcredit,maxhp
    n=0
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    if Rect(0,100,400,100).collidepoint(mx,my)==True:
        n=1
    elif Rect(0,200,400,100).collidepoint(mx,my)==True and bladestun<20:    #skill level cannot exccede a certain number
        n=2
    elif Rect(0,300,400,100).collidepoint(mx,my)==True:
        n=3
    elif Rect(0,400,400,100).collidepoint(mx,my)==True and bladeblock<15:
        n=4
    elif Rect(0,500,400,100).collidepoint(mx,my)==True and movespeedupcredit>0:#have to have a movespeedupcredit to levelup the skill
        n=5
    elif Rect(400,100,400,100).collidepoint(mx,my)==True:
        n=6
    elif Rect(400,200,400,100).collidepoint(mx,my)==True and dartatkspeedup<10:
        n=7
    elif Rect(400,300,400,100).collidepoint(mx,my)==True and dartstun<20:
        n=8
    elif Rect(400,400,400,100).collidepoint(mx,my)==True:
        n=9
    elif Rect(400,500,400,100).collidepoint(mx,my)==True:
        n=10
    else:
        n=0
    if mb[0]==1 and omb[0]!=1:
        if n==1:
            bladepowerup+=1
        if n==2 and bladestun<20:
            bladestun+=1
        if n==3:
            bladelifesteal+=1
        if n==4 and bladeblock<15:
            bladeblock+=1
        if n==5 and movespeedupcredit>0:
            movespeedup+=1
            movespeedupcredit-=1
        if n==6:
            dartpowerup+=1
        if n==7 and dartatkspeedup<10:
            dartatkspeedup+=1
        if n==8 and dartstun<20:
            dartstun+=1
        if n==9:
            dartrangeup+=1
        if n==10:
            maxhp+=1
        if n!=0:
            yessound.play()
    levelupreset()
    if mb[0]==1 and omb[0]!=1 and n!=0:
        scrmode="mainloop"
    screen.blit(endingpic,(0,0))
    screen.blit(leveluppic[n],(0,0))
    display.flip()
def menu():#the main menu of the game
    global scrmode
    n=0
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    if Rect(200,200,400,100).collidepoint(mx,my)==True:
        n=1
        if mb[0]==1 and omb[0]!=1:
            scrmode="mainloop"
            allreset()
    elif Rect(200,300,400,100).collidepoint(mx,my)==True:
        n=2
        if mb[0]==1 and omb[0]!=1:
            scrmode="help"
    elif Rect(200,400,400,100).collidepoint(mx,my)==True:
        n=3
        if mb[0]==1 and omb[0]!=1:
            scrmode="story"
    else:
        n=0
    screen.blit(menupic[n],(0,0))
    display.flip()

def gameover():#the game over screen of the game
    global scrmode
    n=0
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    if Rect(200,300,400,260).collidepoint(mx,my)==True:
        n=0
        if mb[0]==1 and omb[0]!=1:
            scrmode="menu"
    else:
        n=1
    screen.blit(gameoverpic[n],(0,0))
    display.flip()
def helpscr():#the help screen of the game
    global scrmode
    n=0
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    if Rect(528,512,233,88).collidepoint(mx,my)==True:
        n=2
        if mb[0]==1 and omb[0]!=1:
            scrmode="menu"
    elif Rect(78,512,233,88).collidepoint(mx,my)==True:
        n=0
        if mb[0]==1 and omb[0]!=1:
            scrmode="skillscr"
    else:
        n=1
    screen.blit(helppic[n],(0,0))
    display.flip()
def story():#the story screen
    global scrmode
    n=0
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    if Rect(518,513,233,88).collidepoint(mx,my)==True:
        n=1
        if mb[0]==1 and omb[0]!=1:
            scrmode="menu"
    else:
        n=0
    screen.blit(storypic[n],(0,0))
    display.flip()
def skillscr():#the skill explanation screen
    global scrmode
    n=0
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    if Rect(518,512,233,88).collidepoint(mx,my)==True:
        n=1
        if mb[0]==1 and omb[0]!=1:
            scrmode="help"
    else:
        n=0
    screen.blit(skillpic[n],(0,0))
    display.flip()
def mainloop():#the main program of the game
    global mapselfatkrect,keys,mapselfx,mapselfy,mapx,mapy,scrselfx,scrselfy,screnemyx,screnemyy,scrtreex,scrtreey,scrblockrect,selfknife
    global mapselfox,mapselfoy,mapenemyox,mapenemyoy,okeys,selfdirectionx,selfdirectiony,oselfstatus,oenemystatus
    mapselfox,mapselfoy=mapselfx,mapselfy
    mapenemyox,mapenemyoy=mapenemyx[:],mapenemyy[:]
    okeys=keys[:]
    ogamelevel=gamelevel
    selfdirectionx,selfdirectiony=0,0
    oselfstatus=selfstatus[:]
    for i in range(len(enemystatus)):
        oenemystatus[i]=enemystatus[i][:] 
    mapselfatkrect=0
    keys = key.get_pressed()
    #####map analyzing#####
    nuke()
    if checkallclear()==True:
        roundreset()
    selfmodechanging()
    enemymodechanging()
    selfrege()
    enemymove()
    selfmove()
    AIatk()
    dartmodeatk()
    blademodeatk()
    allbacktorange()
    framereset()
    #------------------start drawing everything------------#
    getframedata()
    mapselfx,mapselfy,mapx,mapy,scrselfx,scrselfy,screnemyx,screnemyy,scrtreex,scrtreey,scrblockrect,selfknife=screenoutputdata(mapselfx,mapselfy,mapenemyx,mapenemyy,maptreex,maptreey,mapblockrect,mapsize,selfknife)
    screen.fill((0,0,0))
    screen.blit(gamemap,(mapx,mapy))
    for i in range(len(scrtreex)):
        screen.blit(treepic,(scrtreex[i],scrtreey[i]+200))
    drawself()
    drawknife()
    drawenemy()
    for i in range(len(scrtreex)):
        screen.blit(ballpic,(scrtreex[i],scrtreey[i]))
    drawhpbar()
    drawround()
    drawbladeblock()
    myClock.tick(tick)
    display.flip()

    
#-------------------initiating------------------------#
myClock = time.Clock()
running=True
font.init()
init()
hpfont = font.SysFont("Rosewood Std", 35)
resolution=(800,600)
screen =display.set_mode(resolution)
blockpos=open("blockpos.txt").read().strip().split()#all the positions of the tree
keys = key.get_pressed()
mb=mouse.get_pressed()
omb=mouse.get_pressed()
#-------------------end of initiating-----------------#
#--------------------loading sound-----------------------#
getdamagesound=mixer.Sound("sound/getdamage.wav")
hitsound=mixer.Sound("sound/hit.wav")
knifesound=mixer.Sound("sound/knife.wav")
levelupsound=mixer.Sound("sound/levelup.wav")
bladesound=mixer.Sound("sound/blade.wav")
yessound=mixer.Sound("sound/yes.wav")
blocksound=mixer.Sound("sound/block.wav")
enemydeadsound=mixer.Sound("sound/enemydead.wav")
#-------------------loading image----------------------#
gamemap=image.load("mapbase.png").convert_alpha()
treepic=image.load("tree.png").convert_alpha()
ballpic=image.load("ball.png").convert_alpha()
hpbarpic=image.load("hpbar.png").convert_alpha()
bladeblockpic=image.load("block.png").convert_alpha()
menupic,helppic,storypic,leveluppic,gameoverpic,skillpic=[],[],[],[],[],[]
for i in range(4):
    menupic.append(image.load("menu/menu"+str(i)+".png"))
for i in range(3):
    helppic.append(image.load("help/help"+str(i)+".png"))
for i in range(2):
    storypic.append(image.load("story/story"+str(i)+".png"))
for i in range(11):
    leveluppic.append(image.load("levelup/levelup"+str(i)+".png"))
for i in range(2):
    gameoverpic.append(image.load("gameover/gameover"+str(i)+".png"))
for i in range(2):
    skillpic.append(image.load("skill/skill"+str(i)+".png"))
ninjafoldername,enefoldername=globfolder("ninja"),globfolder("enemy")
for i in range(len(ninjafoldername)):
    ninjafoldername[i]=ninjafoldername[i].replace("\\","/")
for i in range(len(enefoldername)):
    enefoldername[i]=enefoldername[i].replace("\\","/")
up,upright,right,downright,down,downleft,left,upleft=0,1,2,3,4,5,6,7
selfsprmode=['blade', 'bladeatk', 'bladecharge', 'bladedamage', 'bladedead', 'blademove', 'dart', 'dartatk', 'dartdamage', 'dartdead', 'dartmove', 'knife']
#'0blade', '1bladeatk', '2bladecharge', '3bladedamage', '4bladedead', '5blademove', '6dart', '7dartatk', '8dartdamage', '9dartdead', '10dartmove', '11knife'
enesprmode=["atk","damage","move","preatk"]
#"0atk","1damage","2move","3preatk"
selfpic,lock,enemypic,enemylock=[0]*8,[0]*8,[0]*8,[0]*8
for n in ninjafoldername:
    selfpic[eval(n[n.index("/")+1:])]=globfolder(n)
    lock[eval(n[n.index("/")+1:])]=globfolder(n)
for x in range(len(selfpic)):                                           #global loading all the enemy/character image and corner lock
    for y in range(len(selfpic[x])):
        selfpic[x][y]=glob(selfpic[x][y]+"/*.png")
        lock[x][y]=open(lock[x][y]+"/lock.txt").read().strip()
for x in range(len(selfpic)):
    for y in range(len(selfpic[x])):
        for z in range(len(selfpic[x][y])):
            selfpic[x][y][z]=image.load(selfpic[x][y][z]).convert_alpha()
for n in enefoldername:
    enemypic[eval(n[n.index("/")+1:])]=globfolder(n)
    enemylock[eval(n[n.index("/")+1:])]=globfolder(n)
for x in range(len(enemypic)):
    for y in range(len(enemypic[x])):
        enemypic[x][y]=glob(enemypic[x][y]+"/*.png")
        enemylock[x][y]=open(enemylock[x][y]+"/lock.txt").read().strip()
for x in range(len(enemypic)):
    for y in range(len(enemypic[x])):
        for z in range(len(enemypic[x][y])):
            enemypic[x][y][z]=image.load(enemypic[x][y][z]).convert_alpha()
#-------------------end of loading image---------------#
#------------------position defining------------------#
#naming rule:frame+object+type of coordinate
mapx,mapy=0,0
#character
mapselfx,mapselfy=400,300
mapselfox,mapselfoy=0,0
mapselfatkrect=0
scrselfx,scrselfy=0,0
selfknife=[]#element:[0,0,0,0,0,0,0,0]dx,dy,mapx,mapy,scrx,scry,time,atkrect
#tree
maptreex,maptreey=[],[]
scrtreex,scrtreey=[],[]
#block
mapblockrect=[]
scrblockrect=[]
#enemy
mapenemyx,mapenemyy=[],[]
mapenemyox,mapenemyoy=[],[]
screnemyx,screnemyy=[],[]
#------------------end of pos defining----------------#
#------------------load vars---------------------#
for i in range(len(blockpos)):
    if i%2==0:
        maptreex.append(int(blockpos[i]))
        mapblockrect.append(treeblockrect(int(blockpos[i]),int(blockpos[i+1])))
    else:
        maptreey.append(int(blockpos[i]))
#----------------end of load var-----------------#
#----------------defining game data--------------------#
vself=5
venemy=2
vknife=20
selfsize=50
enemysize=60
selfhp=50
enemyhp=100
selfatkrange=75
enemyatkrange=75
selfbladeatkcd=25
selfdartatkcd=25
selfatkstun=20#stun the enemy
enemypreatkstun=25#stun enemy itself before atk
enemyatkcd=14
enemyatkstun=20
knifesize=30
kniferange=15
selfdirectionx,selfdirectiony=0,0
enemyatk=10
selfbladeatk=20
selfdartatk=10
selflevel=0
tick=60
regecounter=0
gamelevel=1
ogamelevel=1
mapsize=(4000,3000)
mapenemyx,mapenemyy=enemygenerater()
selfstatus=[1,0,selfhp,0,"",0]#0 dx,1 dy,2 hp,3 stuntime,4 mode,5.blade(0)or dart(1) !!!!and mode can be "atk" "move" "dead"
enemystatus,oenemystatus=[0]*len(mapenemyx),[0]*len(mapenemyx)
for i in range(len(mapenemyx)):
    enemystatus[i]=[1,0,enemyhp,0,""]#0 dx,1 dy,2 hp,3 stuntime,4 mode !!!!and mode can be "preatk"(allow player to escape) "atk" "move" "dead"
scrtreex,scrtreey=[0]*len(maptreex),[0]*len(maptreex)
mapenemyox,mapenemyoy,screnemyx,screnemyy,enemydirect=[0]*len(mapenemyx),[0]*len(mapenemyx),[0]*len(mapenemyx),[0]*len(mapenemyx),[0]*len(mapenemyx)
scrblockrect=scrtreex
endingpic=0
showblock=[]# the list of block fonts
####skills####
bladepowerup=0
bladestun=0
bladelifesteal=0
bladeblock=0
dartpowerup=0
dartatkspeedup=0
dartstun=0
dartrangeup=0
movespeedup,movespeedupcredit=0,0#allow to level up every 10 gamelevels else it will be too overpower
maxhp=0
#-----------------end of defining game data------------#
#-----------------frame data---------------------------#
scrmode="menu"#can be "menu", "level up", "mainloop", "gameover","skillscr","help","story"
frameselfstatus=[0,0,0,0]#dx,dy,frstun,frame
selfframedelay=5
frameenemystatus=[0]*len(mapenemyx)
for i in range(len(mapenemyx)):
    frameenemystatus[i]=[0,0,0,0]#dx,dy,frstun,frame
enemyframedelay=7
########################################################
#####################   MAIN   #########################
while running:
    for evnt in event.get():                
        if evnt.type == QUIT:
            running = False
    omb=mb[:]
    mb=mouse.get_pressed()
    if scrmode=="menu":
        menu()
    if scrmode=="mainloop":
        mainloop()
    if scrmode=="gameover":
        gameover()
    if scrmode=="help":
        helpscr()
    if scrmode=="story":
        story()
    if scrmode=="levelup":
        levelup()
    if scrmode=="skillscr":
        skillscr()
quit()
#I tried to organize/generalize my code as much as possible, but after making the basic structure, I just cannot hold the structure
#while adding new things, so it comes out pretty messy as what i have now.
#all the images, musics, and sound effects are from SEGA's GBA game "Shining Soul II"

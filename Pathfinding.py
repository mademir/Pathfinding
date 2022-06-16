import os
import pygame
from time import sleep

lc=(150,150,0)#line color

sdict={"W":(-1,0),"E":(1,0),"N":(0,-1),"S":(0,1)}


n,nx=[25,25]#nxn tiles, each nx pixels
n=int(n)
nx=int(nx)
closedcolor=(10,10,10)
wallcolor=(150,20,20)
startcolor=(10,200,10)
endcolor=(200,170,50)
pathcolor=(0,200,200)

def flip():
    pygame.display.flip()
    
pygame.init()
pygame.display.set_caption(u'Pathfinding')
scr=pygame.display.set_mode((n*nx, n*nx))

scr.fill((0,34,64)) #background

def line(spos,epos):
    pygame.draw.line(scr,pygame.Color(lc[0],lc[1],lc[2]), spos, epos)

def draw_board(n,nx):
    for i in range(n):
        line((nx*(i+1),0),(nx*(i+1),n*nx))
        line((0,nx*(i+1)),(n*nx,nx*(i+1)))

def check(x,y):
    for i in list(sdict.keys()):
        sx,sy=x,y
        sx+=sdict[i][0]
        sy+=sdict[i][1]
        if not(sy<0 or sy>n-1) and not(sx<0 or sx>n-1):
            if tiles[sx][sy].stat=="e":
                return True
            
def findmd(x,y,opts):
    lastmd=n*n
    for i in opts:
        sx=x+sdict[i][0]
        sy=y+sdict[i][1]
        md=abs(sx-end[0])+abs(sy-end[1])
        if md<lastmd:
            lastmd=md
            way=i
    return way

    
class tile:
    def __init__(self,x,y,stat=None):
        self.x=x
        self.y=y
        self.stat=stat
        self.paint()
        
    def findopts(self):
        opts=[]
        if (not self.x+1>n-1):
            if tiles[self.x+1][self.y].stat==None:opts+="E"
        if (not self.y+1>n-1):
            if tiles[self.x][self.y+1].stat==None:opts+="S"
        if (not self.x-1<0):
            if tiles[self.x-1][self.y].stat==None:opts+="W"
        if (not self.y-1<0):
            if tiles[self.x][self.y-1].stat==None:opts+="N"
        return opts
        
    def paint(self,color=None):
        if not color:
            if self.stat=="w":
                pygame.draw.rect(scr,wallcolor,(self.x*nx,self.y*nx,nx,nx))
            if self.stat=="s":
                pygame.draw.rect(scr,startcolor,(self.x*nx,self.y*nx,nx,nx))
            if self.stat=="e":
                pygame.draw.rect(scr,endcolor,(self.x*nx,self.y*nx,nx,nx))
            if self.stat=="p":
                pygame.draw.rect(scr,pathcolor,(self.x*nx,self.y*nx,nx,nx))
        else:pygame.draw.rect(scr,color,(self.x*nx,self.y*nx,nx,nx))
        flip()

tiles=list(range(n))
for i in range(n):tiles[i] = [tile(i,k) for k in range(n)]

last=[]

draw_board(n,nx)
flip()

ready=0
draw=False
bx,by=0,0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:raise
            if event.key == pygame.K_RETURN:ready=3#ready to start
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ready==0:#place start
                x=event.pos[0]//nx
                y=event.pos[1]//nx
                tiles[x][y].stat="s"
                tiles[x][y].paint()
                start=(x,y)
                bx,by=x,y
                ready+=1
                continue
            if ready==1:#place end
                x=event.pos[0]//nx
                y=event.pos[1]//nx
                if tiles[x][y].stat==None:
                    tiles[x][y].stat="e"
                    tiles[x][y].paint()
                    end=(x,y)
                    ready+=1
                continue
            draw=True
        if event.type == pygame.MOUSEBUTTONUP:
            draw=False
        if (event.type == pygame.MOUSEMOTION) & draw:
            x=event.pos[0]//nx
            y=event.pos[1]//nx
            if tiles[x][y].stat==None:
                tiles[x][y].stat="w"
                tiles[x][y].paint()
        if event.type == pygame.QUIT:
            pygame.quit()
            os._exit(1)
    if ready!=3:continue#if not ready, skip
    opts=tiles[bx][by].findopts()
    if opts==[]:
        bx,by=last[-1]
        last.pop()
        print("jumped!",bx,by)
        continue
    if len(opts)>1:last.append((bx,by))
    print("last",last)
    md=findmd(bx,by,opts)
    bx+=sdict.get(md)[0]
    by+=sdict.get(md)[1]
    tiles[bx][by].stat="p"
    tiles[bx][by].paint()
    if check(bx,by):
        print("FOUND!")
        pygame.quit()
        os._exit(0)
        break
    sleep(0.2)
        
    sleep(0.1)

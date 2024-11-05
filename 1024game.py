import pygame,sys,time,random

pygame.init()
pygame.display.set_caption("1024")
canvas=screen=pygame.display.set_mode((400,400))
color={0:(255,255,255),1:(0,255,0),2:(0,255,255),3:(0,0,255),4:(255,255,0),5:(255,128,0),6:(255,0,255),7:(127,0,255),8:(255,0,127),9:(255,0,0),10:(255,255,255)}
random.seed()
count=0

running=True
class button:
    def __init__(self,x,y,width,height,color):
        self.rect=pygame.Rect(x,y,width,height)
        self.color=color
        self.x=x
        self.y=y
        self.height=height
        self.width=width
    def draw(self,canvas,text1):
        pygame.draw.rect(canvas,self.color,self.rect)
        font=pygame.font.Font(None,40)
        text=font.render(f'{text1}',True,(0,0,0))
        text_rect=text.get_rect()
        text_rect.center=(self.x+50,self.y+25)
        canvas.blit(text,text_rect)
    def is_clicked(self,pos):
        if self.rect.collidepoint(pos):
            return True
        return False

def begin():
    running=True
    canvas.fill(color.get(1))
    but1=button(0,200,100,50,color.get(2))
    but1.draw(canvas,4)
    but2=button(150,200,100,50,color.get(7))
    but2.draw(canvas,5)
    but3=button(300,200,100,50,color.get(9))
    but3.draw(canvas,6)
    font=pygame.font.Font(None,40)
    text=font.render('Select size',True,(0,0,0))
    text_rect=text.get_rect()
    text_rect.center=(200,200-25)
    canvas.blit(text,text_rect)
    pygame.display.flip()
    
    while running:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if but1.is_clicked(event.pos):
                    return 4
                if but2.is_clicked(event.pos):
                    return 5
                if but3.is_clicked(event.pos):
                    return 6
            elif event.type==pygame.QUIT:
                running=False
hard=begin()
canvas=screen=pygame.display.set_mode((hard*100,hard*100))

def zero_to_end(list_target):
    # 选出非零元素 形成新列表
    # [2, 0, 2, 0] -->  [2, 2]
    new_list = []
    for item in list_target:
        if item != 0:
            new_list.append(item)
            # 追加零元素 [2, 2] --> [2,2,0,0]
    # 判断原列表零元素数量： list_target.count(0)
    for i in range(list_target.count(0)):
        new_list.append(0)
        # 返回新列表
    return new_list

def merge(list_target):
    # 1.将零元素移动到末尾 [2,0,2,0]    -->  [2,2,0,0]
    list_target = zero_to_end(list_target)
    # 2. 合并
    for i in range(len(list_target) - 1):
        # 如果非零元素  相邻且相同
        if list_target[i] != 0 and list_target[i] == list_target[i + 1]:
            # 将后一个元素累加到前一个元素上
            list_target[i] += list_target[i + 1]
            # 讲后一个元素清零
            list_target[i + 1] = 0
    # 3. 将零元素移动到末尾  [2,2,2,0]    -->  [4,0,2,0]  -->[4,2,0,0]
    list_target = zero_to_end(list_target)
    return list_target

def print_atlas(list_atlas,first):
    font=pygame.font.Font(None,80)
    k=0
    if first==0:
        rerandom_atlas(list_atlas)
    else:
        random_atlas(list_atlas)
    for r in range(len(list_atlas)):
        for c in range(len(list_atlas[r])):
            po=pygame.Rect(c*100,r*100,100,100)
            if list_atlas[r][c]==0:
                num,k=0,0
                fontpo=(c*100+33,r*100+25)
            else :
                for i in range(1,11): 
                    num=pow(2,i)
                    if i>6:
                        fontpo=(c*100,r*100+25)
                    elif i>3:
                        fontpo=(c*100+20,r*100+25)
                    else:
                        fontpo=(c*100+33,r*100+25)
                    if list_atlas[r][c]==num:
                        k=i
                        break
                    if k==10:
                        finish()
            pygame.draw.rect(canvas,color.get(k),po,100)
            text=font.render(f'{num}',True,(0,0,0))
            canvas.blit(text,fontpo)
            pygame.display.flip()

# 提示：将二维列表每列元素形成一维列表,交给合并merge函数,再还给二维列表
def move_up(atlas):  # 15:30
    # 将二维列表第一列元素形成一维列表,
    # 00  10   20  30
    for c in range(hard):
        list_merge = []
        for r in range(hard):
            list_merge.append(atlas[r][c])

        # 交给合并merge函数
        list_merge = merge(list_merge)

        # 再还给二维列表
        for r in range(hard):
            atlas[r][c] = list_merge[r]
    return atlas

def move_left(atlas):
    for r in range(hard):
        # 从左到右依次获取行
        list_merge = []
        for c in range(hard):
            # 00  01  02  03
            list_merge.append(atlas[r][c])

        list_merge = merge(list_merge)

        for c in range(hard):
            atlas[r][c] = list_merge[c]

    return atlas

def move_down(atlas):
    for c in range(hard):
        list_merge = []
        # 从下至上获取二维列表列元素
        for r in range(hard-1,-1,-1):
            list_merge.append(atlas[r][c])

        list_merge = merge(list_merge)

        # 从左至右获取一维列表元素
        # 从下至上还给二维列表
        for r in range(hard-1, -1, -1):
            atlas[r][c] = list_merge[hard-1 -r]  # 0  1 2 3
    return atlas

def move_right(atlas):
    for r in range(hard):
        list_merge = []
        for c in range(hard-1, -1, -1):
            list_merge.append(atlas[r][c])

        list_merge=merge(list_merge)

        for c in range(hard-1, -1, -1):
            atlas[r][c] = list_merge[hard-1 - c]
    return atlas

def random_atlas(list_atlas):
    for r in range(len(list_atlas)):
        for c in range(len(list_atlas[r])):
            x=random.random()
            if x<0.3:
                list_atlas[r][c]=2
            elif x>=0.3 and x<0.4:
                list_atlas[r][c]=4
            else:
                list_atlas[r][c]=0

def rerandom_atlas(list_atlas):
    for r in range(len(list_atlas)):
        for c in range(len(list_atlas[r])):
            if list_atlas[r][c]==0:
                if random.random()<0.1:
                    list_atlas[r][c]=2
                else:
                    list_atlas[r][c]=0

def finish():
    canvas.fill(color.get(0))
    font=pygame.font.Font(None,40)

    text=font.render('Congradulation to arrival 1024!',True,(0,0,0))
    text_rect=text.get_rect()
    text_rect.center=(hard*100//2,hard*100//2-100)
    canvas.blit(text,text_rect)

    text=font.render('The total step is',True,(0,0,0))
    text_rect=text.get_rect()
    text_rect.center=(hard*100//2,hard*100//2-50)
    canvas.blit(text,text_rect)

    text=font.render(f'{count}',True,(0,0,0))
    text_rect=text.get_rect()
    text_rect.center=(hard*100//2,hard*100//2)
    canvas.blit(text,text_rect)
    pygame.display.flip()
    time.sleep(3.5)
    sys.exit()

atlas=[[0 for i in range(hard)] for k in range(hard)]
print_atlas(atlas,1)
while running:
    for event in pygame.event.get():
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            count+=1
            move_up(atlas)
            print_atlas(atlas,0)
        if keys[pygame.K_DOWN]:
            count+=1
            move_down(atlas)
            print_atlas(atlas,0)
        if keys[pygame.K_RIGHT]:
            count+=1
            move_right(atlas)
            print_atlas(atlas,0)
        if keys[pygame.K_LEFT]:
            count+=1
            move_left(atlas)
            print_atlas(atlas,0)   
        if keys[pygame.K_ESCAPE]:
            running=False 
        if event.type==pygame.QUIT:
            running=False
                
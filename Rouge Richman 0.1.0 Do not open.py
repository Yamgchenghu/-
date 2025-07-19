import os
from pydoc import doc
import sys
import pygame,random,json

##############################################################定义筹码介绍
coins_introductions={
    ##根据下方的筹码名称撰写介绍
    "色子成双":"投掷色子时，若点数为6，则获得2张对应的6","事事顺利":"打出顺子时，倍率+2","蚌埠倍率":"打出炸弹时，倍率*3","连连专家":"打出连对时，金币+50",
    "风险色子":"掷色子时，有50%概率给1点的手牌，否则点数翻倍","金币钟情":"出牌时，倍率+10，步数减半(向下取整)","步数钟情":"出牌时，倍率锁定为1，步数*250%(向下取整)",
    "高牌全带":"打出任意单张时，消耗所有手牌(弃牌)","多一选择":"手牌上限+1，没有其它效果","顺风顺水":"使用顺子到达商店时，获得5000金币，自毁"
    }













def get_base_path():
    """
    获取基础路径，区分开发环境和打包后的环境
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))
def resource_path(relative_path,last=0):
    return os.path.join(get_base_path(), relative_path)


# 导入 dlc.py
try:
    
    # 尝试在开发模式下导入
    import dlc.easy_pygame as dlc
    mode = "开发"
except ImportError:
    # 如果开发模式导入失败，尝试在打包模式下导入
    sys.path.append(resource_path("dlc/easy_pygame",last=0))
    import dlc.easy_pygame as dlc   # 假设打包后的模块名称为 dlc，并且在 dlc 文件夹中
    mode = "封闭"


def get_music_files():
    """获取 music 文件夹中的所有文件名称"""
    class_folder = resource_path('music')
    if os.path.exists(class_folder):
        return os.listdir(class_folder)
    return []
def mopen(file,lx="r",decode="utf-8"):
    return open(resource_path(f'{file}'), lx, encoding=decode)
if '读取配置':
    with mopen('dlc/init.inf') as f:
        init = f.readlines()
        for i in init:
            if i.startswith("bbh="):
                bbh = i.replace("bbh=","").replace("\n","")
            elif i.startswith("screen_size="):
                screen_size = i.replace("screen_size=","").replace("\n","")
            elif i.startswith("music="):
                music = i.replace("music=","").replace("\n","")


if "导入地图文件夹":
    ##导入地图文件夹，获取所有文件名称，存放在maps列表中
    map_folder = resource_path('maps')
    map_files = os.listdir(map_folder)
    map_names = [os.path.splitext(filename)[0] for filename in map_files if filename.endswith('.json')]
    print(map_files,map_names)

if "初始化数据":
    pygame.init()
    
    flips=0

    screen = pygame.display.set_mode([int(screen_size.split('x')[0]),int(screen_size.split('x')[1])])  
    pygame.display.set_caption("肉鸽大富翁")

    music_files = get_music_files()  # 获取 music 文件夹中的所有文件名称
    clock = pygame.time.Clock()

    dlc.autosetwide()
    dlc.mouselineupload(2)

    players = []
    players_names="Normal"
    cs_money = 2000
    cs_money_choice=[2000,2400,2800,3200,3500]

    plr_data = {}
    

    coins_coins=["色子成双","事事顺利","蚌埠倍率","连连专家","风险色子","金币钟情","步数钟情","高牌全带","多一选择","顺风顺水"]
    dice_all_dices={
    "普通色子":{"points":[1,2,3,4,5,6],"addition":0,"price":500,"intro":"最普通的色子，完全没有用。每人初始有3个"},
    "两级色子":{"points":[1,6],"addition":0,"price":1000,"intro":"只有1和6的色子。很极限。"},
    "素数色子":{"points":[2,3,5,7],"addition":0,"price":800,"intro":"10以内的素数。就差11就能凑成素数顺了。"},
    "混沌色子":{"points":[1,2,3,4,5,6,7,8],"addition":1,"price":800,"intro":"出牌后倍率随机*0.5~1.5，每张结算一次"},
    "骰子王":{"points":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],"addition":0,"price":2000,"intro":"最全点数的色子，大部分游戏用于血量展示"},
    "黄金6点":{"points":[6],"addition":2,"price":1200,"intro":"只有6点的色子，很有价值。每次投掷色子有60%自毁。每出一张牌获得50金币(不参与倍率)"},
    "高数色子":{"points":[1,6,11,12,13,14,15],"addition":0,"price":1200,"intro":"1和6,11到15"},
    "我不想走":{"points":[0],"addition":0,"price":500,"intro":"只有0的色子，不会有人买吧"}
    }
    
    
    page = "主界面"
    do = "进入"
    will_do = "主界面"

    players_colors = [
        (240,80,38),
        (240,240,38),
        (80,250,108),
        (80,138,250)
    ]
    show_do=[]

    if "字体":
        dlc.fontupload("font/0.ttf",50,0)
        dlc.fontupload("font/0.ttf",80,1)
        dlc.fontupload("font/0.ttf",30,2)
        dlc.fontupload("font/0.ttf",16,3)
        dlc.fontupload("font/0.ttf",24,4)
        dlc.fontupload("font/0.ttf",12,5)
    
    





while 1:
    flips+=1
    screen.fill((80,80,80))
    dlc.screen_size = screen_size
    if "动画效果":
        if do == "进入":
            if flips%1==0 and dlc.mp4<=49:
                dlc.mp4+=1
            if dlc.mp4==49:
                do = ""
        elif do == "退出":
            if flips%1==0 and dlc.mp4>=1:
                dlc.mp4-=1
            if dlc.mp4==0:
                page = will_do
                do = "进入"
    if page=="主界面":
        dlc.moutput(screen,"肉鸽大富翁",(180,180,188),((int(screen_size.split('x')[0])//2-dlc.mlength("肉鸽大富翁",1)//2),70),num=1,moving=1)
        dlc.moutput(screen,"继续游戏",(180,210,180),((int(screen_size.split('x')[0])//2-dlc.mlength("继续游戏",0)//2),280),num=0,moving=3)
        dlc.moutput(screen,"新的游戏",(180,130,210),((int(screen_size.split('x')[0])//2-dlc.mlength("开始游戏",0)//2),380),num=0,moving=3)
        dlc.moutput(screen,"创建地图",(210,130,180),((int(screen_size.split('x')[0])//2-dlc.mlength("创建地图",0)//2),480),num=0,moving=3)
        #print("---\n",do,dlc.mp4_xy[dlc.mp4])

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    x=e.pos[0]
                    y=e.pos[1]
                    if x>(int(screen_size.split('x')[0])//2-dlc.mlength("继续游戏",0)//2) and x<(int(screen_size.split('x')[0])//2+dlc.mlength("继续游戏",0)//2):
                        if y>380 and y<480:
                            do = "退出"
                            will_do = "重新游戏设定"
                            map_id=0
                    if x>(int(screen_size.split('x')[0])//2-dlc.mlength("新的游戏",0)//2) and x<(int(screen_size.split('x')[0])//2+dlc.mlength("新的游戏",0)//2):
                        if y>480 and y<580:
                            do = "退出"
                            will_do = "地图编辑"
    elif page=="地图编辑":
        dlc.moutput(screen,"编辑地图",(180,180,188),((int(screen_size.split('x')[0])//2-dlc.mlength("编辑地图",1)//2),70),num=1,moving=1)
        dlc.moutput(screen,"返回",(140,140,140),(10,10),num=3,moving=2)
        dlc.moutput(screen,"从零开始",(180,210,180),((int(screen_size.split('x')[0])//2-dlc.mlength("继续游戏",0)//2),280),num=0,moving=3)
        dlc.moutput(screen,"导入地图",(180,130,210),((int(screen_size.split('x')[0])//2-dlc.mlength("开始游戏",0)//2),380),num=0,moving=3)
        dlc.moutput(screen,"编辑功能",(210,130,180),((int(screen_size.split('x')[0])//2-dlc.mlength("创建地图",0)//2),480),num=0,moving=3)
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    x=e.pos[0]
                    y=e.pos[1]
                    if x>10 and x<100:
                        if y>10 and y<100:
                            do="退出"
                            will_do="主界面"
                    if x>(int(screen_size.split('x')[0])//2-dlc.mlength("从零开始",0)//2) and x<(int(screen_size.split('x')[0])//2+dlc.mlength("从零开始",0)//2):
                        if y>280 and y<380:
                            do = "退出"
                            will_do = "地图设定"
                            setting_map=[[0,0]]
                            picx=0
                            picy=0
                        if y>380 and y<480:
                            do = "退出"
                            will_do = "地图设定"
                            with mopen("maps/newmap.json") as f:
                                setting_map = json.load(f)["map"]
                            print(setting_map)
                            picx=0
                            picy=0
                        if y>480 and y<580:
                            do = "退出"
                            will_do = "规则设定"
                            with mopen("maps/newmap.json") as f:
                                setting_all = json.load(f)
                                try:
                                    setting_rules=setting_all["rules"]
                                except:
                                    setting_rules={}
                                setting_map = setting_all["map"]
                            picx=0
                            picy=0
                            Rulessetting_Random_Coin = "#W随机道具"
                            Rulessetting_Shop = "#W商店"
                            Rulessetting_Coinadd = "#W金币补给"

    elif page=="重新游戏设定":
        dlc.moutput(screen,"新游戏设定",(180,180,188),((int(screen_size.split('x')[0])//2-dlc.mlength("新游戏设定",1)//2),70),num=1,moving=1)
        
        dlc.moutput(screen,"返回",(140,140,140),(10,10),num=3,moving=2)

        dlc.moutput(screen,f"游玩人数#x+=130<{len(players)}>",(210,210,147),(50,220),num=2,moving=2)
        dlc.moutput(screen,f"初始资金#x+=130<{cs_money}>",(170,210,227),(50,270),num=2,moving=2)
        dlc.moutput(screen,f"地图:#x+=175<{map_names[map_id]}>",(170,210,227),(50,320),num=2,moving=2)


        dlc.moutput(screen,"开始游戏",(240,150,177),((int(screen_size.split('x')[0])//2-dlc.mlength("开始游戏",2)//2),520),num=2,moving=3)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    x=e.pos[0]
                    y=e.pos[1]
                    if x>10 and x<100:
                        if y>10 and y<50:
                            do = "退出"
                            will_do = "主界面"
                    if x>50 and x<400:
                        if y>220 and y<270:
                            if players_names == "Normal":
                                players.append(f"玩家{len(players)+1}")
                            else:
                                try:
                                    players.append(players_names_choice[len(players)])
                                except:
                                    players.append(f"玩家{len(players)+1}")
                            if len(players) > 4:
                                players=players[:2]   
                        if y>270 and y<320:
                                try:
                                    cs_money = cs_money_choice[cs_money_choice.index(cs_money)+1]
                                except:
                                    cs_money = 2000
                        if y>320 and y<370:
                            map_id += 1
                            if map_id > len(map_names)-1:
                                map_id = 0

                    if x>50 and x<900:
                        if y>520 and y<570:
                            if len(players) > 1:
                                do = "退出"
                                will_do = "选择初始筹码"
                            else:
                                dlc.addts("玩家数少于2，无法进行对局",color=(255,70,0))

                            ##初始筹码组
                            coins_newplayer_chosen_coins=[]
                            for i in range(len(players)):
                                coins_newplayer_chosen_coins.append([])
                                for j in range(3):
                                    q=random.choice(coins_coins)
                                    while q=='顺风顺水':
                                        q=random.choice(coins_coins)####顺风顺水条件太难，开局抽取时被ban掉！！！！

                                    coins_newplayer_chosen_coins[i].append(q)

                            ###导入玩家数据
                            for i in players:

                                plr_data[i]={"name":i,"money":cs_money,"position":0,"dices":["普通色子","普通色子","普通色子"],"coins":[]}
                            ##从文件中导入地图和规则
                            with mopen(f"maps/{map_names[map_id]}.json") as f:
                                setting_all = json.load(f)
                                try:
                                    setting_rules=setting_all["rules"]
                                except:
                                    setting_rules={}
                                setting_map = setting_all["map"]
                            now_player=0
                            choose_coin=0
                            show_x=[40]
                            for i in players[1:]:
                                show_x.append(30-dlc.mlength(f"<玩家:{i}>",4))

    elif page=="地图设定":
        dlc.moutput(screen,"地图设定",(180,180,188),((int(screen_size.split('x')[0])//2-dlc.mlength("地图设定",1)//2),70),num=1,moving=1)
        dlc.moutput(screen,"保存并返回",(240,150,177),((int(screen_size.split('x')[0])//2-dlc.mlength("保存并返回",2)//2),520),num=2,moving=3)
        if do=="":#判定完全动画完成才渲染图像
            show_x=100
            show_y=200
            for j in range(6):
                for i in range(18):#x=i,y=j
                    if (i+picx,j+picy) in setting_map or [i+picx,j+picy] in setting_map:
                        ##绘制 50x50 方框
                        pygame.draw.rect(screen,(180,180,188),(show_x+50*i,show_y+50*j,50,50),2)
                        ##绘制 50x50 文字
                        dlc.moutput(screen,f"{setting_map.index([i+picx,j+picy])}",(225,125,25),(show_x+50*i+25-dlc.mlength(f"{setting_map.index([i+picx,j+picy])}",3)//2,show_y+50*j+11),num=3)
                   

        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    x=e.pos[0]
                    y=e.pos[1]
                    if y>500 and y<600:
                        with mopen("maps/newmap.json","w") as f:
                            json.dump({"map":setting_map},f)
                        do = "退出"
                        will_do = "主界面"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    setting_map.append([setting_map[-1][0]-1,setting_map[-1][1]])
                if e.key == pygame.K_RIGHT:
                    setting_map.append([setting_map[-1][0]+1,setting_map[-1][1]])
                if e.key == pygame.K_UP:
                    setting_map.append([setting_map[-1][0],setting_map[-1][1]-1])
                if e.key == pygame.K_DOWN:
                    setting_map.append([setting_map[-1][0],setting_map[-1][1]+1])
                if e.key == pygame.K_BACKSPACE:
                    setting_map=setting_map[:-1]
                ##WASD移动视角
                if e.key == pygame.K_w:
                    picy-=1
                if e.key == pygame.K_s:
                    picy+=1
                if e.key == pygame.K_a:
                    picx-=1
                if e.key == pygame.K_d:
                    picx+=1
                ##回车保存
                if e.key == pygame.K_RETURN:
                    with mopen("maps/newmap.json","w") as f:
                        json.dump({"map":setting_map},f)
    elif page=="规则设定":
        dlc.moutput(screen,"规则设定",(180,180,188),((int(screen_size.split('x')[0])//2-dlc.mlength("地图设定",1)//2),70),num=1,moving=1)
        dlc.moutput(screen,"保存并返回",(240,150,177),((int(screen_size.split('x')[0])//2-dlc.mlength("保存并返回",2)//2),520),num=2,moving=3)
        dlc.moutput(screen,"规则设定",(240,180,88),(800,170),num=2,moving=4)
        dlc.moutput(screen,f"{Rulessetting_Random_Coin}",(240,180,88),(800,210),num=2,moving=4)
        dlc.moutput(screen,f"{Rulessetting_Shop}",(240,180,88),(800,250),num=2,moving=4)
        dlc.moutput(screen,f"{Rulessetting_Coinadd}",(240,180,88),(800,290),num=2,moving=4)
        if do=="":#判定完全动画完成才渲染图像
            show_x=100
            show_y=200
            for j in range(6):
                for i in range(14):#x=i,y=j
                    if (i+picx,j+picy) in setting_map or [i+picx,j+picy] in setting_map:
                        ##绘制 50x50 方框
                        if i==0 and j==0:
                            pygame.draw.rect(screen,(255,205,125),(show_x,show_y,50,50),2)
                        
                            try:
                                rule = setting_rules[setting_map.index([i+picx,j+picy])]
                                if rule=="随机道具":
                                    Rulessetting_Random_Coin = "#R随机道具"
                                else:
                                    Rulessetting_Random_Coin = "#W随机道具"

                                if rule=="商店":
                                    Rulessetting_Shop = "#R商店"
                                else:
                                    Rulessetting_Shop = "#W商店"
                                if rule=="金币补给":
                                    Rulessetting_Coinadd = "#R金币补给"
                                else:
                                    Rulessetting_Coinadd = "#W金币补给"
                                
                            except:
                                Rulessetting_Random_Coin = "#W随机道具"
                                Rulessetting_Shop = "#W商店"
                                Rulessetting_Coinadd = "#W金币补给"
                            try:
                                setting_num=setting_map.index([i+picx,j+picy])
                            except:
                                setting_num="None"
                        else:
                            pygame.draw.rect(screen,(180,180,188),(show_x+50*i,show_y+50*j,50,50),2)
                            Rulessetting_Random_Coin = "#W随机道具"
                            Rulessetting_Shop = "#W商店"
                            Rulessetting_Coinadd = "#W金币补给"
                            setting_num="None"
                        ##绘制 50x50 文字
                        dlc.moutput(screen,f"{setting_map.index([i+picx,j+picy])}",(225,125,25),(show_x+50*i+25-dlc.mlength(f"{setting_map.index([i+picx,j+picy])}",3)//2,show_y+50*j+11),num=3)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    x=e.pos[0]
                    y=e.pos[1]
                    if y>500 and y<600:
                        with mopen("maps/newmap.json","w") as f:
                            json.dump({"map":setting_map,"rules":setting_rules},f)

                        do = "退出"
                        will_do = "主界面"
                    if x>=800:
                        if setting_num=="None":
                            dlc.addts("单元格无效，无法增加规则",color=(255,100,0))
                        elif y>=180 and y<=210:
                            ##删除单元格规则
                            try:
                                setting_rules.pop(setting_num)
                            except:
                                dlc.addts("无法删除单元格规则",color=(255,100,0))
                        elif y>=210 and y<=250:
                            setting_rules[setting_num]="随机道具"
                        elif y>=250 and y<=290:
                            setting_rules[setting_num]="商店"

                        elif y>=290 and y<=330:
                            setting_rules[setting_num]="金币补给"

            if e.type == pygame.KEYDOWN:
                ##WASD移动视角
                if e.key == pygame.K_w or e.key == pygame.K_UP:
                    picy-=1
                if e.key == pygame.K_s or e.key == pygame.K_DOWN:
                    picy+=1
                if e.key == pygame.K_a or e.key == pygame.K_LEFT:
                    picx-=1
                if e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                    picx+=1
                ##回车保存
                if e.key == pygame.K_RETURN:
                    with mopen("maps/newmap.json","w") as f:
                        json.dump({"map":setting_map,"rules":setting_rules},f)
    elif page=="选择初始筹码":
        dlc.moutput(screen,"选择初始筹码",(180,180,188),((int(screen_size.split('x')[0])//2-dlc.mlength("选择初始筹码",1)//2),70),num=1,moving=1)
        ###纵向输出3个筹码的名字，右方输出介绍

        if choose_coin==0:
            dlc.moutput(screen,"<当前选择>",(255,95,53),(960,217),num=3,moving=4)
        elif choose_coin==1:
            dlc.moutput(screen,"<当前选择>",(195,255,103),(960,277),num=3,moving=4)
        elif choose_coin==2:
            dlc.moutput(screen,"<当前选择>",(255,115,253),(960,337),num=3,moving=4)
        #print(show_x)
        if show_do!=[]:
            if show_do[1]=="-":
                if show_x[show_do[0]]>30-dlc.mlength(f"<玩家:{players[show_do[0]]}>",4):
                    show_x[show_do[0]]-=7
                if show_do[0]+1==len(players):
                        if show_x[0]<=40:
                            can_close=0
                            show_x[0]+=7
                        else:
                            can_close=1
                else:
                        if show_x[show_do[0]+1]<=40:
                            show_x[show_do[0]+1]+=7
                            can_close=0
                        else:
                            can_close=1

                if show_x[show_do[0]]<=30-dlc.mlength(f"<玩家:{players[show_do[0]]}>",4) and can_close==1:
                    show_do=[]
                    

        for i in range(len(players)):
            if i==now_player:
                dlc.moutput(screen,f"<玩家:{players[now_player]}>",players_colors[i],(show_x[i],20+40*i),num=4,moving=2)
            else:
                dlc.moutput(screen,f"<玩家:{players[i]}>",players_colors[i],(show_x[i],20+40*i),num=4,moving=2)
        


        dlc.moutput(screen,coins_newplayer_chosen_coins[now_player][0],(240,80,38),(80,210),num=4,moving=2)
        dlc.moutput(screen,coins_introductions[coins_newplayer_chosen_coins[now_player][0]],(240,80,38),(430,210),num=4,moving=4)
        dlc.moutput(screen,coins_newplayer_chosen_coins[now_player][1],(180,240,88),(80,270),num=4,moving=2)
        dlc.moutput(screen,coins_introductions[coins_newplayer_chosen_coins[now_player][1]],(180,240,88),(430,270),num=4,moving=4)
        dlc.moutput(screen,coins_newplayer_chosen_coins[now_player][2],(240,100,228),(80,330),num=4,moving=2)
        dlc.moutput(screen,coins_introductions[coins_newplayer_chosen_coins[now_player][2]],(240,100,228),(430,330),num=4,moving=4)
        

        dlc.moutput(screen,"确认",(240,150,177),((int(screen_size.split('x')[0])//2-dlc.mlength("确认",2)//2),520),num=2,moving=3)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    x=e.pos[0]
                    y=e.pos[1]
                    
                    if x>300 and x<=600:
                        if y>520 and y<570:
                            ##写入player
                            #print(plr_data)
                            plr_data[players[now_player]]["coins"].append(coins_newplayer_chosen_coins[now_player][choose_coin])
                            choose_coin=0
                            now_player+=1
                            if now_player==len( plr_data):
                                show_do=[now_player-1,"-"]
                                do="退出"
                                will_do="游戏"
                                now_player=0
                            else:
                                show_do=[now_player-1,"-"]
                    if y>210 and y<270:
                        choose_coin=0
                    if y>270 and y<330:
                        choose_coin=1
                    if y>330 and y<400:
                        choose_coin=2
    elif page=="游戏":
        if "显示当前回合的玩家":
            if show_do!=[]:
                if show_do[1]=="-":
                    if show_x[show_do[0]]>30-dlc.mlength(f"<玩家:{players[show_do[0]]}>",4):
                        show_x[show_do[0]]-=7
                    if show_do[0]+1==len(players):
                            if show_x[0]<=40:
                                can_close=0
                                show_x[0]+=7
                            else:
                                can_close=1
                    else:
                            if show_x[show_do[0]+1]<=40:
                                show_x[show_do[0]+1]+=7
                                can_close=0
                            else:
                                can_close=1

                    if show_x[show_do[0]]<=30-dlc.mlength(f"<玩家:{players[show_do[0]]}>",4) and can_close==1:
                        show_do=[]
            for i in range(len(players)):
                    dlc.moutput(screen,f"<玩家:{players[i]}>#x=280<{plr_data[players[i]]['position']}>",players_colors[i],(show_x[i],20+40*i),num=4,moving=2)
        if "渲染地图":
            if do=="":#判定完全动画完成才渲染图像

                pygame.draw.rect(screen,(250,220,180),(345,5,40*13+10,40*7+10),5)


                show__x=350
                show__y=10
                picx=setting_map[plr_data[players[now_player]]["position"]][0]-4
                picy=setting_map[plr_data[players[now_player]]["position"]][1]-2

                for j in range(7):
                    for i in range(13):#x=i,y=j
                        if (i+picx,j+picy) in setting_map or [i+picx,j+picy] in setting_map:
                            if "摆放棋子":
                                if [i+picx,j+picy]==setting_map[plr_data[players[0]]["position"]]:
                                    #绘制10x10红色方形
                                    pygame.draw.rect(screen,players_colors[0],(show__x+40*i+2,show__y+40*j+22,9,9))
                                if [i+picx,j+picy]==setting_map[plr_data[players[1]]["position"]]:
                                    #绘制10x10红色方形
                                    pygame.draw.rect(screen,players_colors[1],(show__x+40*i+11,show__y+40*j+22,9,9))
                                if len(players)>=3 and [i+picx,j+picy]==setting_map[plr_data[players[2]]["position"]]:
                                    #绘制10x10红色方形
                                    pygame.draw.rect(screen,players_colors[2],(show__x+40*i+2,show__y+40*j+31,9,9))
                                if len(players)>=4 and [i+picx,j+picy]==setting_map[plr_data[players[3]]["position"]]:
                                    #绘制10x10红色方形
                                    pygame.draw.rect(screen,players_colors[3],(show__x+40*i+11,show__y+40*j+31,9,9))
                            if "显示价钱":
                                if [i+picx,j+picy]==setting_map[0]:
                                    dlc.output(screen,"起  点",(255,255,255),(show__x+40*i+2,show__y+40*j+2),200,5)
                            pygame.draw.rect(screen,(30,30,78),(show__x+40*i,show__y+40*j+19,40,2),2)
                            pygame.draw.rect(screen,(30,30,78),(show__x+40*i+19,show__y+40*j+19,2,21),2)
                            pygame.draw.rect(screen,(180,180,188),(show__x+40*i,show__y+40*j,40,40),2)


        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    x=e.pos[0]
                    y=e.pos[1]
                    
                


                        
    

    





    
    dlc.mouselineoutput(screen)
    dlc.outputts(screen,2)

    pygame.display.flip()
    clock.tick(60)


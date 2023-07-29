import math
import os
import pygame, sys
import time
import requests

pygame.init()
pygame.display.set_caption("Spendee")
WIDTH = 1536
HEIGHT = 864

def get_font(size):
    return pygame.font.SysFont("8-bit Madness",size)

display = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
card_scale = (330*50/100,420*50/100)
card_distance = (10,60)
card_place = (WIDTH-card_scale[0]-10,(0))
hold_button_scale = (165,60)
buy_button_scale = (165,60)

tag = 'start'
running = True
viewing = False
picking = False
view_player = False
dupli = False
list_card = [[],[],[]]
pick_coin = []
this_coin = []
return_coin = []
back = 0
select = 0
pick = 0
remove = 0
color_coins = ["White","Blue","Green","Red","Black","Gold"]
list_coins = [pygame.image.load(os.path.join('Base',i+'Coin.png')) for i in color_coins]
color_card = ["White","Blue","Green","Red","Black"]
list_color_card = [pygame.image.load(os.path.join('Base',i+'Card.png')) for i in color_card ]

while running:
#important-----------------------------------------------
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
#important-----------------------------------------------
    mouse_pos = pygame.mouse.get_pos()
    display.fill('#b1651c')

    if tag == 'start':
        text = ['choose', 'number', 'of' ,'player']
        for i in range(len(text)):
            choose_no = get_font(200).render(text[i],True,"#ffff17")
            display.blit(choose_no,((WIDTH/2-choose_no.get_width())/2,(HEIGHT*3/2/5+choose_no.get_height())/2*i+50))
        for i in range(3):
            player_numtxt = get_font(300).render(str(i+2),True,"#ffff17")
            num_pos = ((WIDTH*6/4-player_numtxt.get_width())/2,(HEIGHT/2-player_numtxt.get_height())/2+HEIGHT*i/4)
            display.blit(player_numtxt,num_pos)
            num_rect = pygame.Rect(num_pos,(player_numtxt.get_width(),player_numtxt.get_height()))
            if pygame.mouse.get_pressed()[0] and not view_player and not back:
                if num_rect.collidepoint(mouse_pos):
                    tag = 'wait'
                    num = i+2

    elif tag == 'wait':
        display.fill('#000000')
        loading = get_font(150).render("Loading . . .",True,"#ffff17")        
        display.blit(loading,(WIDTH/2-loading.get_width()/2,HEIGHT/2-loading.get_height()/2))
        pygame.display.update()
        requests.post('http://127.0.0.1:8000/create_room/'+str(num))
        time.sleep(.5)
        tag = 'room'

    elif tag == 'room':
# load data pic game -----------------------------------------------
        data = requests.get('http://127.0.0.1:8000/room/').json()
        # load cards ---------------------------------------------------
        list_deck = [data["card_tier_1"],data["card_tier_2"],data["card_tier_3"]]
        list_tier = ["T1","T2","T3"]
        for j in range(len(list_deck)):
            for i in range(len(list_deck[j])):
                a = pygame.image.load(os.path.join(list_tier[j],list_deck[j][i]["name"])+'.jpg')
                b = pygame.transform.scale(a,card_scale)
                list_card[j].append(b)
        for i in range(num):
            data['player'].append('')
        tag = 'player'

# player join ---------------------------------------------------
    elif tag == 'player':
        while tag == 'player':
            mouse_pos = pygame.mouse.get_pos()
            display.fill('#b1651c')
            for i in range(data['num_player']):
                player_no = get_font(150).render("Player "+str(i+1),True,"#ffff17")
                player_name = get_font(150).render(data['player'][i],True,"#ffff17")
                input = pygame.Rect(550,50+150*i,900,player_name.get_height())        
                display.blit(player_no,(50,50+150*i))
                display.blit(player_name,(550,50+150*i))
                pygame.draw.rect(display,'red',input,3)
                if pygame.mouse.get_pressed()[0] :
                    if input.collidepoint(mouse_pos):
                        select = i
                        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        tag = "sfsf"

                keys = pygame.key.get_pressed()
                if keys[pygame.K_BACKSPACE]:
                    data['player'][select] = data['player'][select][:-1]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        for i in data['player']:
                            if sum(1 for d in data['player'] if d == i) > 1:
                                dupli = True
                            else : dupli = False
                        if not dupli:
                            for i in range(data['num_player']):
                                requests.post('http://127.0.0.1:8000/join/'+data['player'][i])
                            tag = 'play'
                    elif len(data['player'][select]) < 15 and not event.key == pygame.K_BACKSPACE:
                        data['player'][select] += event.unicode
                    
            back_button = pygame.draw.rect(display,'brown',(200,650,300,110))
            enter_button = pygame.draw.rect(display,'brown',(WIDTH-500,650,300,110))
            back_txt = get_font(120).render("EXIT",True,"#ffff17")
            enter_txt = get_font(120).render("ENTER",True,"#ffff17")
            display.blit(back_txt,(200+300/2-back_txt.get_width()/2,650+120/2-back_txt.get_height()/2))
            display.blit(enter_txt,(WIDTH-500+300/2-enter_txt.get_width()/2,650+120/2-enter_txt.get_height()/2))
            if pygame.mouse.get_pressed()[0] :
                if back_button.collidepoint(mouse_pos): 
                    tag = 'nm nm'
                    running = False
                if enter_button.collidepoint(mouse_pos): 
                    for i in data['player']:
                        if sum(1 for d in data['player'] if d == i) > 1:
                            dupli = True
                        else : dupli = False
                    if not dupli:
                        for i in range(data['num_player']):
                            requests.post('http://127.0.0.1:8000/join/'+data['player'][i])
                        tag = 'play'
            pygame.display.update()
            time.sleep(.01)
        players = requests.get('http://127.0.0.1:8000/player/').json()

# show game ---------------------------------------------------
    elif tag == 'play':
        players = requests.get('http://127.0.0.1:8000/player/').json()
        data = requests.get('http://127.0.0.1:8000/room/').json()
        old_data = data
        old_players = players
        #card -----------------------------------------------------------
        pygame.draw.circle(display,'red',(420,180+180*data["flag"]),20)

        for j in range(len(list_card)):
            for i in range(len(list_card[j])):
                card_pos = (card_place[0]-i*(card_scale[0]+card_distance[0]),HEIGHT-(card_place[1]+card_scale[1]*j+card_distance[1]*(j+1))-card_scale[1])
                display.blit(list_card[j][i],(card_pos)) 
                rect = pygame.Rect((card_pos),card_scale)
                pygame.draw.rect(display,'black',rect,5) 
                if pygame.mouse.get_pressed()[0] and not view_player and not back :
                    if rect.collidepoint(mouse_pos):
                        viewing = True
                        view_card = card_pos
                        if i == 4 : can_buy = False
                        else : can_buy = True
                        this_card = data['card_tier_'+str(j+1)][i]
                        num_card = i
            a = pygame.image.load(os.path.join('Base','Back'+str(j+1)+'.jpg'))
            b = pygame.transform.scale(a,card_scale)
            display.blit(b,(card_place[0]-4*(card_scale[0]+card_distance[0]),HEIGHT-(card_place[1]+card_scale[1]*j+card_distance[1]*(j+1))-card_scale[1]))

        if viewing :
            picking = 0
            pick_coin = []
            hold_button = pygame.Rect(view_card[0],view_card[1]-hold_button_scale[1],hold_button_scale[0],hold_button_scale[1])
            pygame.draw.rect(display,'red',hold_button)
            hold_txt = get_font(60).render("HOLD",True,"#ffff17")
            display.blit(hold_txt, (view_card[0]+(hold_button_scale[0]-hold_txt.get_width())/2,view_card[1]-hold_button_scale[1]+(hold_button_scale[1]-hold_txt.get_height())/2))
            if can_buy :
                buy_button = pygame.Rect(view_card[0],view_card[1]+card_scale[1],buy_button_scale[0],buy_button_scale[1])
                pygame.draw.rect(display,'red',buy_button)
                buy_txt = get_font(60).render('BUY',can_buy,"#ffff17")   
                display.blit(buy_txt, (view_card[0]+(buy_button_scale[0]-buy_txt.get_width())/2,view_card[1]+card_scale[1]+(buy_button_scale[1]-buy_txt.get_height())/2))
            if pygame.mouse.get_pressed()[0] and not view_player and not back:
                if hold_button.collidepoint(mouse_pos):
                    requests.post('http://127.0.0.1:8000/hold_card/'+this_card['name'])
                    if not requests.get('http://127.0.0.1:8000/return_coin/').json()['status']:
                        back = 0
                    else : back = 1
                    list_card = [[],[],[]]
                    players = requests.get('http://127.0.0.1:8000/player/').json()
                    data = requests.get('http://127.0.0.1:8000/room/').json()
                    list_deck = [data["card_tier_1"],data["card_tier_2"],data["card_tier_3"]]
                    list_tier = ["T1","T2","T3"]
                    for j in range(len(list_deck)):
                        for i in range(len(list_deck[j])):
                            a = pygame.image.load(os.path.join(list_tier[j],list_deck[j][i]["name"])+'.jpg')
                            b = pygame.transform.scale(a,card_scale)
                            list_card[j].append(b)
                    viewing = False
                    
                elif buy_button.collidepoint(mouse_pos):
                    response = requests.post('http://127.0.0.1:8000/buy_card/'+this_card['name']).json()
                    list_card = [[],[],[]]
                    players = requests.get('http://127.0.0.1:8000/player/').json()
                    data = requests.get('http://127.0.0.1:8000/room/').json()
                    list_deck = [data["card_tier_1"],data["card_tier_2"],data["card_tier_3"]]
                    list_tier = ["T1","T2","T3"]
                    for j in range(len(list_deck)):
                        for i in range(len(list_deck[j])):
                            a = pygame.image.load(os.path.join(list_tier[j],list_deck[j][i]["name"])+'.jpg')
                            b = pygame.transform.scale(a,card_scale)
                            list_card[j].append(b)
                    viewing = False
                    time.sleep(.1)
        
        # coin ----------------------------------------------------
        for i in range(len(list_coins)):
            coin_pos = (WIDTH-card_scale[0]*6,(HEIGHT-(list_coins[i].get_height()+10)*6-50)/2+(list_coins[i].get_height()+10)*i)
            rect = pygame.Rect(coin_pos,list_coins[i].get_size())
            display.blit(list_coins[i],coin_pos)
            if i < 5 :
                amount_coins_txt = get_font(70).render(str(len(data['coin'][i])-1),True,"#000000")
            else :
                amount_coins_txt = get_font(70).render(str(len(data['gold_coin'])),True,"#000000")
            display.blit(amount_coins_txt,(coin_pos[0]+(list_coins[i].get_width()-amount_coins_txt.get_width())/2,coin_pos[1]+(list_coins[i].get_height()-amount_coins_txt.get_height())/2))
            if pygame.mouse.get_pressed()[0] and not view_player and not back:
                if rect.collidepoint(mouse_pos) and i < 5:
                    picking = True
                    if len(pick_coin) < 3:
                        pick = 1
                        pick_coin.append(data['coin'][i][0]["color"])

        if picking :
            viewing = 0
            for i in range(len(pick_coin)):
                coin_pos = (WIDTH-card_scale[0]*6+20-120,(HEIGHT-(list_coins[i].get_height()+10)*6-50)/2+(list_coins[i].get_height()+10)*i)
                if remove == 1:
                    i-=1
                    remove = 0
                    time.sleep(.1)
                if pygame.mouse.get_pressed()[0] and not view_player and not back:
                    if pygame.Rect(coin_pos,(100,100)).collidepoint(mouse_pos):
                        pick_coin.remove(pick_coin[i])
                        remove = 1

            for i in range(len(pick_coin)):
                coin_pos = (WIDTH-card_scale[0]*6+20-120,(HEIGHT-(list_coins[i].get_height()+10)*6-50)/2+(list_coins[i].get_height()+10)*i)
                display.blit(list_coins[color_coins.index(pick_coin[i])],coin_pos)
                if pick == 1 : 
                    time.sleep(.1)
                    pick = 0

            confirm_button = pygame.draw.rect(display,'brown',(440,450,100,70))
            confirm_txt = get_font(80).render("OK",True,"#ffff17")
            display.blit(confirm_txt,(440+100/2-confirm_txt.get_width()/2,450+70/2-confirm_txt.get_height()/2))
            if pygame.mouse.get_pressed()[0] and not view_player and not back:
                if confirm_button.collidepoint(mouse_pos) :
                    requests.post('http://127.0.0.1:8000/pick_coin/'+' '.join(pick_coin))
                    pick_coin = []
                    if not requests.get('http://127.0.0.1:8000/return_coin/').json()['status'] :
                        back = 0
                    else :  back = 1
                    picking = False
                    players = requests.get('http://127.0.0.1:8000/player/').json()
                    data = requests.get('http://127.0.0.1:8000/room/').json()

            if len(pick_coin) == 0:
                picking = False
            
        # player --------------------------------------------------------
        for i in range(len(players)):
            player_name = get_font(50).render(players[i]['name'],True,"#ffff17")
            player_score = get_font(80).render(str(players[i]['score']),True,"#ffff17")
            display.blit(player_name,(50,80+i*180))
            display.blit(player_score,(380,70+i*180))
            rect = pygame.Rect(50,80+i*180,350,180)

            for j in range(5):
                if players[i]['coin'][j]:
                    coin_in_player = pygame.transform.scale(list_coins[j],(52,52))
                    display.blit(coin_in_player,(150+50*j-26,150+i*180-26))
                    player_amount_coin = get_font(40).render(str(len(players[i]['coin'][j])),True,"#000000")
                    display.blit(player_amount_coin,(150+50*j-player_amount_coin.get_width()/2,150+i*180-player_amount_coin.get_height()/2))

                if players[i]['card'] and color_card[j] in [d['value'] for d in players[i]['card']]:
                    card_in_player = pygame.transform.scale(list_color_card[j],(33*1.57,42*1.57))
                    display.blit(card_in_player,(150+50*j-26,150+i*180+30))
                    pygame.draw.rect(display,'black',(150+50*j-26,150+i*180+30,math.ceil(33*1.57),math.ceil(42*1.57)),2)
                    if j < 4 : player_amount_card = get_font(40).render(str(sum(1 for d in players[i]['card'] if d.get("value")== color_card[j])),True,"#000000")
                    else : player_amount_card = get_font(40).render(str(sum(1 for d in players[i]['card'] if d.get("value")== color_card[j])),True,"#ffffff")
                    display.blit(player_amount_card,(150+50*j-player_amount_card.get_width()/2,150+30+i*180+33-player_amount_card.get_height()/2))

            if players[i]['gold_coin']:
                coin_in_player = pygame.transform.scale(list_coins[5],(50,50))
                display.blit(coin_in_player,(150+50*(-1)-25,150+i*180-25))
                player_amount_gold_coin = get_font(40).render(str(len(players[i]['gold_coin'])),True,"#000000")
                display.blit(player_amount_gold_coin,(150+50*(-1)-player_amount_gold_coin.get_width()/2,150+i*180-player_amount_gold_coin.get_height()/2))

            if players[i]['hold_card']:
                pygame.draw.rect(display,'brown',(150+50*(-1)-26,150+i*180+30,math.ceil(33*1.57),math.ceil(42*1.57)))
                pygame.draw.rect(display,'black',(150+50*(-1)-26,150+i*180+30,math.ceil(33*1.57),math.ceil(42*1.57)),2)
                player_amount_card = get_font(40).render(str(len(players[i]['hold_card'])),True,"#000000")
                display.blit(player_amount_card,(150+50*(-1)-player_amount_card.get_width()/2,150+30+i*180+33-player_amount_card.get_height()/2))

            if pygame.mouse.get_pressed()[0] and not view_player and not back:
                if rect.collidepoint(mouse_pos):
                    view_player = True
                    this_player = players[i]
                    
        if back:
            pygame.draw.rect(display,'gray',(240,20,300,800))
            for j in range(5):
                if players[data["flag"]]['coin'][j]:
                    coin_in_player = pygame.transform.scale(list_coins[j],(100,100))
                    display.blit(coin_in_player,(250,(HEIGHT-(list_coins[j].get_height()+10)*6-50)/2+(list_coins[j].get_height()+10)*j))
                    player_amount_coin = get_font(70).render(str(len(players[data["flag"]]['coin'][j])),True,"#000000")
                    display.blit(player_amount_coin,(250+36,(HEIGHT+55-(list_coins[j].get_height()+10)*6-50)/2+(list_coins[j].get_height()+10)*j))
                    rect = pygame.Rect((250,(HEIGHT-(list_coins[j].get_height()+10)*6-50)/2+(list_coins[j].get_height()+10)*j,100,100))
                    picking = 0
                    viewing = 0
                    if pygame.mouse.get_pressed()[0] and not view_player :
                        if rect.collidepoint(mouse_pos) :
                            if len(return_coin) < 3:
                                return_coin.append(players[data["flag"]]['coin'][j][0]['color'])
                            time.sleep(.1)

            for i in range(len(return_coin)):
                if remove == 1:
                    i-=1
                    remove = 0
                    time.sleep(.1)
                coin_pos = (WIDTH-card_scale[0]*6+20-150,(HEIGHT-(list_coins[i].get_height()+10)*6-50)/2+(list_coins[i].get_height()+10)*i)
                display.blit(list_coins[color_coins.index(return_coin[i])],coin_pos)
                if pygame.mouse.get_pressed()[0] and not view_player :
                    if pygame.Rect(coin_pos,(100,100)).collidepoint(mouse_pos) :
                        return_coin.remove(return_coin[i])
                        remove = 1

            if 10+len(return_coin) == (sum(len(i) for i in players[data['flag']]['coin'])+len(players[data['flag']]['gold_coin'])):
                confirm_button = pygame.draw.rect(display,'brown',(400,450,100,70))
                confirm_txt = get_font(80).render("OK",True,"#ffff17")
                display.blit(confirm_txt,(400+100/2-confirm_txt.get_width()/2,450+70/2-confirm_txt.get_height()/2))
                if pygame.mouse.get_pressed()[0] and not view_player :
                    if confirm_button.collidepoint(mouse_pos):
                        requests.post('http://127.0.0.1:8000/return_coin/'+' '.join(return_coin))
                        players = requests.get('http://127.0.0.1:8000/player/').json()
                        return_coin = []
                        data = requests.get('http://127.0.0.1:8000/room/').json()
                        back = 0

        if view_player :
            pygame.draw.rect(display,'#acc9eb',(50,50,800,HEIGHT-100))
            for i in range(len(this_player['hold_card'])):
                a = pygame.image.load(os.path.join('T'+str(this_player['hold_card'][i]['tier']),this_player['hold_card'][i]["name"])+'.jpg')
                b = pygame.transform.scale(a,(33*4,42*4))
                display.blit(b,(150+i*233,550))

                if this_player["name"] == players[data['flag']]['name']:
                    buy_button = pygame.Rect(150+i*233,560+42*4,33*4,buy_button_scale[1])
                    pygame.draw.rect(display,'red',buy_button)
                    buy_txt = get_font(60).render('BUY',True,"#ffff17")   
                    display.blit(buy_txt, (150+i*233+(33*4-buy_txt.get_width())/2,560+42*4+(buy_button_scale[1]-buy_txt.get_height())/2))
                else :
                    a = pygame.image.load(os.path.join('Base','Back'+str(this_player['hold_card'][i]['tier'])+'.jpg'))
                    b = pygame.transform.scale(a,(33*4,42*4))
                    display.blit(b,(150+i*233,550,33*4,42*4))

                if pygame.mouse.get_pressed()[0]:
                    if buy_button.collidepoint(mouse_pos):
                        requests.post('http://127.0.0.1:8000/get_hold_card/'+this_player['hold_card'][i]['name'])
                        players = requests.get('http://127.0.0.1:8000/player/').json()
                        data = requests.get('http://127.0.0.1:8000/room/').json()
                        view_player = False

            for j in range(5):
                show_card = [this_player['card'].index(d) for d in this_player['card'] if d['value'] == color_card[j]]
                for i in range(len(show_card)):
                    a = pygame.image.load(os.path.join('T'+str(this_player['card'][show_card[i]]['tier']),this_player['card'][show_card[i]]["name"])+'.jpg')
                    b = pygame.transform.scale(a,(33*3,42*3))
                    display.blit(b,(180+j*(33*3+10),150+i*42))

            if pygame.mouse.get_pressed()[0] :
                if not pygame.Rect(50,50,800,HEIGHT-100).collidepoint(mouse_pos):
                    view_player = False

        for i in players:
            if i['score'] >= 15:
                requests.get('http://127.0.0.1:8000/last_turn/')
                podium = requests.get('http://127.0.0.1:8000/win/').json()
                tag = 'end game'

        if old_data != data or old_players != players :
            if (sum(len(i) for i in players[data['flag']]['coin'])+len(players[data['flag']]['gold_coin'])) <= 10:
                requests.get('http://127.0.0.1:8000/update_flag/')
                old_data = data
                old_players = players

    if tag == 'end game':
        display.fill('#b1651c')
        winner_is = get_font(300).render("WINNER IS",True,"#ffff17")
        display.blit(winner_is,((WIDTH-winner_is.get_width())/2,(HEIGHT-winner_is.get_height())/2-300))
        winner = get_font(250).render(podium["winner_name"],True,"#ffff17")
        display.blit(winner,((WIDTH-winner.get_width())/2,(HEIGHT-winner.get_height())/2))
        
    pygame.display.update()
    
pygame.quit()
sys.exit()
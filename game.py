from class_game import *
from class_user import *
from fastapi import FastAPI

system = System()
app = FastAPI()

@app.post("/create_room/{num_player}")
async def get_room(num_player:int):
    if num_player < 2 or num_player > 4:
        return "Can't create room"
    stack_coin = StackCoin()
    gold_coin = GoldCoin()
    full_deck = FullDeck([], 90)
    
    #สร้างเหรียญ
    stack_coin.generate_coin(num_player)
    #สร้างการ์ด
    file_name = 'data'
    full_deck.generate_card(file_name)
    #แยกกอง t1 t2 t3
    deck_t1 = Deck([], 1, 40)
    deck_t2 = Deck([], 2, 30)
    deck_t3 = Deck([], 3, 20)
    full_deck.split_tier(deck_t1, deck_t2, deck_t3)

    #สุ่ม top deck 5  .[]
    deck_t1.shuffle_deck()
    deck_t2.shuffle_deck()
    deck_t3.shuffle_deck()
    #เข้า บอร์ด
    room = BoardRoom(deck_t1, deck_t2, deck_t3, stack_coin, gold_coin)
    #คนเล่นกี่คน
    room.add_num_player(num_player)

    system.add_room(room)

    return True

@app.get("/room/")
async def print_room():

    data = { "num_player" : system.get_room()[0].get_num_player(),
            "target" : system.get_room()[0].get_target(),
            "card_tier_1" : system.get_room()[0].show_card_t1(),
            "card_tier_2" : system.get_room()[0].show_card_t2(),
            "card_tier_3" : system.get_room()[0].show_card_t3(),
            "player" : [],
            "coin" : system.get_room()[0].show_coin(),
            "gold_coin" : system.get_room()[0].get_gold_coin().get_coins() ,
            "flag" : system.get_room()[0].get_flag()
            }
    return data

@app.post("/join/{name}")
async def get_name(name : str):
    if len(system.get_room()) == 1:
        for player in system.get_room()[0].get_player():
            if name == player.get_name():
                return {"False" : "already have this name"} 
        if system.get_room()[0].add_player(Player(name)):
            system.set_play(True)
            return {"False" : "playing"}
        else :
            return True
    else :
        return False #ยังไม่ได้สร้างห้อง 

@app.get("/player/")
async def print_player():
    data = []
    for i in range(len(system.get_room()[0].get_player())):
        data.append({"id" : i+1,
            "name" : system.get_room()[0].get_player()[i].get_name(),
            "score" : system.get_room()[0].get_player()[i].get_score(),
            "card" : system.get_room()[0].get_player()[i].return_card(),
            "hold_card" : system.get_room()[0].get_player()[i].return_hold_card(),
            "coin" : system.get_room()[0].get_player()[i].return_coin(),
            "gold_coin" : system.get_room()[0].get_player()[i].return_gold_coin()})
    return data

#pick coin
@app.get("/coin/")
async def print_coin():
    if system.get_play() == False:
        return {"False" : "can't play. Waiting for others"}
    else :
        return {"coin" : system.get_room()[0].show_coin(),
            "gold_coin" : system.get_room()[0].get_gold_coin().get_coins() }

@app.post("/pick_coin/{color}")
async def player_pick_coin(color : str):
    if system.get_play() == False:
        return {"False" : "can't play. Waiting for others"}
    else :
        list_coin = color.split(' ')
        temp = system.get_room()[0].get_coin().pick_coin(list_coin)
        if temp != False:
            system.get_room()[0].get_player()[system.get_room()[0].get_flag()].update_coin(temp)
            return True
        else :
            return temp
    
#return coin
@app.get("/return_coin/")
async def print_player_coin():
    return {"player_coin" : system.get_room()[0].get_player()[system.get_room()[0].get_flag()].return_coin(),
            "player_gold_coin" : system.get_room()[0].get_player()[system.get_room()[0].get_flag()].return_gold_coin(),
            "status" : system.get_room()[0].get_player()[system.get_room()[0].get_flag()].too_much_coin()}

@app.post("/return_coin/{color}")
async def player_return_coin(color : str):
    if system.get_play() == False:
        return {"False" : "can't play. Waiting for others"}
    else :
        if system.get_room()[0].get_player()[system.get_room()[0].get_flag()].too_much_coin():
            system.get_room()[0].return_coins(color, system.get_room()[0].get_player()[system.get_room()[0].get_flag()])
            return True 
        else:
            return False
        

@app.get("/card/")
async def print_card():
    if system.get_play() == False:
        return {"False" : "can't play. Waiting for others"}
    else :
        return {"card_t1" : system.get_room()[0].show_card_t1(),
            "card_t2" : system.get_room()[0].show_card_t2(),
            "card_t3" : system.get_room()[0].show_card_t3()}  

#buy card
@app.post("/buy_card/{name_card}")
async def player_buy_card(name_card : str):
    if system.get_play() == False:
        return {"False" : "can't play. Waiting for others"}
    else :
        can_buy = system.get_room()[0].buy_card(system.get_room()[0].get_player()[system.get_room()[0].get_flag()],name_card)
        if can_buy != False:
            if can_buy == 1:
                system.get_room()[0].get_deck_1().random_top_deck()
            elif can_buy == 2:
                system.get_room()[0].get_deck_2().random_top_deck()
            elif can_buy == 3:
                system.get_room()[0].get_deck_3().random_top_deck()
            return True
        else :
            return False

#hold card
@app.post("/hold_card/{name_card}")
async def player_hold_card(name_card : str):
    if system.get_play() == False:
        return {"False" : "can't play. Waiting for others"}
    else :
        if system.get_room()[0].get_player()[system.get_room()[0].get_flag()].can_hold():
            can_hold = system.get_room()[0].hold_card(system.get_room()[0].get_player()[system.get_room()[0].get_flag()],name_card)
            if can_hold == 1:
                system.get_room()[0].get_deck_1().random_top_deck()
            elif can_hold == 2:
                system.get_room()[0].get_deck_2().random_top_deck()
            elif can_hold == 3:
                system.get_room()[0].get_deck_3().random_top_deck()
            return "Can hold this card"
        else :
            return "Can't hold this card"

#buy hold card
@app.get("/get_hold_card/")
async def print_hold_card():
    return system.get_room()[0].get_player()[system.get_room()[0].get_flag()].return_hold_card()

@app.post("/get_hold_card/{card_name}")
async def buy_hold_card(card_name:str):
    if system.get_play() == False:
        return {"False" : "can't play. Waiting for others"}
    else :
        system.get_room()[0].buy_hold_card(system.get_room()[0].get_player()[system.get_room()[0].get_flag()],card_name)

#update flag
@app.get("/update_flag/")
async def get_update_flag():
    system.get_room()[0].update_flag()
    return system.get_room()[0].get_flag()

#check score ถึง 15 ให้เป็น last turn
@app.get("/last_turn/")
async def last_turn():
    if system.get_play() == False:
        return {"False" : "can't play. Waiting for others"}
    else :
        system.set_play(False)
        
#get win
@app.get("/win/")
async def winner():
    if system.get_play() == False:
        return {"winner_name" : system.get_room()[0].win()}
    else :
        return "playing"
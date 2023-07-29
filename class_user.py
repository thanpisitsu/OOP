from class_game import *

class System :
    def __init__(self) :
        self._room = []
        self._play = False
#getter-----------------------------------

    def get_room(self):
        return self._room
    
    def get_play(self):
        return self._play
    
#setter-----------------------------------
    def set_play(self,status):
        self._play = status

    def add_room(self, room):
        self._room.append(room)
        if len(self._room) > 1:
            self._room.pop(0)

color_coin = [ "White", "Blue", "Green", "Red", "Black"]
class Player() :
    def __init__(self, name) :
        self._name = name
        self._score = 0
        self._card = []
        self._hold_card = []
        self._coins = [[],[],[],[],[]]
        self._gold_coins = []

#getter--------------------------------
    def get_name(self):
        return self._name
            
    def get_score(self):
        return self._score
    
    def get_card(self):
        return self._card
    
    def get_hold_card(self):
        return self._hold_card
    
    def get_coins(self):
        return self._coins
    
    def get_gold_coins(self):
        return self._gold_coins
    
#setter-----------------------------------
    def set_hold_card(self,list_card):
        self._hold_card = list_card
    
    def return_card(self):
        deck = []
        for card in self._card:
            deck.append({"name" : card.get_name(),"cost" : card.get_cost(),"point" : card.get_point(),"tier" : card.get_tier(),"value" : card.get_value()})
        return deck
    
    def return_hold_card(self):
        deck = []
        for card in self._hold_card:
            deck.append({"name" : card.get_name(),"cost" : card.get_cost(),"point" : card.get_point(),"tier" : card.get_tier(),"value" : card.get_value()})
        return deck
    
    def return_coin(self):
        t_coin = []
        for list_coin in self._coins:
            temp = []
            for coin in list_coin:
                temp.append({"color" : coin.get_color(), "value" : 1})
            t_coin.append(temp)
        return t_coin
    
    def return_gold_coin(self):
        return self._gold_coins
    
    def can_hold(self) :
        if len(self._hold_card) == 3:
            return False
        return True
    
    def add_hold_card(self, card):
        self._hold_card.append(card)

    def print_hold_card(self):
        for card in self._hold_card:
            card.print_card()

    def update_card(self, card):
        self._card.append(card)

    def update_coin(self, choose):
        if choose != False:
            for coin in choose:
                if coin.get_color() == 'White':
                    self._coins[0].append(coin)
                elif coin.get_color() == 'Blue':
                    self._coins[1].append(coin)
                elif coin.get_color() == 'Green':
                    self._coins[2].append(coin)
                elif coin.get_color() == 'Red':
                    self._coins[3].append(coin)
                elif coin.get_color() == 'Black':
                    self._coins[4].append(coin)

    def update_gold_coin(self, coin):
        self._gold_coins.append(coin)
    
    def pay_gold_coin(self):
        coin = self._gold_coins[0]
        self._gold_coins.remove(coin)
        return coin

    def pay_coin(self, color, num): # จำนวนเหรียญที่ต้องคืนในสีนั้น
        temp = []
        for list_coin in self._coins:
            if len(list_coin) > 0:
                if list_coin[0].get_color() == color:
                    for i in range(num):
                        coin = list_coin[0]
                        temp.append(coin)
                        list_coin.pop()
                        print(f'{color} check!!!')
                    return temp

    def too_much_coin(self):
        num_of_coin = 0
        for list_coin in self._coins:
            num_of_coin += len(list_coin)
        num_of_coin += len(self._gold_coins)

        if num_of_coin > 10 :
            print("get only 10 coins")
            return True
        else:
            return False

    def print_coin(self):
        for list_coin in self._coins:
            a = []
            for coin in list_coin:
                a.append(coin.get_color())
            print(a)

    def discount_coin(self):
        dis_coin = []
        for i in range(5):
            temp = 0
            for card in self._card:
                if color_coin[i] == card.get_value():
                    temp += 1
            dis_coin.append(temp)
        return dis_coin
    
    def update_score(self, point):
        self._score += point
import random
import json
class FullDeck :
    def __init__(self, card, number) :
        self._card_collection = card #Aggragation with Card
        self.__num_card = number

    def generate_card(self, file_name):
        f = open(f'{file_name}.json')
        data = json.load(f)
        for card in data['all_card_details']:
            self._card_collection.append(Card(card["name"], card["cost"], card["point"], card["tier"], card["value"])) 
        f.close()
    
    def split_tier(self, deck_1, deck_2, deck_3):
         for card in self._card_collection:
            if card.get_tier() == 1 :
                temp = deck_1.get_card_collection()
                temp.append(card)
                deck_1.set_card_collection(temp)
            elif card.get_tier() == 2 :
                temp = deck_2.get_card_collection()
                temp.append(card)
                deck_2.set_card_collection(temp)
            elif card.get_tier() == 3 :
                temp = deck_3.get_card_collection()
                temp.append(card)
                deck_3.set_card_collection(temp)

class Card :
    def __init__(self, name, cost, point, tier, value) :
        self._name = name #"W311"
        self._cost = cost #[3,1,0,0,1]
        self._point = point #0
        self._tier = tier #"in_deck"
        self._value = value
#get-------------------------------------------
    def get_name(self):
        return self._name

    def get_cost(self):
        return self._cost

    def get_point(self):
        return self._point

    def get_tier(self):
        return self._tier

    def get_value(self):
        return self._value

    
class Deck (FullDeck):
    def __init__(self,card, tier, number) :
        FullDeck.__init__(self, card, number)
        self.__tier = tier
        self._top_deck = []
# getter -----------------------------------------------
    def get_card_collection(self):
        return self._card_collection
    def get_top_deck(self):
        return self._top_deck
# setter -----------------------------------------------
    def set_card_collection(self,list_card):
        self._card_collection = list_card

    def print_top_deck(self):
        for card in self._top_deck:
            card.print_card()

    def shuffle_deck(self):
        temp = []
        for i in range(5):
            random.shuffle(self._card_collection)
            temp.append(self._card_collection[0])
            self._card_collection.remove(self._card_collection[0])
        self._top_deck = temp

    def random_top_deck(self):
        random.shuffle(self._card_collection)
        temp = self._card_collection[0]
        self._top_deck.append(temp)
        self._card_collection.remove(self._card_collection[0])


color_coin = [ "White", "Blue", "Green", "Red", "Black"]
class StackCoin :
    def __init__(self) :
        self._coins = [] # [7,7,7,7] #Aggregation with Coin
#getter--------------------------------
    def get_coins(self):
        return self._coins
    
    def less_than_3_color(self):
        z_coin = 0
        for temp in self._coins:
            if len(temp) > 1:
                z_coin += 1
        return z_coin

    def pick_coin(self, choose_coin) :
        coin = []
        if self.less_than_3_color() == 2: # เหลือสีน้อยกว่า 3
            if len(choose_coin) == 2:
                if choose_coin[0] == choose_coin[1]:
                    for list_coin in self._coins:
                        if len(list_coin) - 1 < 4 and list_coin[0].get_color() == choose_coin[0]:
                            print("Can't pick coin.")
                            return False
            else :
                print(" 2 color, 1 coin. Nope")
                return False
        elif self.less_than_3_color() == 1:
            if len(choose_coin) != 1:
                print("pick again")
                return False
        elif self.less_than_3_color() >= 3:       
            if len(choose_coin) == 2:
                if choose_coin[0] != choose_coin[1]:
                    print("Can't pick coin, please pick 1 pair or 3 differrent")
                    return False
                elif choose_coin[0] == choose_coin[1]:
                    for list_coin in self._coins:
                        if len(list_coin) - 1 < 4 and list_coin[0].get_color() == choose_coin[0]:
                            print("Can't pick coin.")
                            return False
            elif len(choose_coin) == 3:
                if choose_coin[0] == choose_coin[1] or choose_coin[1] == choose_coin[2] or choose_coin[0] == choose_coin[2]:
                    print("Can't pick like this. Please choose 3 different or 1 pair.")
                    return False
            
                for i in range(len(choose_coin)):
                    for temp in self._coins:
                        if temp[0].get_color() == choose_coin[i]:
                            print('yeeeeee')
                            if len(temp) == 1 :
                                print("0 coin, can't pick.")
                                return False
            else:
                print("Can't pick like this. Please choose 3 different or 1 pair.")
                return False
        
        for i in range(len(choose_coin)):
            for list_coin in self._coins:
                if choose_coin[i] == list_coin[0].get_color() :
                    if len(list_coin) - 1 > 0:
                        coin.append(list_coin[0])
                        list_coin.remove(list_coin[0])
        #print check                  
        return coin
    
    def update_coins(self, coin): #list ที่เก็บ class coin
        #temp is coin color
        for temp in coin:
            for list_coin in self._coins:
                if temp.get_color() == list_coin[0].get_color():
                    list_coin.append(temp)
    
    def generate_coin(self, num):
        for i in range(len(color_coin)):
            if num == 2:
                num_coin = 5
            elif num == 3:
                num_coin = 6
            else :
                num_coin = 8
            temp = []
            for j in range(num_coin):
                temp.append(Coin(color_coin[i]))
            self._coins.append(temp)
        
class Coin :
    def __init__(self, color) :
        self._color = color #"white"
        self.__value = 1
# getter ---------------------------------------------
    def get_color(self):
        return self._color

class GoldCoin :
    def __init__(self) :
        self._coins = ["Gold", "Gold", "Gold", "Gold", "Gold"]
#getter--------------------------------
    def get_coins(self):
        return self._coins
    
    def pay_gold_coin(self):
        coin = self._coins[0]
        self._coins.remove(coin)
        return coin
    
    def update_gold_coin(self, coin):
        self._coins.append(coin)

    def print_gold_coin(self):
        print(self._coins)



class BoardRoom :
    def __init__(self, deck_tier_1, deck_tier_2, deck_tier_3, coin, gold_coin) :
        self._num_player = 0 #2+1+1
        self._target = 15 #15
        self._deck_1 = deck_tier_1 # Class deck
        self._deck_2 = deck_tier_2 # Class deck
        self._deck_3 = deck_tier_3 # Class deck
        self._player = [] #[]
        self._coin = coin #[]
        self._gold_coin = gold_coin #[]
        self._flag = 0
#getter--------------------------------------------
    def get_num_player(self):
        return self._num_player

    def get_target(self):
        return self._target

    def get_deck_1(self):
        return self._deck_1

    def get_deck_2(self):
        return self._deck_2

    def get_deck_3(self):
        return self._deck_3

    def get_player(self):
        return self._player

    def get_coin(self):
        return self._coin

    def get_gold_coin(self):
        return self._gold_coin

    def get_flag(self):
        return self._flag


    def show_card(self):
        for card in self._deck_1:
            card.print_card()

    def show_card_t1(self):
        d_tier_1 = []
        for card in self._deck_1.get_top_deck():
            d_tier_1.append({"name" : card.get_name(),"cost" : card.get_cost(),"point" : card.get_point(),"tier" : card.get_tier(),"value" : card.get_value()})
        return d_tier_1
    
    def show_card_t2(self):
        d_tier_2 = []
        for card in self._deck_2.get_top_deck():
            d_tier_2.append({"name" : card.get_name(),"cost" : card.get_cost(),"point" : card.get_point(),"tier" : card.get_tier(),"value" : card.get_value()})
        return d_tier_2
        
    def show_card_t3(self):
        d_tier_3 = []
        for card in self._deck_3.get_top_deck():
            d_tier_3.append({"name" : card.get_name(),"cost" : card.get_cost(),"point" : card.get_point(),"tier" : card.get_tier(),"value" : card.get_value()})
        return d_tier_3
    
    def show_coin(self):
        t_coin = []
        for list_coin in self._coin.get_coins():
            temp = []
            for coin in list_coin:
                temp.append({"color" : coin.get_color(), "value" : 1})
            t_coin.append(temp)
        return t_coin
    
    def add_player(self, player):
        if len(self._player) < self._num_player:
            self._player.append(player)
        if len(self._player) == self._num_player:
            return True
        else :
            return False

    def add_num_player(self, num):
        self._num_player = num
    
    def check_player_in_room(self):
        if self._num_player == len(self._player):
            return True
        else :
            return False

    def update_flag(self):
        self._flag += 1
        self._flag = self._flag % self._num_player
    
    def buy_card(self,player,card_name):
        search=False
        for card in self._deck_1.get_top_deck():
            if card_name == card.get_name():
                current_card=card
                current_deck=self._deck_1.get_top_deck()
                search=True
                break
        for card in self._deck_2.get_top_deck():
            if card_name == card.get_name():
                current_card=card
                current_deck=self._deck_2.get_top_deck()
                search=True
                break
        for card in self._deck_3.get_top_deck():
            if card_name == card.get_name():
                current_card=card
                current_deck=self._deck_3.get_top_deck()
                search=True
                break
        if search == False :
            print("Wrong name")
            return False
        
        can_buy = True
        discount = player.discount_coin()
        player_coin = 0
        card_coin = 0
        cost = []
        for i in range(5):
            temp = current_card.get_cost()[i] - discount[i]
            if temp < 0:
                temp = 0
            cost.append(temp)
                
        for i in range(5):     
            if len(player.get_coins()[i]) < cost[i]:
                player_coin += len(player.get_coins()[i])
                card_coin += cost[i]
                can_buy = False

        if not can_buy:
            if player_coin + len(player.get_gold_coins()) >= card_coin:
                can_buy = True

        if can_buy:
            #remove coin from player
            for i in range(5):
                if cost[i] > 0:
                    if cost[i] > len(player.get_coins()[i]):
                        diff = cost[i] - len(player.get_coins()[i])
                        #remove coin
                        if len(player.get_coins()[i]) > 0 :
                            self._coin.update_coins(player.pay_coin(color_coin[i], len(player.get_coins()[i])))
                        #remove gold coin
                        for i in range(diff):
                            self._gold_coin.update_gold_coin(player.pay_gold_coin())
                    else :
                        print(color_coin[i])
                        check = player.pay_coin(color_coin[i], cost[i])
                        self._coin.update_coins(check)

            #update score
            player.update_score(current_card.get_point())
            #update card
            player.update_card(current_card)
            #remove card from deck
            current_deck.remove(current_card)
            print(current_card.get_tier())
            return current_card.get_tier()
        else:
            print("Not enough coin, can't buy.")
            return False

    def buy_hold_card(self, player, card_name):
        search = False
        for card in player.get_hold_card():
            if card.get_name() == card_name:
                current_card = card
                search = True
        if not search:
            print("Don't have this card on your hand")
            return False
        can_buy = True
        discount = player.discount_coin()
        player_coin = 0
        card_coin = 0
        cost = []
        for i in range(5):
            temp = current_card.get_cost()[i] - discount[i]
            if temp < 0:
                temp = 0
            cost.append(temp)
                
        for i in range(5):     
            if len(player.get_coins()[i]) < cost[i]:
                player_coin += len(player.get_coins()[i])
                card_coin += cost[i]
                can_buy = False

        if not can_buy:
            if player_coin + len(player.get_gold_coins()) >= card_coin:
                can_buy = True

        if can_buy:
            #remove coin from player
            for i in range(5):
                if cost[i] > 0:
                    if cost[i] > len(player.get_coins()[i]):
                        diff = cost[i] - len(player.get_coins()[i])
                        #remove coin
                        if len(player.get_coins()[i]) > 0 :
                            self._coin.update_coins(player.pay_coin(color_coin[i], len(player.get_coins()[i])))
                        #remove gold coin
                        for i in range(diff):
                            self._gold_coin.update_gold_coin(player.pay_gold_coin())
                    else :
                        print(color_coin[i])
                        check = player.pay_coin(color_coin[i], cost[i])
                        self._coin.update_coins(check)

            #update score
            player.update_score(current_card.get_point())
            #update card
            player.update_card(current_card)
            #remove card from deck
            hold = player.get_hold_card()
            hold.remove(current_card)
            player.set_hold_card(hold)
            return True
        else:
            print("Not enough coin, can't buy.")
            return False
        

    def hold_card(self, player, card_name):
        search=False
        for card in self._deck_1.get_top_deck():
            if card_name == card.get_name():
                current_card=card
                current_deck=self._deck_1.get_top_deck()
                search=True
                break
        for card in self._deck_2.get_top_deck():
            if card_name == card.get_name():
                current_card=card
                current_deck=self._deck_2.get_top_deck()
                search=True
                break
        for card in self._deck_3.get_top_deck():
            if card_name == card.get_name():
                current_card=card
                current_deck=self._deck_3.get_top_deck()
                search=True
                break
        if search == False :
            print("Wrong name")
            return False
        #card เข้า player
        player.add_hold_card(current_card)
        current_deck.remove(current_card)
        #gold coin เข้า player
        if self._gold_coin.get_coins() != []:
            player.update_gold_coin(self._gold_coin.pay_gold_coin())
        print(current_card.get_tier())
        return current_card.get_tier()

    def return_coins(self, color, player):
        list_coin = color.split(' ')
        for coin in list_coin :
                for i in range(5):
                    if color_coin[i] == coin:
                        self._coin.update_coins(player.pay_coin(coin, 1))

    def win(self):
        for i in self._player:
            if i.get_score() >= self._target:
                return i._name
#/
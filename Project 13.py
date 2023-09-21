from random import shuffle

class Card:
    _value_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8":8, "9":9, "10": 10, "j": 11, "q": 12, "k": 13, "a": 14}
    def __init__(self, number, suit):
        if str(number).lower() not in [str(num) for num in range(2, 11)] + list("jqka"):
            raise Exception("Number wasn't 2-10 or J, Q, K, or A.")
        else:
            self.number = str(number).lower()
        if suit.lower() not in ["clubs", "hearts", "diamonds", "spades"]:
            raise Exception("Suit wasn't one of: clubs, hearts, spades, or diamonds.")
        else:
            self.suit = suit.lower()
            
    def __str__(self):
        return(f'{self.number} of {self.suit.lower()}')
    
    def __repr__(self):
        return(f'Card(str({self.number}), "{self.suit}")')
    
    def __eq__(self, other):
        if self.number == other.number:
            return True
        else:
            return False
    
    def __lt__(self, other):
        if self._value_dict[self.number] < self._value_dict[other.number]:
            return True
        else: 
            return False
    
    def __gt__(self, other):
        if self._value_dict[self.number] > self._value_dict[other.number]:
            return True
        else:
            return False
    def __add__(self, other): 
      value = self._value_dict.get(self.number)
      other_value = self._value_dict.get(other.number)
      return value + other_value
    def __radd__(self , other): 
      value = self._value_dict.get(self.number)
      if type(other) == int or type(other) == float: 
       sum = value + other
      else: 
       sum = value + _value_dict.get(other.number)
      return sum

class Deck:
    _suits = ["clubs", "hearts", "diamonds", "spades"]
    _numbers = [str(num) for num in range(2, 11)] + list("jqka")
    
    def __init__(self):
        self.cards = [Card(number, suit) for suit in self._suits for number in self._numbers]
                      
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, key):
        return self.cards[key]
    def __setitem__(self, index, value):
        self.cards[index] = value

import queue
class Hand:
    def __init__(self, *cards):
        self.cards = [card for card in cards]
        
    def __str__(self):
        vals = [str(val) for val in self.cards]
        return(', '.join(vals))
    
    def __repr__(self):
        vals = [repr(val) for val in self.cards]
        return(', '.join(vals))
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, key):
        return self.cards[key]
    
    def __setitem__(self, key, value):
        self.cards[key] = value
    
    def sum(self):
        # remember, when we compare to Ace of Hearts, we are really only comparing the values,
        # and ignoring the suit.
        number_aces = sum(1 for card in self.cards if card == Card("a", "hearts"))
        non_ace_sum = sum(card for card in self.cards if card != Card("a", "hearts"))
        
        if number_aces == 0:
            return non_ace_sum
        
        else:
            # only 2 options 1 ace is 11 the rest 1 or all 1
            high_option = non_ace_sum + number_aces*1 + 10
            low_option = non_ace_sum + number_aces*1
            
            if high_option <= 21:
                return high_option
            else:
                return low_option
            
    def add(self, *cards):
        self.cards = self.cards + list(cards)
        return self
    
    def clear(self):
        self.cards = []


class Player:
    def __init__(self, name, strategy = None, dealer = False):
        self.name = name
        self.hand = Hand()
        self.dealer = dealer
        self.wins = 0
        self.draws = 0
        self.losses = 0
        if not self.dealer and not strategy:
            print(f"Non-dealer MUST have strategy.")
            
        self.strategy = strategy

        
    def __str__(self):
        summary = f'''{self.name}
------------
Wins: {self.wins/(self.wins+self.losses+self.draws):.2%}
Losses: {self.losses/(self.wins+self.losses+self.draws):.2%}
Draws: {self.draws/(self.wins+self.losses+self.draws):.2%}'''
        return summary
    
    def cards(self):
        if self.dealer:
            return [list(self.hand.cards)[0], "Face down"]
        else:
            return self.hand

import sys
class BlackJack:
    def __init__(self, *players, dealer = None):
        self.players = players
        self.deck = Deck()
        self.dealt = False
        if not dealer:
            self.dealer = Player('dealer', dealer=True)
        
    def deal(self):
        # shuffle the deck
        shuffle(self.deck)
        
        # we are ignoring dealing order and dealing to the dealer
        # first
        for _ in range(2):
            self.dealer.hand.add(*self.deck.draw())
            
        # deal 2 cards to each player
        for player in self.players:
            
            # first, clear out the players hands in case they've played already
            player.hand.clear()
            for _ in range(2):
                player.hand.add(*self.deck.draw())
                
        self.dealt = True
    
    def play(self):
        
        # make sure we've dealt
        if not self.dealt:
            sys.exit("You MUST deal the cards before playing.")
        
        # if dealer has face up ace or 10, checks to make sure 
        # doesn't have blackjack.
        # remember, when we compare to Ace of Hearts, we are really only comparing the values,
        # and ignoring the suit.
        face_value_ten = (Card("10", "hearts"), Card("j", "hearts"), Card("q", "hearts"), Card("k", "hearts"), Card("a", "hearts"))
        if self.dealer.cards()[0] in face_value_ten:
            
            if self.dealer.hand.sum() == 21:
                # winners get a draw, losers
                # get a loss
                for player in self.players:
                    if player.hand.sum() == 21:
                        player.draws += 1

                    else:
                        player.losses += 1
                
                return "GAME OVER"
                

        # if the dealer doesn't win with a blackjack,
        # the players now know the dealer doesn't 
        # have a blackjack
        
            
        # if the dealer doesn't have blackjack
        for player in self.players:
            # players play using their strategy until they hold
            while True:
                player_move = player.strategy(self, player)

                if player_move == "hit":
                    player.hand.add(*self.deck.draw())
                else:
                    break

        # dealer draws until >= 17
        while self.dealer.hand.sum() < 17:
            self.dealer.hand.add(*self.deck.draw())

        # if the dealer gets 21, players who get 21 draw
        # other lose
        if self.dealer.hand.sum() == 21:
            for player in self.players:
                if player.hand.sum() == 21:
                    player.draws += 1

                else:
                    player.losses += 1

        # otherwise, dealer has < 21, anyone with more wins, same draws,
        # and less loses
        elif self.dealer.hand.sum() < 21:
            for player in self.players:

                if player.hand.sum() > 21:
                    # player busts
                    player.losses += 1

                elif player.hand.sum() > self.dealer.hand.sum():
                    # player wins
                    player.wins += 1

                elif player.hand.sum() == self.dealer.hand.sum():
                    # player ties
                    player.draws += 1

                else:
                    # player loses
                    player.losses += 1

        # if dealer busts, players who didn't bust, win
        # players who busted, lose -- this is the house's edge
        else:
            for player in self.players:

                if player.hand.sum() < 21:
                    # player won
                    player.wins += 1

                else:
                    # player busted
                    player.losses += 1
            
        return "GAME OVER"


#Question 1
lucky_deck = Deck()
shuffle(lucky_deck)
for i in range(10): 
  print(lucky_deck[i])
'''
Before shuffle it,the cards are from 2 to a and from clubs to hears to diamonds, and spades.
After shuffle it, the cards just have no sequences. 
'''

#Question 2
print(Card("2", "clubs") + Card("k", "diamonds")) # 15
print(Card("k", "hearts") + Card("q", "hearts"))
print(Card("k", "diamonds") + Card("a", "spades") + Card("5", "hearts"))

#Question 3
x = Hand(Card("a", "diamonds"), Card("k", "hearts"), Card("a", "spades")) 
print(sum(x))
x.add(Card("8", "hearts"))
print(sum(x))

#Question 4
def always_hit_once(my_blackjack_game, me) -> str:
    """
    This is a simple strategy where the player
    always hits once.
    """
    if len(me.hand) == 3:
        return "hold"
    else:
        return "hit"
def seventeen_plus(my_blackjack_game, me) -> str:
    """
    This is a simple strategy where the player holds if the sum
    of cards is 17+, and hits otherwise.
    """
    if me.hand.sum() >= 17:
        return "hold"
    else:
        return "hit"

player1 = Player("John", seventeen_plus)
player2 = Player("Paul", always_hit_once)


for i in range(0,1000):
  game = BlackJack(player1, player2)
  game.deal()
  game.play()
  
print(player1.wins)
print(player2.wins)



#Question 5
def eighteen_plus(my_blackjack_game, me) -> str:
    """
    This is a simple strategy where the player holds if the sum
    of cards is 18+, and hits otherwise.
    """
    if me.hand.sum() >= 18:
        return "hold"
    else:
        return "hit"

player1 = Player("John", eighteen_plus)
player2 = Player("Paul", always_hit_once)


for i in range(0,1000):
  game = BlackJack(player1, player2)
  game.deal()
  game.play()
  
print(player1.wins)
print(player2.wins)








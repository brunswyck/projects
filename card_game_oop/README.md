# playing a card game
## description
a deck of cards gets created 
split between the different players  
each player plays a card at every turn  
until there are no cards left  
- name of the game: WeTakeYourMoney  

## game class
- WeTakeYourMoney = Game(no_of_players, no_of_cards)
- Game has no_of_players Player instances with player properties
- Game has 52 card instances with card properties  
  -> cards_per_player = 52 // no_of_players
- randomly shuffle those 52 card instances  
  -> shuffle_cards()
- game ends  
  -> every player has 0 card instances left
## player class
- properties:  
  -> cardsPlayed  
  -> cards_in_hand = 52 / no_of_players
  
- split among numberOfPlayers (get set state in WeTakeYourMoney)

## card class
- properties:  
  -> cards = {
    name = "ace", points = 1, 
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "jack": 10, 
    "queen": 10,
    "king": 10
    
  }
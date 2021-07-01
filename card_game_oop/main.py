import pprint as pp
import random
import typing
from utils.card import Card

# COACHES' NOTES: I very much like the .gitignore file
# However, .idea should also be included in it and somehow
# the __pycache__ folder got uploaded too. Maybe you pushed it
# before adding the .gitignore file. 

# COACHES' NOTES: The README.md has unnecessary information. If the user
# wants to know the properties of a particular class, he just
# goes to the code of the particular class.
# Use the README to share non-code stuff, like a small description
# and how to install the project and how to run it.

# COACHES' NOTES: You should have followed the structure outlined.
# The main file is only used to call the program from.
# All the logic should be in other classes/files.

# COACHES' NOTES: It's hard to give you good feedback when you don't respect
# the guidelines.


# todo: document random ranges https://www.delftstack.com/howto/python/random-integers-between-range-python/
def shuffle_cards(deck_of_cards: list):
    # COACHES' NOTES : You should return the shuffled deck here
    random.shuffle(deck_of_cards)


def generate_card_instances():
    # COACHES' NOTES : You can copy the icons we had in the project description to
    # use instead of the names of the icon.
    card_properties = {"club": "black",
                       "diamond": "red",
                       "heart": "red",
                       "spade": "black"}
    cards = []  # how to initialize this as a list of Card without creating an instance?
    cards_in_game = {
        "ace": 1,
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
    card_number = 0
    
    # COACHES' NOTES : card_deck should have been the Deck class, with a
    # property self.cards
    card_deck = {
        card_number: {"color": "",          # "black" "spade" "jack" 10
                      "composition": "",
                      "name": "",
                      "points": 0
                      }
    }
    for card, points in cards_in_game.items():    # for every card: "ace" with points: 1 you have ----
        for composition, color in card_properties.items():  # ----> 4 compositions of which 2 are black & 2 are red

            card_deck[card_number] = {"color": color,
                                      "composition": composition,  # filling this card_deck list with dictionaries
                                      "name": card,
                                      "points": points}
            cards.append(Card(color, composition, card, points))
            card_number += 1
    return cards


if __name__ == '__main__':
    all_cards = generate_card_instances()
    print(all_cards)
    """ [[black club ace: 1], [red diamond ace: 1], [red heart ace: 1], [black spade ace: 1], ... """
    shuffle_cards(all_cards)
    print(all_cards)
    """ [[red heart three: 3], [black club ten: 10], [black spade queen: 10], [red heart ten: 10], """
    # pp.pprint([card.get_card_properties for card in all_cards])

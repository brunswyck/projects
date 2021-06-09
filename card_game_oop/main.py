import pprint as pp
import random
from utils.card import Card


# todo: document random ranges https://www.delftstack.com/howto/python/random-integers-between-range-python/
def shuffle_cards(deck_of_cards: Card):
    old_deck_values = list(deck_of_cards.get_card_properties())
    random.shuffle(old_deck_values)
    pp.pprint(old_deck_values)
    # use zip to put values back into dictionary
    for x in range(0, 51):
        print(x)
    # shuffled_deck
    # pp.pprint(dict(zip(deck_of_cards, old_deck_now_shuffled)))


def generate_card_instances():
    card_properties = {"club": "black", "diamond": "red", "heart": "red", "spade": "black"}
    cards = [Card]
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
    card_deck = {card_number: {"color": "", "composition": "", "name": "", "points": 0}}  # "black" "spade" "jack" 10
    for card, points in cards_in_game.items():
        for composition, color in card_properties.items():
            card_deck[card_number] = {"color": color, "composition": composition, "name": card, "points": points}
            # something going wrong here, the first card in the list = "class utils.card.Card" instead of black club ace 1
            cards.append(Card(color, composition, card, points))
            card_number += 1
    return cards


if __name__ == '__main__':
    all_cards = generate_card_instances()
    print(type(all_cards[0]))  # todo: fix this
    print(type(all_cards[1]))  # this one is properly filled but should be at 0


    # for card in all_cards:
    #     print(card.get_card_properties())
    # shuffle_cards(all_cards)

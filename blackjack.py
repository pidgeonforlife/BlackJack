"""
Name: Eric Choi
Date: April 23rd 2021
"""

import doctest
import random


class User:
    """ Represent a user where each instances of money and current cards is appended to self.
    """

    def __init__(self):
        """ Initiates a user class with $100 and an empty list of current cards in hand.

        :precondition: user's money must have 100
        :precondition: current_cards must be an empty list
        :postcondition: initiate a user class object with money and current cards appended to self
        """
        self.money = 100
        self.current_cards = []


class Dealer:
    """ Represents a dealer where each instances of deck of cards and current cards is appended to self.
    """

    def __init__(self):
        """ Initiates a dealer class with a deck of cards and empty list of current cards in hand.

        :precondition: deck_of_cards must be valid
        :precondition: current_cards must be an empty list
        :postcondition: initiate a dealer class object with a deck of cards and current cards appended to self
        """
        self.deck_of_cards = generate_deck_of_cards()
        self.current_cards = []


def generate_deck_of_cards():
    """Generate a deck of cards with the given lists of suits and numbers.

    :precondition: deck of cards must be less than or equal to 52 total cards
    :return: a deck of cards

    >>> deck_of_cards = generate_deck_of_cards()
    >>> len(deck_of_cards) == 52
    True
    """
    suits = ["Hearts", "Clubs", "Diamonds", "Spades"]
    numbers = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    deck = [Card(suit, number) for suit in suits for number in numbers]
    return deck


class Card:
    """ Represents a card where each instance has a suit and number.
    """

    def __init__(self, suit: str, number: str):
        """Initiate a card class.

        :param suit: a string
        :param number: a string
        :precondition: suit is a string of the card's name,
                        number is a string of the card's number
        :postcondition: initiates a card class object with suit and number

        >>> king_of_diamonds = Card("Diamonds", "King")
        >>> king_of_diamonds.suit
        'Diamonds'
        >>> king_of_diamonds.number
        'King'
        """
        self.suit = suit
        self.number = number

    def __str__(self):
        """ Return a readable string that represents the card object.

        :return: a readable string that represents the card object

        >>> king_of_diamonds = Card("Diamonds", "King")
        >>> print(king_of_diamonds)
        King of Diamonds
        """

        return f"{self.number} of {self.suit}"


def add_card_values(values):
    """ Add the card values for each party that are given in the current cards that the user and dealer holds.

    If an Ace card is within the current cards add the value of one. If there is a face card (King, Jack, Queen) add the
    value of ten.

    :param values: current_card value for user and dealer
    :precondition:
    :postcondition:
    :return: the total number of the values added

    """
    total_number = 0
    number_of_aces = 0
    face_cards = ["Jack", "Queen", "King", "Spades"]
    for card in values.current_cards:
        if card.number == "Ace":
            number_of_aces += 1
        elif card.number in face_cards:
            total_number += 10
        else:
            total_number += int(card.number)
    while number_of_aces > 0:
        big_number = total_number + 11
        if big_number <= 21:
            total_number += 11
        else:
            total_number += 1
        number_of_aces -= 1
    return total_number


def print_current_cards(user, dealer):
    """ Print out the current cards of the user and the dealer.

    :param user: a valid user object
    :param dealer: a valid dealer object
    :precondition: the user and dealer must both be a valid object
    :postcondition: will print out the current cards for each the user and dealer
    :return: the current cards of the user and dealer

    """
    print("The dealer's cards: ")
    for card in dealer.current_cards:
        print(card)
    print("The dealer's card value: " + str(add_card_values(dealer)))

    print("The user's cards: ")
    for card in user.current_cards:
        print(card)
    print("The user's card value: " + str(add_card_values(user)))


def process_win(user, dealer, wins_double, bet_amount, record):
    """ Process the win condition of the user and append the win to record, and reset the parties' current cards.

    :param user: a valid user object
    :param dealer: a valid dealer object
    :param wins_double: a boolean
    :param bet_amount: a string
    :param record: a valid dictionary
    :precondition: if win_double is true, user wins double the amount that the user bets
                    if wins_double is false, user wins but doesn't win double the amount that the user bets
    :postcondition: have the user win according to the user's situation and append the win to the record
    :return: append the win to game's record and reset the parties' current cards

    """
    if wins_double:
        print("Congrats! You won this round, you have won double your monies.")
        user.money += bet_amount * 2
    else:
        print("Congrats! You won this round.")
        user.money += bet_amount
    user.current_cards = []
    dealer.current_cards = []
    record["Wins"] += 1


def process_loss_or_draw(user, dealer, is_loss, bet_amount, record):
    """ Process the win or loss condition of the user and append it to the record.
    Additionally empty the user's and dealer's current cards.

    :param user: a valid user object
    :param dealer: a valid dealer object
    :param is_loss: a boolean
    :param bet_amount: a string
    :param record: a valid dictionary
    :precondition: if is_loss is true, user loses the amount of money the user bets
                    if loss is false, user and dealer makes a draw
    :postcondition: have the user lose or draw according to the user's situation and append the result to the record
    :return: append the result of the round to the game's record and reset the current cards of dealer and user

    """
    if is_loss:
        print("Your card value is greater than 21! You lost " + str(bet_amount))
        user.money -= bet_amount
        record["Loses"] += 1
    else:
        print("It's a draw!")
        record["Draws"] += 1
    user.current_cards = []
    dealer.current_cards = []


def less_than_twenty_one(user):
    """ When the current value of the cards that the user holds is less than 21 return 'y' otherwise, 'n'.

    :param user: a valid user object
    :precondition: user must be a valid user object
    :precondition: user's total current card value must be less than 21 to return 'y' otherwise 'n'
    :return: 'y' when current card value is less than 21 and 'n' if greater

    """
    if add_card_values(user) < 21:
        return "y"
    return "n"


def player_draw_card(user, deck):
    """ Give the option for the user to choose if he/she would like to draw a card.

    :param user: a valid user object
    :param deck: a list
    :precondition: user must be a valid user object
    :precondition: deck must be a list
    :return: "y" or "n" according to the user's given input

    """
    user_input = input("Your current card value is " +
                       str(add_card_values(user)) +
                       ". Would you like to draw a card? (y/n): ")
    if user_input != "y":
        return "n"
    else:
        new_card = deck.pop(random.randrange(len(deck)))
        user.current_cards.append(new_card)
        print("You picked a(n) " + new_card.__str__())
        return "y"


def end_game(user, record):
    """ Prints out the ending for the game and shows a scoreboard/record.

    :param user: a valid user object
    :param record: a valid record object
    :precondition: user must be a valid user object
    :precondition: record must be a valid record object
    :return: an ending statement and prints the scoreboard/record of the user

    """
    print("The end! Here is your record.")
    for key, value in record.items():
        print(key + ": " + str(value), end="\n")
    print("Your money at the end of the game: " + str(user.money))


class Game:
    """ Represent a game where each instances will have a user dealer, and a scoreboard.
    """

    def __init__(self, user, dealer):
        """ Initiate a game class.

        :param user: a valid user object
        :param dealer: a valid dealer object
        :precondition: user and dealer both must be valid
        :precondition: records must be a dictionary
        :postcondition: initiates a game class with user, dealer, and scoreboard/record

        """
        self.user = user
        self.dealer = dealer
        self.record = {"Wins": 0, "Losses": 0, "Draws": 0}

    def start_game(self):
        """ Runs the game and ends when the preconditions are met.

            The game will be run between the dealer and the user, where in each instances the user wins, loses or draws,
            it will be tallied in the records and printed out. User will win money, lose money, or break even and have
            the money the user bets returned.

        :precondition: each round will begin when the dealer states how much money the user has and will end when:
                        - user has no money left to bet and loses(money) then gets tallied to result
                        - dealer's hand exceeds over 21 and the user wins(money) then gets tallied to the result
                        - the dealer and user's hand both end up with 21 it will be considered a draw
                        - if the user's hand exceeds over 21 and loses(money) then gets tallied to the result
        :precondition: must have a valid user object, a valid dealer object, and a valid record object
        :postcondition: game will continue to loop while the player has money or the card deck has more than 0 cards
        """
        deck = self.dealer.deck_of_cards
        while deck and self.user.money > 0:
            print("The deck currently has: " + str(len(self.dealer.deck_of_cards)))
            bet_amount = int(input("You currently have " + str(self.user.money) +
                                   ". How much would you like to bet? (Minimum bet amount is $10): "))
            if 10 > bet_amount or bet_amount > self.user.money:
                print("Invalid amount. Try again.")
                continue
            for _ in range(2):
                self.user.current_cards.append(deck.pop(random.randrange(len(deck))))
                self.dealer.current_cards.append(deck.pop(random.randrange(len(deck))))
            print_current_cards(self.user, self.dealer)
            player_card_value = add_card_values(self.user)
            dealer_card_value = add_card_values(self.dealer)
            print(str(dealer_card_value))
            while dealer_card_value <= 14:
                print("The dealer's card value is: " + str(dealer_card_value))
                input("The dealer card value is less than or equal to 14, so he will pick a card out of the deck."
                      "(Press enter to continue)")
                new_card = deck.pop(random.randrange(len(deck)))
                self.dealer.current_cards.append(new_card)
                print("The dealer drew out " + new_card.__str__())
                dealer_card_value = add_card_values(self.dealer)
                input("The dealer's new card value is " + str(dealer_card_value) + "(Press enter to continue)")

            if dealer_card_value > 21:
                if len(self.dealer.current_cards) == 3:
                    process_win(self.user, self.dealer, True, bet_amount, self.record)
                    continue

                else:
                    process_win(self.user, self.dealer, False, bet_amount, self.record)
                    continue

            user_input = less_than_twenty_one(self.user)

            while player_card_value < 21 and user_input == "y":
                user_input = player_draw_card(self.user, deck)

            if player_card_value > 21:
                process_loss_or_draw(self.user, self.dealer, True, bet_amount, self.record)
                continue

            if player_card_value == dealer_card_value:
                process_loss_or_draw(self.user, self.dealer, False, bet_amount, self.record)
                continue

            if player_card_value > dealer_card_value:
                process_win(self.user, self.dealer, True, bet_amount, self.record)
                continue

        end_game(self.user, self.record)


def main():
    """ Drive the program. """
    doctest.testmod(verbose=True)
    user = User()
    dealer = Dealer()
    game = Game(user, dealer)
    game.start_game()


if __name__ == '__main__':
    main()

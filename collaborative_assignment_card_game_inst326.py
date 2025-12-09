
#Steve Rozario

import random

class Card:
    """This represesnts a card in the game. The card can be a normal or special 
    card.
    
    Attributes:
        suit (str): The suit of the card.
        ranktype (str): The value/rank of the card.
        action (str): Special effects of the card. 
    
    """
    def __init__(self, suit, ranktype, action=None):
    
        """Creates card object with the suit, ranktype, and action. 

        Args:
            suit (str): The suit of the card.
            ranktype (str): The value/rank of the card.
            action (str): Special effects of the card. 
            
        Side effects:
            None.
        """
        self.suit = suit
        self.ranktype = ranktype
        self.action = action
    
    def __repr__(self):
        """String representation of the card 

        Returns:
            str: Description of the card and any special actions that was done.
        """
        if self.action:
            return f"{self.ranktype} of {self.suit} ({self.action})"
        return f"{self.ranktype} of {self.suit}"
    
    


class Deck:
    """Shows the deck of cards that will be used. The deck has normal and action
    cards. Additionally, the deck class will handle shuffling, pulling cards, 
    and looping the deck back once the cards have run out.

    Raises:
        ValueError: Happens when there isn't enough cards and deck is trying to
        reload the cards already played.

    Returns:
        Deck: Initialized deck object
    """
    SUITS = ["HEARTS", "SPADES", "DIAMONDS", "CLUBS"]
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    ACTIONS = ["SKIP", "DRAW 2 CARDS", "REVERSE"]
    
    def __init__(self):
        """Creates the cards, card shuffling, and selecting random ranks for 
        wild cards.
        """
        self.cards = []           
        self.played_cards = []   

        self.wild_rank = random.choice(self.RANKS)
        self.build_deck()
        self.shuffle()
        
    def build_deck(self):
        """Makes the complete deck with the normal cards and the action cards. 
        The action cards have special effects(Skip, reverse, Draw 2 cards).
        """
        for suit in self.SUITS:
            for rank in self.RANKS:
                self.cards.append(Card(suit, rank))
        
        for suit in self.SUITS:
            for action in self.ACTIONS:
                self.cards.append(Card(suit, "ACTION", action))
                
    def shuffle(self):
        """Cards in the deck get randomized.
        """
        random.shuffle(self.cards)
        
    def card_pull(self):
        """Draws a card and if needed, reshuffles the card pile that is already 
        used.

        Returns:
            Card: Card taken from the top of the deck.
        """
        if not self.cards:
            self.reload_played_cards()
        return self.cards.pop()
    
    def reload_played_cards(self):
        """Reloads the cards played back into the deck excluding the top card.
        
        Raises:
            ValueError: In case there isn't enough cards to rebuild the deck.
        """
        if len(self.played_cards) <= 1:
            raise ValueError("Not enough cards to restart deck")
        
        top = self.played_cards[-1]
        self.cards = self.played_cards[:-1]
        self.played_cards = [top]
        self.shuffle()
        
    def start_game(self):
        """Draws a card that is valid and not an action card.

        Returns:
            Card: The card that starts the game(Non-action card).
        """
        card = self.card_pull()
        
        while card.action is not None:
            self.cards.insert(0, card)
            self.shuffle()
            card = self.card_pull()
        
        self.played_cards.append(card)
        return card


def card_validation(hand, played_card, current_suit):
    """Returns the valid card using Crazy 8 and Uno rules. It handles concerns
    determining whether or not the cards played are valid/invalid.

    Args:
        hand (list[Card]): The hand player has currently.
        played_card (Card): The recent card on top of the card pile
        current_suit (str): To follow the suit that is being played unless it 
        is changed by the wild card(8).

    Returns:
        Card or None: Plays the first card that is valid, otherwise it will 
        return none.
    """
    valid_cards= []
    for card in hand:

        #rule: cards that follow uno rules(special)
        if card.action is not None:
            valid_cards.append(card)
        
        #rule: Crazy 8/wildcard
        elif card.ranktype == "8":
            valid_cards.append(card)
            
        #rule: Makes sure the suit matches
        elif card.suit == current_suit:
            valid_cards.append(card)
            
        #rule: The ranks of the cards match 
        elif card.ranktype == played_card.ranktype:
            valid_cards.append(card)
            
            
    return valid_cards[0] if valid_cards else None
            
        
        
#Brandon
def apply_special_action(card, get_next_player, draw_cards, reverse_direction):
    """Applies a special card action (skip, reverse, draw 2 cards). Uses mock
    functions for the purpose of deliverable."""
    
    if card.action is None:
        return "NO_ACTION"
    
    if card.action == "SKIP":
        next_player = get_next_player()
        return f"Skipped {next_player}"
    
    elif card.action == "REVERSE":
        reverse_direction()
        return "Direction reversed"
    
    elif card.action == "DRAW 2 CARDS":
        next_player = get_next_player()
        draw_cards(next_player, 2)
        return f"{next_player} draws 2 cards."
    
    return "UNKNOWN_ACTION"


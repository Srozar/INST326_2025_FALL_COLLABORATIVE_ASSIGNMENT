
#Steve Rozario

import random
from typing import List, Optional

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
            
        
#Brandon Appleton

class Player:
    """
    Represents a player in the Crazy Eights/Uno game.

    Attributes:
        name (str): Name of the player.
        hand (list[Card]): List of cards currently held by the player.
        is_cpu (bool): Whether the player is controlled by CPU.
    """

    def __init__(self, name, is_cpu=False):
        """
        Initializes a Player object with a name, an empty hand, and CPU flag.

        Args:
            name (str): The name of the player.
            is_cpu (bool, optional): True if CPU-controlled, False otherwise. Defaults to False.

        Side effects:
            Creates an empty hand for the player.
        """
        self.name = name
        self.hand = []
        self.is_cpu = is_cpu

    def draw_card(self, deck, count=1):
        """
        Draws one or more cards from the deck and adds them to the player's hand.

        Args:
            deck (Deck): The deck to draw cards from.
            count (int, optional): Number of cards to draw. Defaults to 1.

        Side effects:
            Cards are removed from the deck and added to the player's hand.
        """
        for _ in range(count):
            self.hand.append(deck.card_pull())

    def play_card(self, played_card, current_suit):
        """
        Selects a card to play. Human players choose via input, CPU players pick automatically.

        Args:
            played_card (Card): The card currently on top of the pile.
            current_suit (str): The current suit to match.

        Returns:
            Card or None: The chosen card to play, or None if drawing a card.

        Side effects:
            For humans: prompts terminal input.
            For CPU: prints chosen card to terminal.
        """
        valid_cards = [card for card in self.hand if card_validation([card], played_card, current_suit)]
        if not valid_cards:
            return None

        if self.is_cpu:
            chosen_card = valid_cards[0]  # Simple AI: play first valid card
            print(f"{self.name} plays: {chosen_card}")
            return chosen_card

        # Human player input
        print(f"\n{self.name}'s turn. Current card: {played_card} (Suit: {current_suit})")
        print("Your hand:")
        for i, card in enumerate(self.hand, 1):
            print(f"{i}: {card}")
        print("\nValid cards to play:")
        for i, card in enumerate(valid_cards, 1):
            print(f"{i}: {card}")

        while True:
            try:
                choice = int(input(f"Select a card to play (1-{len(valid_cards)}) or 0 to draw: "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(valid_cards):
                    return valid_cards[choice - 1]
            except ValueError:
                pass
            print("Invalid choice. Try again.")


class Game:
    """
    Represents a Crazy Eights/Uno game session.

    Attributes:
        deck (Deck): The deck used for the game.
        players (list[Player]): List of players participating in the game.
        current_player_idx (int): Index of the player whose turn it is.
        direction (int): Direction of play (1 for clockwise, -1 for counterclockwise).
        played_card (Card): The most recently played card.
        current_suit (str): The current suit to match in play.
    """

    def __init__(self, players):
        """
        Initializes the Game with a deck, players, and deals starting hands.

        Args:
            players (list[Player]): List of Player objects participating.

        Side effects:
            Deals 7 cards to each player.
            Draws a starting card for the game.
        """
        self.deck = Deck()
        self.players = players
        self.current_player_idx = 0
        self.direction = 1
        self.played_card = self.deck.start_game()
        self.current_suit = self.played_card.suit

        for player in self.players:
            player.draw_card(self.deck, 7)

    def next_player_index(self):
        """
        Calculates the index of the next player based on current direction.

        Returns:
            int: The index of the next player.
        """
        return (self.current_player_idx + self.direction) % len(self.players)

    def apply_action_card(self, card):
        """
        Applies the effect of action cards: SKIP, REVERSE, DRAW 2 CARDS.

        Args:
            card (Card): The action card that was played.

        Side effects:
            Modifies the game direction or forces the next player to draw cards.
            Updates current player index as needed.
        """
        next_idx = self.next_player_index()

        if card.action == "SKIP":
            print(f"{self.players[self.current_player_idx].name} played SKIP! {self.players[next_idx].name} is skipped!")
            self.current_player_idx = (next_idx + self.direction) % len(self.players)
        elif card.action == "REVERSE":
            print(f"{self.players[self.current_player_idx].name} played REVERSE! Changing direction.")
            self.direction *= -1
            self.current_player_idx = self.next_player_index()
        elif card.action == "DRAW 2 CARDS":
            print(f"{self.players[self.current_player_idx].name} played DRAW 2 CARDS! {self.players[next_idx].name} draws 2 cards.")
            self.players[next_idx].draw_card(self.deck, 2)
            self.current_player_idx = next_idx

    def choose_suit(self):
        """
        Prompts the player to choose a suit after playing a wild card (8).

        Returns:
            str: The suit chosen by the player.

        Side effects:
            Interactively asks the user for input in the terminal.
        """
        suits = Deck.SUITS
        print("You played an 8! Choose a suit:")
        for i, suit in enumerate(suits, 1):
            print(f"{i}: {suit}")
        while True:
            try:
                choice = int(input(f"Select a suit (1-{len(suits)}): "))
                if 1 <= choice <= len(suits):
                    return suits[choice - 1]
            except ValueError:
                pass
            print("Invalid choice. Try again.")

    def play_turn(self):
        """
        Executes a single turn for the current player.

        Returns:
            bool: True if the game is won during this turn, False otherwise.

        Side effects:
            Modifies player hands, current card, current suit, and current player index.
        """
        player = self.players[self.current_player_idx]
        chosen_card = player.play_card(self.played_card, self.current_suit)

        if chosen_card:
            player.hand.remove(chosen_card)
            self.deck.played_cards.append(chosen_card)
            self.played_card = chosen_card

            if chosen_card.ranktype == "8":
                # For CPU, pick a random suit
                if player.is_cpu:
                    self.current_suit = random.choice(Deck.SUITS)
                    print(f"{player.name} changes suit to {self.current_suit}")
                else:
                    self.current_suit = self.choose_suit()
            else:
                self.current_suit = chosen_card.suit

            if chosen_card.action:
                self.apply_action_card(chosen_card)
            else:
                self.current_player_idx = self.next_player_index()
        else:
            print(f"{player.name} has no valid cards. Drawing a card...")
            player.draw_card(self.deck)
            self.current_player_idx = self.next_player_index()

        if len(player.hand) == 0:
            print(f"\n{player.name} has won the game! Congratulations!")
            return True
        return False

    def start(self):
        """
        Starts the game loop, alternating turns until a player wins.

        Side effects:
            Runs the terminal interaction loop for gameplay.
        """
        print(f"Starting card: {self.played_card}")
        while True:
            if self.play_turn():
                break


def select_game_mode():
    """
    Prompts the user to choose a game mode.

    Returns:
        str: Either "hotseat" or "cpu" indicating the selected mode.
    """
    print("Select Game Mode:")
    print("1: Hot-seat two-player")
    print("2: Player vs CPU")
    while True:
        choice = input("Enter 1 or 2: ")
        if choice == "1":
            return "hotseat"
        elif choice == "2":
            return "cpu"
        print("Invalid choice. Try again.")


def main():
    """
    Main function to initialize and start the game based on user-selected mode.

    Side effects:
        Starts a terminal-based Crazy Eights/Uno game.
    """
    mode = select_game_mode()
    if mode == "hotseat":
        players = [Player("Player 1"), Player("Player 2")]
    else:  # Player vs CPU
        players = [Player("Player 1"), Player("CPU", is_cpu=True)]

    game = Game(players)
    game.start()


if __name__ == "__main__":
    main()
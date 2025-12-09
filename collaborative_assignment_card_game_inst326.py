
#Steve Rozario
def card_validation(hand, played_card, current_suit):
    """Returns the valid card using Crazy 8 and Uno rules. It handles concerns
    determining whether or not the cards played are valid/unvalid.

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
        #rule 4: Crazy 8/wildcard
        if card.ranktype == "8":
            valid_cards.append(card)
        
        #rule: cards that follow uno rules(special)
        elif card.action is not None:
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
    
    elif card.action == "DRAW 2 cards":
        next_player = get_next_player()
        draw_cards(next_player, 2)
        return f"{next_player} draws 2 cards."
    
    return "UNKNOWN_ACTION"

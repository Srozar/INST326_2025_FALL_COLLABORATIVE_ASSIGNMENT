def apply_special_action(card, get_next_player, draw_cards, reverse_direction):
    """Applies a special card action (skip, reverse, draw 2). Uses mock
    functions for the purpose of deliverable."""
    
    if card.action is None:
        return "NO_ACTION"
    
    if card.action == "SKIP":
        next_player = get_next_player()
        return f"Skipped {next_player}"
    
    elif card.action == "REVERSE":
        reverse_direction()
        return "Direction reversed"
    
    elif card.action == "DRAW 2":
        next_player = get_next_player()
        draw_cards(next_player, 2)
        return f"{next_player} draws 2 cards."
    
    return "UNKNOWN_ACTION"
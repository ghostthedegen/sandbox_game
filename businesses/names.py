def find_name(text, names):
    """Match what the player typed, ignoring capitals and extra spaces.

    Returns the name as the game spells it, or None if nothing matches.
    """

    typed = text.strip().lower()

    for name in names:
        if name.lower() == typed:
            return name

    return None

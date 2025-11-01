def cleanFlashcardContent(string: str) -> str:
    """
    Cleans the content of a flashcard input by removing tabs and newlines.

    This is used to ensure the content is in a format suitable for Quizlet, 
    where newlines and tabs are used to separate flashcards. The function
    replaces tabs and newlines with spaces and trims any leading/trailing 
    whitespace from the input string.

    Args:
        string (str): The raw flashcard content.

    Returns:
        str: The cleaned flashcard content without tabs, newlines, or extra spaces.
    """
    # Replace newlines and tabs with spaces and trim any leading/trailing spaces
    return string.replace('\n', ' ').replace('\t', ' ').strip()

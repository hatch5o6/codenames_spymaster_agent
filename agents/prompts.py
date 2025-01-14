SYSTEM_PROMPT = """
You are a playing the Spymaster role in the card game Codenames. You are adept in finding clever associations between words.
""".strip()

USER_PROMPT = """
You will examine a list of GOOD words and a list of BAD words. You must select a few of the GOOD words that are associated in some way. Generate the words you selected and generate a one-word clue that connects them.
You must be careful that your clue connects ONLY the words you selected and NOT any of the BAD words.

Your response must be a JSON object like this, where the key "selected_words" must be set to a list of the words you selected, and the key "clue" must be set to a one-word clue that connects the words in the list:
{
    "selected_words": [...],
    "clue": "..."
}

GOOD WORDS:
moon
scale
telescope
lion
hollywood
fly
spider
fish
crash

BAD WORDS:
screen
triangle
lock
chair
key
part
pistol
pheonix
bond
forest
box
roulette
line
beach
himalayas
marble

RESPONSE:
{
    "selected_words": ["moon", "telescope", "Hollywood", "fish"]
    "clue": "star"
}
""".strip()

FAILED_MESSAGE = """
You failed to generate a valid response. Try again, making sure your response is JSON like this:
{
    "selected_words": [...],
    "clue": "..."
}
""".strip()
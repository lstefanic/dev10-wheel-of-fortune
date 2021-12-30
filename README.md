# dev10-wheel-of-fortune

Play a version of Wheel of Fortune. Runs entirely in a terminal with a text-based UI

### Differences from the real game

- The wheel has 24 spaces: one Bankrupt, one Lose a Turn, and money values from $100 to $900 in increments of $50. There are two of each amount from $100 to $300, and one each of all other amounts
- If you guess a consonant that appears multiple times in the puzzle, the dollar amount you landed on is not multiplied. For example, if the phrase is "spaghetti and meatballs" and you guess T after landing on $600, you are awarded $600, not $1800
- You may only guess one consonant per turn. If you guess correctly, you do not get to respin the wheel and guess again
- There is no bonus money awarded for solving the puzzle. When the puzzle is solved, the round simply ends

### How to use

Download the files `wheel.py` and `phrases.json` and in a terminal, run `python wheel.py`

### Sample gameplay

The text of a sample game can be seen in the jupyter notebook file `wheel.ipynb`

### Credits

The `phrases.json` file is the output of web scrapper code in `webscrapper.py` provided by Scott Partacz

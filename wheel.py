import random
import math
import json

def build_wheel():

    result = ["Bankrupt", "Lose a Turn"]
    for dollar_amount in range(100,950,50):
        result.append(dollar_amount)
    for dollar_amount in range(100,350,50):
        result.append(dollar_amount)
    return tuple(result)

def spin_wheel():
    index = math.floor(random.random() * len(WHEEL))
    return WHEEL[index]

def choose_phrase_and_category(used_phrases):
    f = open("phrases.json")
    phrase_dict = json.load(f)
    f.close()
    phrase_list = list(phrase_dict.keys())
    while ( True ):
        index = math.floor(random.random() * len(phrase_list))
        phrase = phrase_list[index]
        category = phrase_dict[phrase]
        if ( phrase.lower() not in used_phrases ):
            used_phrases.add(phrase.lower())
            return [phrase.lower(), category.lower()]

# Display category, phrase with guessed letters filled in, and set of guessed letters
def display_puzzle_info(phrase,category,guessed_letters):

    revealed = "    %s: " % category
    for i in range(len(phrase)):
        if ( phrase[i] in guessed_letters or phrase[i] in SPECIAL_CHARS ):
            revealed += phrase[i]
        else:
            revealed += "_"
        revealed += " "
    print(revealed[0:-1])

    guessed = "    Guessed letters: "
    for letter in sorted(guessed_letters):
        guessed += letter + " "
    print(guessed[0:-1] + "\n")

def display_score(player_money):

    score = "    Scoreboard: "
    for i in range(3):
        score += "$%u | " % player_money[i]
    print(score[0:-3] + "\n")

# Get a consonant inputted by a player
def get_consonant():

    guess = "1"
    while ( not (guess.isalpha() and len(guess) == 1 and guess not in VOWELS) ):
        guess = input("Guess a consonant: ")
    return guess.lower()

# Get a vowel inputted by a player
def get_vowel():

    guess = "1"
    while ( not (guess.isalpha() and len(guess) == 1 and guess in VOWELS) ):
        guess = input("Guess a vowel: ")
    return guess.lower()

# Return True if there are still unguessed consonants, False if not
def consonants_left(phrase,guessed_letters):
    
    for i in range(len(phrase)):
        if ( phrase[i] not in VOWELS and phrase[i] not in guessed_letters ):
            return True
    return False

def buy_vowels(player_money,phrase,category,guessed_letters,player):

    while ( player_money[player] >= 250 ):
        action = input("Buy a vowel for $250? (y/n): ")
        if ( action == "n" ):
            break
        if ( action == "y" ):
            vowel = get_vowel()
            guessed_letters.add(vowel)
            player_money[player] -= 250
            if ( phrase.find(vowel) != -1 ):
                print("\n    You guessed correctly!")
                display_puzzle_info(phrase,category,guessed_letters)
                display_score(player_money)
            else:
                print("\n    That letter is not there!\n")
                break

# Allow player to attempt to solve the puzzle
# Return True if puzzle is solved, False if not
def guess_phrase(phrase):

    while ( True ):
        action = input("Solve the puzzle? (y/n): ")
        if ( action == "n" ):
            return False
        if ( action == "y" ):
            guess = input("Enter your guess: ")
            if ( guess.lower() == phrase ):
                print("\n    You solved the puzzle!")
                return True
            else:
                print("\n    That guess is incorrect")
                return False

def play_standard_round(player_money,used_phrases):

    [phrase, category] = choose_phrase_and_category(used_phrases)
    guessed_letters = set()
    round_over = False
    while( not round_over ):
        for player in range(3):
            if ( round_over ):
                break
            input("\nPlayer %u, it's your turn. Hit Enter to spin the wheel" % (player+1))
            space = spin_wheel()
            if ( space == "Bankrupt" ):
                print("\n    You landed on Bankrupt")
                player_money[player] = 0
            elif ( space == "Lose a Turn" ):
                print("\n    You landed on Lose a Turn")
            else:
                # Wheel spin landed on money

                print("\n    You landed on $%u" % space)
                display_puzzle_info(phrase,category,guessed_letters)
                display_score(player_money)
                if ( not consonants_left(phrase,guessed_letters) ):
                    print("There are no consonants left")
                    buy_vowels(player_money,phrase,category,guessed_letters,player)
                    round_over = guess_phrase(phrase)
                else:
                    consonant = get_consonant()
                    guessed_letters.add(consonant)
                    if ( phrase.find(consonant) != -1 ):
                        player_money[player] += space
                        print("\n    You guessed correctly!")
                        display_puzzle_info(phrase,category,guessed_letters)
                        display_score(player_money)
                        buy_vowels(player_money,phrase,category,guessed_letters,player)
                        round_over = guess_phrase(phrase)
                    else:
                        print("\n    That letter is not there!")

def play_final_round(used_phrases):

    [phrase, category] = choose_phrase_and_category(used_phrases)
    guessed_letters = {"r", "s", "t", "l", "n", "e"}
    display_puzzle_info(phrase,category,guessed_letters)
    for i in range(3):
        guessed_letters.add(get_consonant())
    guessed_letters.add(get_vowel())
    print("")
    display_puzzle_info(phrase,category,guessed_letters)
    guess = input("Enter your guess: ")
    if ( guess.lower() == phrase ):
        print("\n    Correct! You win the grand prize of $10000!\n")
    else:
        print("\n    Sorry, the word was %s\n" % phrase)

def play_game():

    player_money = [0, 0, 0]
    used_phrases = set()

    for round in range(2):
        print("\nPlayers 1, 2, and 3: Welcome to round %u" % (round+1))
        play_standard_round(player_money,used_phrases)

    best_player = 0
    most_money = player_money[best_player]
    for player in range(1,3):
        if player_money[player] > most_money:
            best_player = player
            most_money = player_money[best_player]
    print("\nPlayer %u, you move on to Round 3\n" % (best_player+1))
    play_final_round(used_phrases)

############################## Main instructions ##############################

WHEEL = build_wheel()
VOWELS = ("a", "A", "e", "E", "i", "I", "o", "O", "u", "U")
SPECIAL_CHARS = (" ", ".", "!", "?", "&", "'", "-")

play_game()
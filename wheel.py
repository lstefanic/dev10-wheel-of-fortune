import random
import math
import json

def build_wheel():

    result = ["Bankrupt", "Lose a Turn"]
    for dollar_amount in range(100,950,50):
        result.append(dollar_amount)
    for dollar_amount in range(100,350,50):
        result.append(dollar_amount)
    return result

def spin_wheel():
    index = math.floor(random.random() * len(WHEEL))
    return WHEEL[index]

def choose_phrase():
    f = open("phrases.json")
    phrase_dict = json.load(f)
    f.close()
    phrase_list = list(phrase_dict.keys())
    index = math.floor(random.random() * len(phrase_list))
    phrase = phrase_list[index]
    category = phrase_dict[phrase]
    return [phrase.lower(), category.lower()]

def display_puzzle_info():

    revealed = "    %s: " % category
    for i in range(len(secret_phrase)):
        if ( secret_phrase[i] in guessed_letters or secret_phrase[i] in SPECIAL_CHARS ):
            revealed += secret_phrase[i]
        else:
            revealed += "_"
        revealed += " "
    print(revealed[0:-1])

    guessed = "    Guessed letters: "
    for letter in sorted(guessed_letters):
        guessed += letter + " "
    print(guessed[0:-1] + "\n")

def display_score():

    score = "    Scoreboard: "
    for i in range(3):
        score += "$%u | " % player_money[i]
    print(score[0:-3] + "\n")

def get_consonant():

    guess = "1"
    while ( not (guess.isalpha() and len(guess) == 1 and guess not in VOWELS) ):
        guess = input("Guess a consonant: ")
    return guess.lower()

def get_vowel():

    guess = "1"
    while ( not (guess.isalpha() and len(guess) == 1 and guess in VOWELS) ):
        guess = input("Guess a vowel: ")
    return guess.lower()

def get_guess():
    
    guess = input("Enter your guess: ")
    return guess.lower()

def consonants_left():
    
    for i in range(len(secret_phrase)):
        if ( secret_phrase[i] not in VOWELS and secret_phrase[i] not in guessed_letters ):
            return True
    return False

def buy_vowels(player):

    while ( player_money[player] >= 250 ):
        action = input("Buy a vowel for $250? (y/n): ")
        if ( action == "n" ):
            break
        if ( action == "y" ):
            guess = get_vowel()
            guessed_letters.add(guess)
            player_money[player] -= 250
            print("")
            display_puzzle_info()
            display_score()

def guess_phrase():

    action = input("Solve the puzzle? (y/n): ")
    if ( action == "y" ):
        guess = get_guess()
        if ( guess == secret_phrase ):
            print("\n    You solved the puzzle!")
            return True
        else:
            print("\n    That guess is incorrect")
    return False

def standard_round():

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
                print("\n    You landed on $%u" % space)
                display_puzzle_info()
                display_score()
                if ( not consonants_left() ):
                    print("There are no consonants left")
                    buy_vowels(player)
                    round_over = guess_phrase()
                else:
                    consonant = get_consonant()
                    guessed_letters.add(consonant)
                    if ( secret_phrase.find(consonant) != -1 ):
                        player_money[player] += space
                        print("\n    You guessed correctly!")
                        display_puzzle_info()
                        display_score()
                        buy_vowels(player)
                        round_over = guess_phrase()
                    else:
                        print("\n    That letter is not there!")

def final_round():

    display_puzzle_info()
    for i in range(3):
        guessed_letters.add(get_consonant())
    guessed_letters.add(get_vowel())
    print("")
    display_puzzle_info()
    guess = get_guess()
    if ( guess == secret_phrase ):
        print("\n    Correct! You win the grand prize of $10000!\n")
    else:
        print("\n    Sorry, the word was %s\n" % secret_phrase)

# Game setup
WHEEL = build_wheel()
VOWELS = ["a", "A", "e", "E", "i", "I", "o", "O", "u", "U"]
SPECIAL_CHARS = [" ", "!", "?", "&", "'", "-"]
player_money = [0, 0, 0]
guessed_letters = set()

# Rounds 1 and 2
for round in range(2):
    print("\nPlayers 1, 2, and 3: Welcome to round %u" % (round+1))
    guessed_letters.clear()
    [secret_phrase, category] = choose_phrase()
    standard_round()

# Round 3
best_player = 0
most_money = player_money[best_player]
for player in range(1,3):
    if player_money[player] > most_money:
        best_player = player
        most_money = player_money[best_player]
print("\nPlayer %u, you move on to Round 3\n" % (best_player+1))
guessed_letters = {"r", "s", "t", "l", "n", "e"}
[secret_phrase, category] = choose_phrase()
final_round()
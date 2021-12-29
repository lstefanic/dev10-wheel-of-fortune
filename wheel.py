import random
import math

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

def choose_word():
    f = open("words.txt")
    words = f.read().splitlines()
    f.close()
    index = math.floor(random.random() * len(words))
    return words[index]

def display_word_info():

    revealed = "    Secret word: "
    for i in range(len(secret_word)):
        if ( secret_word[i] in guessed_letters ):
            revealed += secret_word[i]
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

def guess_consonant():

    guess = "1"
    while ( not (guess.isalpha() and len(guess) == 1 and guess not in VOWELS) ):
        guess = input("Guess a consonant: ")
    return guess.lower()

def guess_vowel():

    guess = "1"
    while ( not (guess.isalpha() and len(guess) == 1 and guess in VOWELS) ):
        guess = input("Guess a vowel: ")
    return guess.lower()

def guess_word():
    
    guess = "1"
    while ( not guess.isalpha() ):
        guess = input("Guess a word: ")
    return guess.lower()

def consonants_left():
    
    for i in range(len(secret_word)):
        if ( secret_word[i] not in VOWELS and secret_word[i] not in guessed_letters ):
            return True
    return False

def buy_vowels():

    while ( player_money[player] >= 250 ):
        action = input("Buy a vowel for $250? (y/n): ")
        if ( action == "n" ):
            break
        if ( action == "y" ):
            guess = guess_vowel()
            guessed_letters.add(guess)
            player_money[player] -= 250
            print("")
            display_word_info()
            display_score()

# Game setup
WHEEL = build_wheel()
VOWELS = ["a", "A", "e", "E", "i", "I", "o", "O", "u", "U"]
player_money = [0, 0, 0]
used_words = set()
guessed_letters = set()

# Rounds 1 and 2
for round in range(2):
    print("\nPlayers 1, 2, and 3: Welcome to round %u" % (round+1))
    guessed_letters.clear()
    secret_word = choose_word()
    while (secret_word in used_words ):
        secret_word = choose_word()
    used_words.add(secret_word)
    round_is_over = False
    while ( not round_is_over ):
        for player in range(3):
            if ( round_is_over ):
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
                display_word_info()
                display_score()
                if ( not consonants_left() ):
                    print("There are no consonants left")
                    buy_vowels()
                    action = input("Guess the word? (y/n): ")
                    if ( action == "y" ):
                        guess = guess_word()
                        if ( guess == secret_word ):
                            print("\n    You found the secret word!")
                            round_is_over = True
                        else:
                            print("\n    That guess is incorrect")
                else:
                    guess = guess_consonant()
                    guessed_letters.add(guess)
                    if ( secret_word.find(guess) != -1 ):
                        player_money[player] += space
                        print("\n    You guessed correctly!")
                        display_word_info()
                        display_score()
                        buy_vowels()
                        action = input("Guess the word? (y/n): ")
                        if ( action == "y" ):
                            guess = guess_word()
                            if ( guess == secret_word ):
                                print("\n    You found the secret word!")
                                round_is_over = True
                            else:
                                print("\n    That guess is incorrect")
                    else:
                        print("\n    That letter is not there!")

# Round 3
best_player = 0
most_money = player_money[best_player]
for player in range(1,3):
    if player_money[player] > most_money:
        best_player = player
        most_money = player_money[best_player]
print("\nPlayer %u, you move on to Round 3\n" % (best_player+1))
guessed_letters = {"r", "s", "t", "l", "n", "e"}
secret_word = choose_word()
while (secret_word in used_words ):
    secret_word = choose_word()
used_words.add(secret_word)
display_word_info()
for i in range(3):
    guessed_letters.add(guess_consonant())
guessed_letters.add(guess_vowel())
print("")
display_word_info()
guess = guess_word()
if ( guess == secret_word ):
    print("\n    Correct! You win the grand prize of $10000!\n")
else:
    print("\n    Sorry, the word was %s\n" % secret_word)
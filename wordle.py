import random
import json
import urllib.request
import regex as re

MAX_LIFE = 6
WORD_LENGTH = 5
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_END = '\033[0m'

# Download the database
DOWNLOAD_ROOT = r"https://raw.githubusercontent.com/kentnard/wordle-game/main/"
file_name = r"words_dictionary.json"
URL = DOWNLOAD_ROOT + file_name

data = urllib.request.urlopen(URL) #Get an object of type HTTPResponse
data_decode = data.read().decode('utf-8') #Convert it to String
data_dict = json.loads(data_decode) #Convert it to Dictionary

for key in data_dict.keys() :
    data_dict[key] = len(key)

dictionary_filtered = {k: v for k, v in data_dict.items() if len(k) == WORD_LENGTH}

word_list = list(dictionary_filtered.keys())

print("Welcome to Wordle! Can you guess the word?")
print(f"The word consists of {WORD_LENGTH} letters and you have only {MAX_LIFE} tries.")

class InvalidLengthException(Exception) :
    """
    Exception raised for input that doesn't have the length of five.

    Attributes :
        word -- input of the word that causes the error
        message -- explaination of the error
    """

    def __init__(self, word, message = "The length of the input is not valid. Please input a 5-letter word!" ) :
        self.word = word
        self.message = message
        super().__init__(self.message)

class InvalidWordException(Exception) :
    """
    Exception raised for word that doesn't exist in the dictionary.

    Attributes :
        word -- input of the word that causes the error
        message -- explaination of the error
    """

    def __init__(self, word, message = "Invalid word! Please input another word!" ) :
        self.word = word
        self.message = message
        super().__init__(self.message)

def notInDictionary(word, dictionary) :
    if word not in dictionary :
        return True
    else :
        return False

def checkWord(guess, answer) :
    color_palette = []
    for i in range(WORD_LENGTH) :
        if guess[i] == answer[i] :
            color = COLOR_GREEN
        elif guess[i] in answer :
            color = COLOR_YELLOW
        else :
            color = COLOR_RED
        color_palette.append((guess[i], color))

    for i in range(WORD_LENGTH) :
        if color_palette[i][1] == COLOR_YELLOW :
            letter_answer_count = answer.count(guess[i])
            letter_green_count = color_palette.count((guess[i], COLOR_GREEN))
            letter_yellow_count_until_now = color_palette[:i].count((guess[i], COLOR_YELLOW))
            if letter_green_count + letter_yellow_count_until_now + 1 > letter_answer_count :
                color_palette[i] = (guess[i], COLOR_RED)
    return [x[1] for x in color_palette]

def change_color_one_letter(letter, color, string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') :
    string_split = string.split(letter.upper())
    result = string_split[0] + color + letter + COLOR_END + string_split[1]
    return result

def change_color_all(guess, color_list, string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') :
    letter_list = [letter.upper() for letter in guess] #List of all letter

    string_progress = string
    for i in range(len(letter_list)) :
        # First, check if the color of the letter has been changed or not
        # The hierarchy is : GREEN > YELLOW > RED
        string_progress_split = string_progress.split(letter_list[i])
        if color_list[i] == COLOR_RED : 
            if string_progress_split[0].endswith(COLOR_GREEN) :
                string_progress_split[0] = string_progress_split[0].replace(COLOR_RED, '')
                color_choice = COLOR_GREEN
            elif string_progress_split[0].endswith(COLOR_YELLOW) :
                string_progress_split[0] = string_progress_split[0].replace(COLOR_RED, '')
                color_choice = COLOR_YELLOW
            else :
                color_choice = COLOR_RED
                
        elif color_list[i] == COLOR_YELLOW :
            if string_progress_split[0].endswith(COLOR_GREEN) :
                string_progress_split[0] = string_progress_split[0].replace(COLOR_YELLOW, '')
                color_choice = COLOR_GREEN
            else : 
                color_choice = COLOR_YELLOW
        else :
            color_choice = COLOR_GREEN
            
        string_progress = change_color_one_letter(letter_list[i], color_choice, string_progress)
    return string_progress

def change_color_answer(guess, color_list) :
    string_progress = ""
    for i in range(WORD_LENGTH) :
        string_progress += color_list[i] + guess[i]
    string_progress += COLOR_END
    return string_progress     
    
#Game starts here
life = MAX_LIFE
is_winning = False
attempt = 1
random_number = random.randint(0, len(word_list))
answer = word_list[random_number]
letters_available = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

while life > 0 and is_winning == False :
    try :
        #First, check if the length of the word is correct
        # Display the available words
        print(letters_available)
        
        #Ask user to input their guess
        guess = input(f'Guess the word #{attempt} : ')
        guess = guess.lower()
        
        if len(guess) != WORD_LENGTH :
            raise InvalidLengthException()
    except :
        print(InvalidLengthException(guess))    
    else :
            try :
                #Second, check if the word even exists
                if notInDictionary(guess, word_list) :
                    raise InvalidWordException()
            except :
                print(InvalidWordException(guess))
            else :
                #If the word passes those tests, then we check if it's the same word or not.
                result_color = checkWord(guess, answer)
                letters_available = change_color_all(guess, result_color, letters_available)
                print(change_color_answer(guess, result_color))
                attempt += 1
                if result_color.count(COLOR_GREEN) == 5 :
                    is_winning = True
                else :
                    life -= 1

if is_winning == True :
    print(f'Congratulations, you won! The word was : {answer}') 
else :
    print(f"You didn't guess the word correctly!\nThe answer is : {answer}")
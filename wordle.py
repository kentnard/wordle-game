import random
import json
import urllib.request

MAX_LIFE = 6
WORD_LENGTH = 5

# Download the database
DOWNLOAD_ROOT = r"https://raw.githubusercontent.com/kentnard/wordle-game/main/"
file_name = r"words_dictionary.json"
print(f"Downloading {file_name}")
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
            color = 'green'
        elif guess[i] in answer :
            color = 'yellow'
        else :
            color = 'red'
        color_palette.append((guess[i], color))

    for i in range(WORD_LENGTH) :
        if color_palette[i][1] == 'yellow' :
            letter_answer_count = answer.count(guess[i])
            #letter_guess_count = guess.count(guess[i])
            letter_green_count = color_palette.count((guess[i], 'green'))
            letter_yellow_count_until_now = color_palette[:i].count((guess[i], 'yellow'))
            if letter_green_count + letter_yellow_count_until_now + 1 > letter_answer_count :
                color_palette[i] = (guess[i], 'red')
    return [x[1] for x in color_palette]

#Game starts here
life = MAX_LIFE
is_winning = False
attempt = 1
random_number = random.randint(0, len(word_list))
answer = word_list[random_number]

while life > 0 and is_winning == False :
    try :
        #First, check if the length of the word is correct
        guess = input(f'Guess the word #{attempt} : ')
        guess = guess.lower()
        if len(guess) != WORD_LENGTH :
            raise InvalidLengthException()
        else :
            try :
                #Second, check if the word even exists
                if notInDictionary(guess, word_list) :
                    raise InvalidWordException()
            except :
                print(InvalidWordException(guess))
            else :
                #If the word passes those tests, then we check if it's the same word or not.
                result = checkWord(guess, answer)
                attempt += 1
                print(result)
                if result.count('green') == 5 :
                    is_winning = True
                else :
                    life -= 1
    except :
        print(InvalidLengthException(guess))

if is_winning == True :
    print(f'Congratulations, you won! The word was : {answer}') 
else :
    print(f"You didn't guess the word correctly!\nThe answer is : {answer}")




import os
import time
import glob
import random
import pandas as pd
import PySimpleGUI as sg

from layouts import *
from constants import *


def excel_to_dict(path: str) -> dict:
    """ This method gets excel path and return dictionary

        :arg:
            path(str) - directory where excel file/files are saved

        :return:
             words_dict(Dict) - dictionary where we keep all words and when X word displays, we delete it from the dict
    """

    excel_file = pd.read_excel(path, header=None, index_col=False)
    words = list(excel_file.iloc[:, 0])
    translations = list(excel_file.iloc[:, 1])
    words_dict = dict(zip(words, translations))

    return words_dict


def get_words(path_of_excels: str) -> dict:
    """ This method is to read words from excel and save them as python dictionary

        :arg:
            path_of_excels(str) - directory where excel file/files are saved

        :return:
             words(Dict) - dictionary where we keep all words and when X word displays, we delete it from the dict
    """

    excel_files = glob.glob(os.path.join(path_of_excels, "*.xlsx"))
    words = {}
    for f in excel_files:
        words.update(excel_to_dict(f))

    return words


def get_random_word(words: dict) -> (str, str):
    """ This method is used to choose new word randomly

        :arg:
            words(Dict) - dictionary where we keep all words and when X word displays, we delete it from the dict

        :return:
             random_key, random_value - new pair of word and its value
    """

    random_key, random_value = random.choice(list(words.items()))

    return random_key, random_value


def display_new_word(words_dict: dict, window: sg) -> (str, str):
    """ This method is used to display new word that is chosen randomly

        :arg:
            words_dict(Dict) - dictionary where we keep all words and when X word displays, we delete it from the dict
            window(sg) - PySimpleGUI window

        :return:
             random_key, random_value - new pair of word and its value
    """

    random_key, random_value = get_random_word(words_dict)
    window["-OUT-"].update(random_key)
    window["-TRANS-"].update("")
    words_left = len(words_dict) - 1
    window["-NUMWORDS-"].update(f"Words Left: {words_left}")

    return random_key, random_value


def update_window(scores: int, words_dict: dict, window: sg) -> (str, str):
    """ This method is used for updating score on the window and display new word that is chosen randomly

        :arg:
            scores(int) - the word that should be displayed on the page when its opened
            words_dict(Dict) - dictionary where we keep all words and when X word displays, we delete it from the dict
            window(sg) - PySimpleGUI window

        :return:
             random_key, random_value - new pair of word and its value
    """

    window["-SCORE-"].update(str(scores))
    random_key, random_value = display_new_word(words_dict, window)

    return random_key, random_value


def get_gif(percentile: int) -> str:
    """ This method returns a gif based on percentile

        :arg:
            percentile(int) - final result of user

        :return:
             (str) - gif
    """

    if percentile > PERCENTILE_SUPER:
        return GIFS[0]

    elif percentile > PERCENTILE_GOOD:
        return GIFS[1]

    elif percentile > PERCENTILE_NEUTRAL:
        return GIFS[2]

    else:
        return GIFS[3]


def display_result(num_words: int, score: int, full_time: int):
    """ Here is the logic for the final page

        :arg:
            num_words(int) - number of words in total
            score(int) - number of correctly guessed words
            full_time(int) - time that user spent for this session

        :return:
             None
    """

    # Calculations for getting score
    percentile = score / num_words

    gif = get_gif(percentile)

    final_score = f"Your score is: {score} / {num_words}"

    layout = final_page_layout(final_score, full_time, gif)
    window = sg.Window("GRE", layout, size=(WIN_WIDTH, WIN_HEIGHT), finalize=True)

    # Display final result and animation
    while True:
        event, values = window.read(timeout=100)
        window.Element('-IMAGE-').UpdateAnimation(gif, time_between_frames=50)
        if event == sg.WIN_CLOSED:
            break

    window.close()


def display_words(words_dict: dict, random_key: str, random_value: str, window: sg, scores: int) -> int:
    """ Here is the logic for the whole process (what should happen for each click on any button)

        :arg:
            words_dict(Dict) - dictionary where we keep all words and when X word displays, we delete it from the dict
            random_key(str) - randomly chosen word (that is key for dictionary)
            random_value(str) - value of randomly chosen word
            window(sg) - PySimpleGUI window
            scores(int) - number of correctly guessed words

        :return:
             scores(int) - number of correctly guessed words
    """

    while True:

        if len(words_dict) == 0:
            break

        event, values = window.read()
        window["-OUT-"].update(random_key)

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == "Next":
            random_key, random_value = display_new_word(words_dict, window)

        if event == "Translation":
            window["-TRANS-"].update(random_value)

        if event == "Guessed":
            scores += 1
            random_key, random_value = update_window(scores, words_dict, window)

        words_dict.pop(random_key, random_value)

    window.close()

    return scores


def first_page() -> str:
    """ This is the very first page when user chooses which option does he/she want to practice

        :arg:
            None

        :return:
             result(str) - ALL_WORDS or UNKNOWN
    """

    result = ""
    layout = first_page_layout()
    window = sg.Window("GRE", layout, size=(WIN_WIDTH, WIN_HEIGHT), finalize=True)
    while True:
        event, values = window.read(timeout=100)
        if event == "ALL_WORDS":
            result = "ALL_WORDS"
            break
        elif event == "UNKNOWN":
            result = "UNKNOWN"
            break
    window.close()

    return result


def main():
    start_time = time.time()

    result = first_page()

    path = ""
    if result == "ALL_WORDS":
        path = PATH_TO_ALL_EXCELS
    else:
        path = PATH_TO_UNKNOWN

    words_dict = get_words(path)
    num_words = len(words_dict)
    first_random_key, first_random_value = get_random_word(words_dict)

    scores = 0

    layout = get_main_layout(first_random_key)
    window = sg.Window("GRE", layout, size=(WIN_WIDTH, WIN_HEIGHT))

    scores = display_words(words_dict, first_random_key, first_random_value, window, scores)

    end_time = time.time()
    full_time = end_time - start_time

    display_result(num_words, scores, full_time)


if __name__ == "__main__":
    main()

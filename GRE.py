import pandas as pd
import os 
import glob 
import random 
import PySimpleGUI as sg
import time
from PIL import Image

WIN_HEIGHT = 600
WIN_WIDTH = 1100
path_to_all_excels = r"C:\Users\admin\Desktop\Rango\Projects\Study_Vocab_App\all_words"
path_to_unknown = r"C:\Users\admin\Desktop\Rango\Projects\Study_Vocab_App\unknown_words"
PERCENRILE_SUPER = 0.95
PERCENRILE_GOOD = 0.85
PERCENRILE_NEUTRAL = 0.7

def get_gifs() -> list:
    gif1 = r'super_happy.gif'
    gif2 = r'happy.gif'
    gif3 = r'neutral.gif'
    gif4 = r'bad.gif'
    return [gif1, gif2, gif3, gif4]

def excel_to_dict(path: str) -> dict:
    excel_file = pd.read_excel(path, header = None, index_col = False)
    words = list(excel_file. iloc[:, 0])
    translations = list(excel_file.iloc[:, 1])
    words_dict = dict(zip(words, translations))
    return words_dict

def get_words(path_of_excels: str) -> dict:
    excel_files = glob.glob(os.path.join(path_of_excels, "*.xlsx"))
    words = {}
    for f in excel_files:
        words.update(excel_to_dict(f))
    return words

def get_random_word(words:dict) -> (str, str):
    random_key, random_value = random.choice(list(words.items()))
    return random_key, random_value

def display_new_word(words_dict:dict, window:sg) -> (str, str):
    random_key, random_value = get_random_word(words_dict)
    window["-OUT-"].update(random_key)
    window["-TRANS-"].update("")
    words_left = len(words_dict)-1
    window["-NUMWORDS-"].update(f"Words Left: {words_left}")
    return random_key, random_value

def display_score(scores:int, words_dict:dict, window:sg) -> (str, str):
    window["-SCORE-"].update(str(scores))
    random_key, random_value = display_new_word(words_dict, window)
    return random_key, random_value

def get_main_layout(random_key:str) -> list:
    layout = [
        [sg.Text("")],
        [sg.Text(random_key, size = (30, 1), key = "-OUT-", font = ("Helvetica", 20)),
        sg.Text("Words Left: ", key = "-NUMWORDS-", font = ("Helvetica", 20))],
        [sg.Button("Translation", font = ("Helvetica", 15)),
        sg.Button("Next", font = ("Helvetica", 15)),
        sg.Button("Guessed", font = ("Helvetica", 15))],
        [sg.Text("Your score is: ", font = ("Helvetica", 15)),
        sg.Text("0", size = (3, 1), key = "-SCORE-", font = ("Helvetica", 15))],
        [sg.Text("Translation is: ", font = ("Helvetica", 15)),
        sg.Text("", size = (100, 1), key = "-TRANS-", font = ("Helvetica", 15))],
        [sg.VStretch()],
        [sg.Stretch(), sg.Exit(font = ("Helvetica", 15), pad = (0, 0))]
    ]
    return layout

def get_gif(percentile:int)->str:
    gif = ''
    gifs_list = get_gifs()
    if percentile > PERCENRILE_SUPER: gif = gifs_list[0]
    elif percentile > PERCENRILE_GOOD: gif = gifs_list[1]
    elif percentile > PERCENRILE_NEUTRAL : gif = gifs_list[2]
    else: gif = gifs_list[3]
    return gif

def display_result(num_words:int, score:int, full_time:int):
    percentile = score/num_words
    gif = get_gif(percentile)
    final_score = f"Your score is: {score} / {num_words}"
    layout = [
        [sg.Text("")],
        [sg.Text(final_score, font = ("Helvetica", 30))],
        [sg.Image(filename=gif,
              enable_events=True,
              key="-IMAGE-")],
        [sg.Text(f"Total time is: {int(full_time/60)} minutes", font = ("Helvetica", 30))]
    ]
    window = sg.Window("GRE", layout, size = (WIN_WIDTH, WIN_HEIGHT), finalize=True)
    while True:
        event, values = window.read(timeout=100)
        window.Element('-IMAGE-').UpdateAnimation(gif,  time_between_frames=50)
        if event == sg.WIN_CLOSED:
            break
    window.close()

def display_words(words_dict:dict, random_key:str, random_value:str, window:sg, scores:int) -> int:
    while True:
        if(len(words_dict) == 0):
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
            scores+=1
            random_key, random_value = display_score(scores, words_dict, window)
        words_dict.pop(random_key, random_value)
    window.close()
    return scores

def first_page_layout():
    layout = [
        [sg.Text("")],
        [sg.Text("")],
        [sg.Text("")],
        [sg.Text("")],
        [sg.Text("")],
        [sg.Text("")],
        [sg.Text("")],
        [sg.Text("")],
        [sg.Text("                                                                                     "), 
        sg.Button("ALL_WORDS", font = ("Helvetica", 15)), sg.Button("UNKNOWN", font = ("Helvetica", 15))]
    ]
    return layout

def first_page():
    result = ""
    layout = first_page_layout()
    window = sg.Window("GRE", layout, size = (WIN_WIDTH, WIN_HEIGHT), finalize=True)
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
    if(result == "ALL_WORDS"):
        path = path_to_all_excels
    else:
        path = path_to_unknown
    words_dict = get_words(path)
    num_words = len(words_dict)
    random_key, random_value = get_random_word(words_dict)
    scores = 0
    layout = get_main_layout(random_key)
    window = sg.Window("GRE", layout, size = (WIN_WIDTH, WIN_HEIGHT))
    scores = display_words(words_dict, random_key, random_value, window, scores)
    end_time = time.time()
    full_time = end_time-start_time
    display_result(num_words, scores, full_time)
    
if __name__ == "__main__":
    main()
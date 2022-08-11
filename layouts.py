import PySimpleGUI as sg


def get_main_layout(random_key: str) -> list:
    """ This method creates layout for the main page

        :arg:
            random_key(str) - the word that should be displayed on the page when its opened

        :return:
             layout(list)
    """

    layout = [
        [sg.Text("")],
        [sg.Text(random_key, size=(30, 1), key="-OUT-", font=("Helvetica", 20)),
         sg.Text("Words Left: ", key="-NUMWORDS-", font=("Helvetica", 20))],
        [sg.Button("Translation", font=("Helvetica", 15)),
         sg.Button("Next", font=("Helvetica", 15)),
         sg.Button("Guessed", font=("Helvetica", 15))],
        [sg.Text("Your score is: ", font=("Helvetica", 15)),
         sg.Text("0", size=(3, 1), key="-SCORE-", font=("Helvetica", 15))],
        [sg.Text("Translation is: ", font=("Helvetica", 15)),
         sg.Text("", size=(100, 1), key="-TRANS-", font=("Helvetica", 15))],
        [sg.VStretch()],
        [sg.Stretch(), sg.Exit(font=("Helvetica", 15), pad=(0, 0))]
    ]

    return layout


def first_page_layout() -> list:
    """ This method creates layout for the very first page

        :arg:
            None

        :return:
             layout(list)
    """

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
         sg.Button("ALL_WORDS", font=("Helvetica", 15)), sg.Button("UNKNOWN", font=("Helvetica", 15))]
    ]

    return layout


def final_page_layout(final_score: int, full_time: int, gif: str) -> list:
    """ This method creates layout that is used to display the final result(score and time)

        :arg:
            final_score(int) - number of correctly guessed words
            full_time(int) - time that user spent for this session
            gif(str) - gif

        :return:
             layout(list)
    """

    layout = [
        [sg.Text("")],
        [sg.Text(final_score, font=("Helvetica", 30))],
        [sg.Image(filename=gif,
                  enable_events=True,
                  key="-IMAGE-")],
        [sg.Text(f"Total time is: {int(full_time / 60)} minutes", font=("Helvetica", 30))]
    ]

    return layout

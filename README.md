# Study_Vocab_App

## Description:

This is a desktop application to study new vocabulary easily. There are two main directories where user can save his/her words with meanings:
all_words - you can save here excel worksheets(as much as you want) with all words and its meanings.
unknown - if user wants to practice only the words that he/she doesn't know, user can create seperate excel worksheets(as much as user wants) for such words and save this excel in this directory.
When user runs application, he/she chooses between all_words and unkown, then application chooses random words from excel and displays it on the screen. If user knows the meaning of word, user can click on 'Guessed' button and he/she gets one score for each guessed word. If user doesn't know the meaning of word, he/she clicks on button 'next' and doesn't deserve any point. There is also button 'Translation' - if user isn't sure that his/her guess is correct, he/she can press this button and application shows the meaning of that word(from excel worksheet). This button can be used for recheck if user guessed word or to see the translation if user didn't guess the word. Each word displays only once and user can see how many words are left on the right upper corner. After finishing all words, user can see his/her score, how much time did it take to go through all words and based on his/her score application displays some gif (angry, neutral, happy or super happy gif). I used **pandas** and **glob** libraries to work with excel file, **PySimpleGUI** for desktop app and **PIL** library to work with gifs. 

## How to install and run the project:

You need to install PySimpleGUI and then just run the main.py file (for windows command prompt: user should be in the directory where user saved main.py file and run 'python main.py' command).

## Visual:
![gre](https://user-images.githubusercontent.com/85623531/169103788-7cbdd508-f75f-4949-b7de-4217cc550020.PNG)

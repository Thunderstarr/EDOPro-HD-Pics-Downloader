# [EDOPro/Ygopro](https://discord.gg/ygopro-percy) hd cards downloader

This program automamize the process of acess [YGO Cards Databese](https://db.ygoprodeck.com/), choose of a card you want a better resolution pic, download the image and put it into your game's pics folder. The method is simple, a python script gets a list of cards ids in a ydk file and use link manipulation to download card per card directly into the pics folder. I pretend to expand this project to a deck containing all tcg/ocg cards and adjust the algorithim to download field's image too.

The size of a standart card pic is 177x254 that downloads automaticaly when you open the game, the pics you download with this program has the resolution of 421x614 or 139% larger and 142% taller. This upscale helps with runing your game in fullscreen.

### Instalation:
- Download exe (~5 MB) or py (1 kb) if you have python 3 installed in your computer;
- Extract to your EDOPro folder;
- Double-click exe or py file;
- Insert a valid deck name (without .ydk);
- If you are in deck edit screen, just get back to main menu to reload the pics;

### Download all cards pics (officials tgc/ocg):
- I recommend you delete all cards pics before you do what follow;
- Download allcards.ydk file;
- Drop it into your game's deck folder;
- Open the program and insert allcards;
- Wait until done. It can take a while because there are more than nine thousant cards.

:raised_hand: Warning: I ran this code a few times and **the program didn't download all the cards**. I don't know how to solve this problem yet, but work around is simple:
- Open the pics folder and scroll all way down to the last buggy pic;
- Go Rename and copy it's name (without .jpg);
- Go to your game's deck folder and open *allcards.ydk* with notepad;
- Hold *Ctrl* and press *h*;
- Paste the name you copied and click on Locate Next;
- Select the id above of that you located;
- Scroll all way up, hold *Shift* and select the id below *#main*;
- Press *Backspace*;
- Save.

This method removes all cards you already download from the list, remain less cards to download next time you execute the program.

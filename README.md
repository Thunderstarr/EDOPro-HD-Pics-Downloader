# [EDOPro/Ygopro](https://discord.gg/ygopro-percy) hd cards downloader

This program automamize the process of acess [YGO Cards Databese](https://db.ygoprodeck.com/), choose of a card you want a better resolution pic, download the image and put it into your game's pics folder. The method is simple, a python script gets a list of cards ids in a ydk file and use link manipulation to download card per card directly into the pics folder. I pretend to expand this project to a deck containing all tcg/ocg cards and adjust the algorithim to download field's image too.

![card comparison](imgs_repo/card_comparison.png)

The size of a standart card pic is 177x254 that downloads automaticaly when you open the game, the pics you download with this program has the resolution of 421x614 or 139% larger and 142% taller. This upscale helps with runing your game in fullscreen.

### Instalation:
- Download [exe](hd_cards_downloader.exe) (~5 MB) or [py](hd_cards_downloader.py) (1 kb) if you have python 3 installed in your computer;
- Extract to your EDOPro folder;
- Double-click exe or py file;
- Insert a valid deck name (without .ydk);
- If you are in deck edit screen, just get back to main menu to reload the pics;

### Commands!:
- */help* to see all commands;
- */allcards* to download all cards pics;
- */allfields* to download all fields artworks;
- */exit to exit*

### Download all cards pics (tgc/ocg):
- I recommend you delete all cards pics before you do what follow;
- Open the program and insert the command: */allcards*;
- Wait until done. It can take a while because it's over nine thousand cards.

### Download all fields artworks (tcg/ocg):
- I recommend you delete all fields artworks before you do what follow;
- Open the program and insert the command: */allfields*;

### You can help me:
With the release of new cards, two problems appear:
- The allcards.ydk don't cover all cards;
- The card's name can change from OCG to TCG (The game considers TCG name as default);

### Future features:
- Tokens also in HD. A large part is available in the database and a generic token will be downloaded if it is not there. The problem is storing a deck with a token, the game automatically deletes them, making it difficult to test.

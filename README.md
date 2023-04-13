# AUTODARTS-GIF

Autodarts-gif displays your favorite images accordingly to the state of a https://autodarts.io game. A running instance of https://github.com/lbormann/autodarts-caller is needed that sends the thrown points from https://autodarts.io to this application.

Tested on Windows 10 & 11 Pro x64, Python 3.9.7


## COMPATIBILITY

| Variant | Support |
| ------------- | ------------- |
| X01 | :heavy_check_mark: |
| Cricket | :heavy_check_mark: |
| Bermuda | |
| Shanghai | |
| Gotcha | |
| Around the Clock | |
| Round the World | |
| Random Checkout | :heavy_check_mark: |
| Count Up | |

## Showcase

#### Images:
<img src="https://github.com/lbormann/autodarts-gif/blob/main/showcase/1.jpg?raw=true">



## INSTALL INSTRUCTION

### Desktop-OS (cross-platform | Windows - Linux - MacOS)

- If you're running a desktop-driven OS (GUI) it's recommended to use autodarts-desktop: https://github.com/lbormann/autodarts-desktop


### Windows - Linux - MacOS

- Download the executable in the release section.


### By Source

#### Setup python3

- Download and install python 3.x.x for your specific os.
- Download and install pip.


#### Get the project

    git clone https://github.com/lbormann/autodarts-gif.git

Go to download-directory and type:

    pip install -r requirements.txt


## Setup Images

Put your image-files (gif, jpeg, jpg, png) in media-directory.


## RUN IT

### Prerequisite

* You need to have a running caller - https://github.com/lbormann/autodarts-caller - (latest version)



### Run by executable (Windows)

Create a shortcut of the executable; right click on the shortcut -> select properties -> add arguments in the target input at the end of the text field.

Example: C:\Downloads\autodarts-gif.exe -A1 "0-14" "bad score"

Save changes.
Click on the shortcut to start the application.


### Run by source

    python3 autodarts-gif.py -A1 "0-14" "bad score"



### Setup autostart [linux] (optional)

Read on autodarts-caller`s (adjust "autodarts-caller"-occurrences with autodarts-gif)

 
### Arguments

- -CON / --connection [OPTIONAL] [Default: "127.0.0.1:8079"] 
- -HFO / --high_finish_on [OPTIONAL] [Default: None] [Possible values: 2 .. 170] 
- -HF / --high_finish_images [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -G / --game_won_images [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -M / --match_won_images [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -B / --busted_images [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -S{0-180} / --score_{0-180}_images [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -A{1-12} / --score_area_{1-12}_images [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 



#### **-CON / --connection**

Host address to data-feeder (autodarts-caller). By Default this is '127.0.0.1:8079' (means your local ip-address / usually you do NOT need to change this)
    
#### **-HFO / --high_finish_on**

Define what a highfinish means for you. Choose a score-value between '2' and '170'. This value is relevant for argument '-HF'. By default this is not set = no images for 'Highfinishes'.

#### **-HF / --high_finish_images**

Displays an image when a high-finish occurs.
Define one image or a list of images. If you define a list, the program will randomly choose at runtime. For examples see below!

#### **-G / --game_won_images**

Displays an image when a game won occurs.
Define one image or a list of images. If you define a list, the program will randomly choose at runtime. For examples see below!

#### **-M / --match_won_images**

Displays an image when a match won occurs.
Define one image or a list of images. If you define a list, the program will randomly choose at runtime. For examples see below!

#### **-B / --busted_images**

Displays an image when a bust occurs.
Define one image or a list of images. If you define a list, the program will randomly choose at runtime. For examples see below!

#### **-S{0-180} / --score_{0-180}_images**

Displays an image when a specific score occurs. You can define every score-value between 0 and 180.
Define one image or a list of images. If you define a list, the program will randomly choose at runtime. For examples see below!

#### **-A{1-12} / --score_area_{1-12}_images**

Besides the definition of single score-values you can define up to 12 score-areas.
Define one image or a list of images. If you define a list, the program will randomly choose at runtime. For examples see below!


_ _ _ _ _ _ _ _ _ _


#### Examples: 


| Argument | [condition] | image 1 | image 2 | image 3 | ... |
| --  | -- | -- | --  | -- | -- | 
|-B |  | goofy | pluto | | | |
|-A1 | 0-15 | donald | party | fun | | |
|-A2 | 16-60 | woow | | | 

The first argument-definition shows the event 'Busted': Busting will result in displaying one of the 2 defined images: goofy or pluto.

The second argument-definition shows a 'score-area': recognized scores between 0 and 15 will result in displaying one of the 3 images: donal, party or fun. 

The third argument-definition shows a 'score-area': recognized scores between 16 and 60 result in displaying wow.

* To set a preset or playlists, use the displayed ID in gif! Moreover you can set a custom duration (Except -IDE)

    syntax: **"ps|{ID}|{seconds}"**

* If you have problems do not hesitate to have a look at example file!

    learn at: **start.bat**




## Community-Profiles (Coming soon - send me your profile :)

| Argument |
| --  |
| HF (Highfinish) | 
| IDE (Idle) | 
| G (Game-won) | 
| M (Match-won) | 
| B (Busted) | 
| S0 (score 0) | 
| S3 (Score 3) | 
| S26 (Score 26) | 
| S135 (Score 135) |
| S140 (Score 140) |
| S144 (Score 144) |
| S153 (Score 153) |
| S162 (Score 162) |
| S171 (Score 171) |
| S180 (Score 180) |
| A1 (Area 1) |
| A2 (Area 2) |
| A3 (Area 3) |
| A4 (Area 4) |
| A5 (Area 5) |
| A6 (Area 6) |
| A7 (Area 7) |
| A8 (Area 8) |
| A9 (Area 9) |
| A10 (Area 10) |
| A11 (Area 11) |
| A12 (Area 12) |



## !!! IMPORTANT !!!

This application requires a running instance of autodarts-caller https://github.com/lbormann/autodarts-caller


## BUGS

It may be buggy. I've just coded it for fast fun with https://autodarts.io. You can give me feedback in Discord > wusaaa


## TODOs

- care bot (json-events!)
- core display fails (on duration?)
- Remove duration (custom)
- add image-platforms (use them randomly -> avail if api-key is set)
- TODOs
- Improve README
- ip 0.0.0.0 should work!
- download every gif in media-directory


### Done

Add start stuff


## LAST WORDS

Make sure your gifs are interesting ;)
Thanks to Timo for awesome https://autodarts.io. It will be huge!


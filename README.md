# AUTODARTS-GIF
[![Downloads](https://img.shields.io/github/downloads/lbormann/autodarts-gif/total.svg)](https://github.com/lbormann/autodarts-gif/releases/latest)

Autodarts-gif displays images accordingly to the state of a https://autodarts.io game. A running instance of https://github.com/lbormann/autodarts-caller is needed that sends thrown points from https://autodarts.io to this application.

Tested on Windows 10 & 11 Pro x64, Python 3.9.7

<img src="https://github.com/lbormann/autodarts-gif/blob/main/showcase/sc.gif?raw=true">


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


## INSTALL INSTRUCTION

### Desktop-OS: Windows - Linux - MacOS

- If you're running a desktop-driven OS (GUI) it's recommended to use autodarts-desktop: https://github.com/lbormann/autodarts-desktop


### Headless-OS: Windows - Linux - MacOS

- Download the executable in the release section. On app-start, make sure you set -WEB to "1" (display images by webserver)


## Setup Images

If you want to display local images you must copy them to media-directory (-MP).
In case you prefer fetching random images out of the web you neither need to configure a media_path (-MP) nor you need to copy images.
Of course you can have a mixed configuration.

## RUN IT

### Prerequisite

* You need to have a running caller - https://github.com/lbormann/autodarts-caller - (latest version)



### Run by executable (Windows)

Create a shortcut of the executable; right click on the shortcut -> select properties -> add arguments in the target input at the end of the text field.

Example: C:\Downloads\autodarts-gif.exe -A1 "0-14" "bad score"

Save changes.
Click on the shortcut to start the application.

 
### Arguments

- -CON / --connection [OPTIONAL] [Default: "127.0.0.1:8079"] 
- -MP / --media_path [OPTIONAL] [Default: None]
- -HFO / --high_finish_on [OPTIONAL] [Default: None] [Possible values: 2 .. 170] 
- -HF / --high_finish_images [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -G / --game_won_images [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -M / --match_won_images [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -B / --busted_images [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -S{0-180} / --score_{0-180}_images [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -A{1-12} / --score_area_{1-12}_images [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -WEB / --web_gif [OPTIONAL] [Default: 0] [Possible values: 0|1|2] 


#### **-CON / --connection**

Host address to data-feeder (autodarts-caller). By Default this is '127.0.0.1:8079' (means your local ip-address / usually you do NOT need to change this)

#### **-MP / --media_path**

You can set an absolute path to your media-file-directory, Make sure your image-files are in a supported file-format (gif,png,jpg,jpeg). Moreover make sure the given path doesn't reside inside main-directory (autodarts-gif).
    
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

#### **-WEB / --web_gif**

If you set this to a '1' or '2' the app will host a web-endpoint to transfer every display-action to connected devices. A value '1' will display images only on connected devices. Value '2' will display images locally and on connected devices.

_ _ _ _ _ _ _ _ _ _


#### Examples: 


| Argument | [condition] | image 1 | image 2 | image 3 | ... |
| --  | -- | -- | --  | -- | -- | 
|-B | | busted | throw | | | |
|-A1 | 0-15 | bad | next | sad | | |
|-A2 | 16-60 | hi\\|3 | | | 

The first argument-definition shows the event 'Busted': Busting will result in display one of the 2 defined images: "busted" or "throw". Now the intern magic happens: If "busted" is a supported image-file, placed in media-directory (-MP) the app will use this file, otherwise it will use the term "busted" as a search-input to find a random image on the web. This mechanismn applies to every configured entry. In our example "throw" could be a local image-file or will be resolved to a random web-image.

The second argument-definition shows a 'score-area': recognized scores between 0 and 15 will result in display one of the 3 images: bad, next or sad. 

The third argument-definition shows a 'score-area': recognized scores between 16 and 60 result in display the image "hi" for a custom duration of 3 seconds. If you don't define a duration-key the application defaults to 0 which means unlimited duration til dart-pull appears.

If don't understand have a look at the example file **start.bat**




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

- improve README
- add more sites
- improve desktop gif-performance
- care bot (json-events!)
- make port(s) configurable

### Done

- add start stuff


## Resources

Icon by <a href="https://icon-icons.com/de/symbol/Foto-Fotografie-Bild/108525"></a> on <a href="https://icon-icons.com">icon-icons.com</a>
License <a href="https://creativecommons.org/licenses/by/4.0/">Attribution 4.0 International (CC BY 4.0)</a>                         
   


# DARTS-GIF
[![Downloads](https://img.shields.io/github/downloads/lbormann/darts-gif/total.svg)](https://github.com/lbormann/darts-gif/releases/latest)

Darts-gif displays images accordingly to the state of a https://autodarts.io game. A running instance of https://github.com/lbormann/darts-caller is needed that sends thrown points from https://autodarts.io to this application.


<img src="https://github.com/lbormann/darts-gif/blob/main/showcase/sc.gif?raw=true">


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
| Segment Training | |


## INSTALL INSTRUCTION

### Desktop-OS:

- If you're running a desktop-driven OS it's recommended to use [darts-hub](https://github.com/lbormann/darts-hub) as it takes care of starting, updating, configurating and managing multiple apps.


### Headless-OS:

- Download the appropriate executable in the release section.


### By Source:

#### Setup python3

- Download and install python 3.x.x for your specific os.
- Download and install pip.


#### Get the project

    git clone https://github.com/lbormann/darts-gif.git

Go to download-directory and type:

    pip3 install -r requirements.txt



## Setup Images

If you want to display local images you must copy them to media-directory (-MP).
In case you prefer fetching random images out of the web you neither need to configure a media_path (-MP) nor you need to copy images.
Of course you can have a mixed configuration.



## RUN IT

### Prerequisite

* You need to have a running caller - https://github.com/lbormann/darts-caller - (latest version)

### Run by executable

#### Example: Windows 

Create a shortcut of the executable; right click on the shortcut -> select properties -> add arguments in the target input at the end of the text field.

Example: C:\Downloads\darts-gif.exe -A1 "0-14" "bad score"

Save changes.
Click on the shortcut to start the application.


### Run by source

#### Example: Linux

    python3 darts-gif.py -A1 "0-14" "bad score"



 
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
- -WEBP / --web_caller_port [Default: 5001]
- -DEB / --debug [Default: 0] [Possible values: 0 | 1]


#### *`-CON / --connection`*

<p>Host address to data-feeder (darts-caller). By Default this is '127.0.0.1:8079' (means your local ip-address / usually you do NOT need to change this)</p>

#### *`-MP / --media_path`*

<p>You can set an absolute path to your media-file-directory, Make sure your image-files are in a supported file-format (gif,png,jpg,jpeg). Moreover make sure the given path doesn't reside inside main-directory (darts-gif).</p>
    
#### *`-HFO / --high_finish_on`*

<p>Define what a highfinish means for you. Choose a score-value between '2' and '170'. This value is relevant for argument '-HF'. By default this is not set = no images for 'Highfinishes'.</p>

#### *`-HF / --high_finish_images`*

<p>Displays an image when a high-finish occurs.
Define one image or a list of images. If you define a list, the program will randomly choose at runtime.</p> For examples see below!

#### *`-G / --game_won_images`*

<p>Displays an image when a game won occurs.
Define one image or a list of images. If you define a list, the program will randomly choose at runtime.</p> For examples see below!

#### *`-M / --match_won_images`*

<p>Displays an image when a match won occurs.
Define one image or a list of images. If you define a list, the program will randomly choose at runtime.</p> For examples see below!

#### *`-B / --busted_images`*

<p>Displays an image when a bust occurs.
Define one image or a list of images. If you define a list, the program will randomly choose at runtime.</p> For examples see below!

#### *`-S{0-180} / --score_{0-180}_images`*

<p>Displays an image when a specific score occurs. You can define every score-value between 0 and 180.
Define one image or a list of images. If you define a list, the program will randomly choose at runtime.</p> For examples see below!

#### *`-A{1-12} / --score_area_{1-12}_images`*

<p>Besides the definition of single score-values you can define up to 12 score-areas.
Define one image or a list of images. If you define a list, the program will randomly choose at runtime.</p> For examples see below!

#### *`-WEB / --web_gif`*

<p>If you set this to a '1' or '2' the app will host a web-endpoint to transfer every display-action to connected devices. A value '1' will display images only on connected devices. Value '2' will display images locally and on connected devices.</p>

#### *`-WEBP / --web_gif_port`*

<p>If web-gif is enabled, you can configure a custom port. By default this is '5001'.</p>

#### *`-DEB / --debug`*

<p>Set this to value '1', to output extended event-information on console. By default this is '0'.</p>



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

If you don't understand have a look at the example file **start.bat**




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

This application requires a running instance of darts-caller https://github.com/lbormann/darts-caller



## Resources

Icon by <a href="https://icon-icons.com/de/symbol/Foto-Fotografie-Bild/108525"></a> on <a href="https://icon-icons.com">icon-icons.com</a>
License <a href="https://creativecommons.org/licenses/by/4.0/">Attribution 4.0 International (CC BY 4.0)</a>                         
   


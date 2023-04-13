import os
from pathlib import Path
import platform
import random
import argparse
from urllib.parse import urlparse, quote, unquote
import requests
import websocket
from websocket_server import WebsocketServer
import threading
import logging
import time
import json
import ast
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 
from flask import Flask, render_template, send_from_directory
from bs4 import BeautifulSoup
# from PIL import Image, ImageSequence, ImageTk
# import tkinter as tk
from PIL import Image
import pygame
import queue



pygame.init()
screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)



sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
sh.setFormatter(formatter)
logger=logging.getLogger()
logger.handlers.clear()
logger.setLevel(logging.INFO)
logger.addHandler(sh)

app = Flask(__name__)
main_directory = os.path.dirname(os.path.realpath(__file__))



VERSION = '1.0.0'

BOGEY_NUMBERS = [169, 168, 166, 165, 163, 162, 159]
SUPPORTED_CRICKET_FIELDS = [15, 16, 17, 18, 19, 20, 25]
SUPPORTED_GAME_VARIANTS = ['X01', 'Cricket', 'Random Checkout']

IMAGE_PARAMETER_SEPARATOR = "|"
SUPPORTED_IMAGE_FORMATS = ['.gif', '.jpg', '.jpeg', '.png']
SITES = [
    'giphy.com',
    'tenor.com',
    # 'gfycat.com',
    # 'reddit.com',
    'imgur.com'
]





def ppi(message, info_object = None, prefix = '\r\n'):
    logger.info(prefix + str(message))
    if info_object != None:
        logger.info(str(info_object))
    
def ppe(message, error_object):
    ppi(message)
    if DEBUG:
        logger.exception("\r\n" + str(error_object))



def sanitize_tag(tag):
    tag = tag.replace(' ', '-')
    tag = quote(tag, safe="")
    # print(tag)
    return tag    
   
def get_random_image_url(tag):
    tag = sanitize_tag(tag)
    sites_tested = SITES.copy()

    image_url = None
    while(image_url is None and sites_tested != []):
        try:
            # Choose random website
            rand_site = random.choice(sites_tested)
            sites_tested.remove(rand_site)
            print(f"Fetching random image from '{rand_site}'")
            

            # Fetch random image by random website
            if rand_site == 'tenor.com':
                site_url = 'https://tenor.com/de/search/{tag}-gifs'.format(tag=tag)
                response = requests.get(site_url)
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                gif_divs = soup.find_all('div', {'class': 'Gif'})
                if gif_divs:
                    image_url_tag = random.choice(gif_divs).find('img')
                    image_url = image_url_tag.get('src') if image_url_tag else None

            elif rand_site == 'gfycat.com':
                site_url = 'https://gfycat.com/gifs/search/{tag}'.format(tag=tag)
                response = requests.get(site_url)
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                image_url_tags = soup.find_all('img', {'class': 'image'})
                if image_url_tags:
                    image_url = random.choice(image_url_tags).get('src')

            # elif rand_site == 'reddit.com':
            #     site_url = 'https://www.reddit.com/r/{tag}/random.json'.format(tag=tag)
            #     response = requests.get(site_url)
            #     html_content = response.text
            #     soup = BeautifulSoup(html_content, 'html.parser')
            #     json_data = response.json()
            #     image_url = json_data[0]['data']['children'][0]['data']['url']

            elif rand_site == 'imgur.com':
                site_url = 'https://api.imgur.com/1/gallery/t/{tag}'.format(tag=tag)
                headers = {'Authorization': 'Client-ID 5b7e6abdd8d0a95'}
                response = requests.get(site_url, headers=headers)
                data = response.json()
                if data['success']:
                    images = [item for item in data['data']['items'] if 'type' in item and item['type'] == 'image/gif']
                    if not images:
                        print('No GIFs found for the given tag.')
                    random_gif = random.choice(images)
                    print(f"Random GIF URL: {random_gif['link']}")
                else:
                    print(f"Error: {data['status']} - {data['data']}")

            elif rand_site == 'giphy.com':
                ak = 'sFze3uleyBhpM92Gzo4mVouEtcuI9DBt'
                site_url = 'https://api.giphy.com/v1/gifs/random?api_key={api_key}&tag={tag}'.format(tag=tag, api_key=ak)
                response = requests.get(site_url)
                if response.status_code == 200:
                    json_data = response.json()
                    image_url = json_data['data']['images']['original']['url']


        except Exception as e:
            print("error fetching image", str(e))
            continue
    return image_url

def get_state(event, images_list):
    choice = random.choice(images_list)

    tag = 'darts'
    if isinstance(choice, tuple) and choice[0]['file'].endswith(tuple(SUPPORTED_IMAGE_FORMATS)) == False:
        tag = choice[0]['file']
    else:
        return choice

    gif_url = get_random_image_url(tag)
    gif_filename = "autodarts_gif_giphy_random.gif"
    if gif_url is not None:
        response = requests.get(gif_url)
        with open(gif_filename, "wb") as f:
            f.write(response.content)
    return ({'file': gif_filename}, 0)
    
    
# root = tk.Tk()
# root.attributes('-fullscreen', True, '-topmost', True)
# root.configure(bg='black')
# def close_on_keypress(event):
#     root.withdraw()
# root.bind('<KeyPress>', close_on_keypress)

# def on_withdraw(event):
#     for child in event.widget.winfo_children():
#         child.destroy()

# root.withdraw()
# root.bind("<Unmap>", on_withdraw) # unmap event is triggered when the window is minimized/iconified
# root.protocol("WM_DELETE_WINDOW", lambda: None) # override the close button to do nothing






def create_image_path(filename, main_dir):
    for file_format in SUPPORTED_IMAGE_FORMATS:
        full_filename = os.path.join(main_dir, f"{filename}{file_format}")
        if os.path.exists(full_filename):
            return full_filename
    return filename

def parse_images_argument(images_argument, custom_duration_possible = True):
    if images_argument == None or images_argument == ["x"] or images_argument == ["X"]:
        return images_argument

    parsed_list = list()
    for image in images_argument:
        try:
            image_params = image.split(IMAGE_PARAMETER_SEPARATOR)
            path_to_file = image_params[0].strip().lower()
            custom_duration = 0
            if custom_duration_possible == True and len(image_params) == 2 and image_params[1].isdigit() == True:
                custom_duration = int(image_params[1])
                   
            state = {"file": create_image_path(path_to_file, MEDIA_PATH)}
            parsed_list.append((state, custom_duration))
        except Exception as e:
            ppe("Failed to parse event-configuration: ", e)
            continue
        
    if parsed_list == []:
        return images_argument
    
    return parsed_list   

def parse_score_area_images_argument(score_area_images_arguments):
    if score_area_images_arguments == None:
        return score_area_images_arguments

    area = score_area_images_arguments[0].strip().split('-')
    if len(area) == 2 and area[0].isdigit() and area[1].isdigit():
        return ((int(area[0]), int(area[1])), parse_images_argument(score_area_images_arguments[1:]))
    else:
        raise Exception(score_area_images_arguments[0] + ' is not a valid score-area')


def process_variant_x01(msg):
    if msg['event'] == 'darts-thrown':
        val = str(msg['game']['dartValue'])
        if SCORE_IMAGES[val] != None:
            schedule_image(image_queue, val, SCORE_IMAGES[val], 'Darts-thrown: ' + val)
        else:
            area_found = False
            ival = int(val)
            for SAE in SCORE_AREA_IMAGES:
                if SCORE_AREA_IMAGES[SAE] != None:
                    ((area_from, area_to), AREA_IMAGES) = SCORE_AREA_IMAGES[SAE]
                    
                    if ival >= area_from and ival <= area_to:
                        schedule_image(image_queue, str(ival), AREA_IMAGES, 'Darts-thrown: ' + val)
                        area_found = True
                        break
            if area_found == False:
                ppi('Darts-thrown: ' + val + ' - NOT configured!')

    elif msg['event'] == 'darts-pulled':
        if WEB == 1 or WEB == 2:
            mirror_clear = {
                    "event": "mirror-clear"
                }
            broadcast(mirror_clear)
        if WEB == 0 or WEB == 2:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT))

    elif msg['event'] == 'busted' and BUSTED_IMAGES != None:
        schedule_image(image_queue, 'busted', BUSTED_IMAGES, 'Busted!')

    elif msg['event'] == 'game-won' and GAME_WON_IMAGES != None:
        if HIGH_FINISH_ON != None and int(msg['game']['dartsThrownValue']) >= HIGH_FINISH_ON and HIGH_FINISH_IMAGES != None:
            schedule_image(image_queue, 'highfinish', HIGH_FINISH_IMAGES, 'Game-won - HIGHFINISH')
        else:
            schedule_image(image_queue, 'gameshot', GAME_WON_IMAGES, 'Game-won')

    elif msg['event'] == 'match-won' and MATCH_WON_IMAGES != None:
        if HIGH_FINISH_ON != None and int(msg['game']['dartsThrownValue']) >= HIGH_FINISH_ON and HIGH_FINISH_IMAGES != None:
            schedule_image(image_queue, 'highfinish', HIGH_FINISH_IMAGES, 'Match-won - HIGHFINISH')
        else:
            schedule_image(image_queue, 'matchshot', MATCH_WON_IMAGES, 'Match-won')

    elif msg['event'] == 'match-started':
        if WEB == 1 or WEB == 2:
            mirror_clear = {
                    "event": "mirror-clear"
                }
            broadcast(mirror_clear)
        if WEB == 0 or WEB == 2:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT))

    elif msg['event'] == 'game-started':
        if WEB == 1 or WEB == 2:
            mirror_clear = {
                    "event": "mirror-clear"
                }
            broadcast(mirror_clear)
        if WEB == 0 or WEB == 2:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT))
            





def connect_data_feeder():
    def process(*args):
        global WS_DATA_FEEDER
        websocket.enableTrace(False)
        data_feeder_host = CON
        if CON.startswith('ws://') == False:
            data_feeder_host = 'ws://' + CON
        WS_DATA_FEEDER = websocket.WebSocketApp(data_feeder_host,
                                on_open = on_open_data_feeder,
                                on_message = on_message_data_feeder,
                                on_error = on_error_data_feeder,
                                on_close = on_close_data_feeder)

        WS_DATA_FEEDER.run_forever()
    threading.Thread(target=process).start()

def on_open_data_feeder(ws):
    ppi('CONNECTED TO DATA-FEEDER ' + str(ws.url))
    
def on_message_data_feeder(ws, message):
    def process(*args):
        try:
            # ppi(message)
            msg = ast.literal_eval(message)

            if('game' in msg):
                mode = msg['game']['mode']
                if mode == 'X01' or mode == 'Cricket' or mode == 'Random Checkout':
                    process_variant_x01(msg)
                # elif mode == 'Cricket':
                #     process_match_cricket(msg)

        except Exception as e:
            ppe('WS-Message failed: ', e)

    threading.Thread(target=process).start()

def on_close_data_feeder(ws, close_status_code, close_msg):
    try:
        ppi("Websocket [" + str(ws.url) + "] closed! " + str(close_msg) + " - " + str(close_status_code))
        ppi("Retry : %s" % time.ctime())
        time.sleep(3)
        connect_data_feeder()
    except Exception as e:
        ppe('WS-Close failed: ', e)
    
def on_error_data_feeder(ws, error):
    ppe('WS-Error ' + str(ws.url) + ' failed: ', error)

    
def on_open_client(client, server):
    ppi('NEW CLIENT CONNECTED: ' + str(client))

def on_left_client(client, server):
    ppi('CLIENT DISCONNECTED: ' + str(client))

def broadcast(data):
    def process(*args):
        global server
        server.send_message_to_all(json.dumps(data, indent=2).encode('utf-8'))
    t = threading.Thread(target=process)
    t.start()
    t.join()
   



# def scale_and_center(image, screen_width, screen_height):
#     img_width, img_height = image.size
#     scale_ratio = min(screen_width / img_width, screen_height / img_height)
#     new_width = int(img_width * scale_ratio)
#     new_height = int(img_height * scale_ratio)
#     image = image.resize((new_width, new_height), Image.LANCZOS)
#     position = ((screen_width - new_width) // 2, (screen_height - new_height) // 2)
#     return image, position

# # TODO: duration + every key!
# def display_image(image, duration=0):
#     global label

#     if label:
#         label.destroy()

#     root.wm_deiconify()
#     label.config(image=None)

#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     image, (position_x, position_y) = scale_and_center(image, screen_width, screen_height)
#     image = ImageTk.PhotoImage(image)
#     label.place(x=position_x, y=position_y)
#     root.update()

# def display_animated_image(img, duration=0):
#     root.wm_deiconify()

#     label = tk.Label(root, bd=0, highlightthickness=0, bg='black')
#     label.pack()
#     # label.config(image=None)

#     def update_image():
#         nonlocal current_frame
#         nonlocal elapsed_time

#         img = frames[current_frame]
#         photo = ImageTk.PhotoImage(img)
#         label.config(image=photo)
#         label.image = photo
#         label.place(x=positions[current_frame][0], y=positions[current_frame][1])

#         elapsed_time += frame_durations[current_frame]
#         current_frame = (current_frame + 1) % len(frames)

#         if duration == 0 or elapsed_time < duration * 1000:
#             root.after(frame_durations[current_frame], update_image)
#         else:
#             root.withdraw()
            
            

#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()

#     frames = []
#     frame_durations = []
#     positions = []

#     for frame in ImageSequence.Iterator(img):
#         frame_durations.append(frame.info["duration"])
#         frame, position = scale_and_center(frame, screen_width, screen_height)
#         frames.append(frame)
#         positions.append(position)

#     current_frame = 0
#     elapsed_time = 0

#     update_image()

# def render_image(event_name, image_list, ptext, duration=5):
#     (state, duration) = get_state(event_name, image_list)
#     ppi(ptext + ' - IMAGE: ' + str(state))
#     file_path = state["file"]

#     if os.path.exists(file_path):
#         try:
#             img = Image.open(file_path)
#             if img.format == 'GIF':
#                 display_animated_image(img, duration)
#             elif img.format in ('PNG', 'JPEG', 'JPG'):
#                 display_image(img, duration)
#         except Exception as e:
#             print(f"Error displaying image: {e}")
#     else:
#         print(f"File not found: {file_path}")





def render_image(event_name, image_list, ptext, duration):
    try:
        (state, duration) = get_state(event_name, image_list)
        ppi(ptext + ' - IMAGE: ' + str(state))
        image_path = state["file"]

        if os.path.exists(image_path) == False:
            print(f"Image not found: {image_path}")
            return

        image = Image.open(image_path)
        screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

        if image.format.lower() == 'gif':
            is_gif = True
            frames = []
            try:
                while True:
                    frames.append(image.copy())
                    image.seek(len(frames))
            except EOFError:
                pass
        else:
            is_gif = False
            image = image.resize(screen_size, Image.ANTIALIAS)
            image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

        start_time = time.time()
        while not pygame.event.peek((pygame.KEYDOWN, pygame.USEREVENT)):
            if is_gif:
                for frame in frames:
                    resized_frame = frame.resize(screen_size, Image.ANTIALIAS)
                    frame_surface = pygame.image.fromstring(resized_frame.tobytes(), resized_frame.size, resized_frame.mode)
                    screen.blit(frame_surface, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(image.info['duration'])

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN or event.type == pygame.USEREVENT:
                            return

                    if duration > 0 and time.time() - start_time >= duration:
                        return
            else:
                screen.blit(image, (0, 0))
                pygame.display.flip()

                if duration > 0 and time.time() - start_time >= duration:
                    return

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.USEREVENT:
                    return

    except Exception as e:
        print(f"Error: {e}")

def display_images(image_queue):
    while True:
        event_name, image_list, ptext, duration = image_queue.get()
        if event_name is None:
            break
        render_image(event_name, image_list, ptext, duration)

def schedule_image(image_queue, event_name, image_list, ptext, duration=0):
    image_queue.put((event_name, image_list, ptext, duration))

# def close_image_after_delay(delay):
#     time.sleep(delay)
#     pygame.event.post(pygame.event.Event(pygame.USEREVENT))



# def render_image(event_name, image_list, ptext, duration=0):
#     try:
#         (state, duration) = get_state(event_name, image_list)
#         ppi(ptext + ' - IMAGE: ' + str(state))
#         image_path = state["file"]

#         if os.path.exists(image_path) == False:
#             print(f"Image not found: {image_path}")
#             return
           
#         image = Image.open(image_path)

#         screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

#         if image.format.lower() == 'gif':
#             is_gif = True
#             frames = []
#             try:
#                 while True:
#                     frames.append(image.copy())
#                     image.seek(len(frames))
#             except EOFError:
#                 pass
#         else:
#             is_gif = False
#             image = image.resize(screen_size, Image.ANTIALIAS)
#             image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

#         start_time = time.time()
#         while not pygame.event.peek((pygame.KEYDOWN, pygame.USEREVENT)):
#             if is_gif:
#                 for frame in frames:
#                     resized_frame = frame.resize(screen_size, Image.ANTIALIAS)
#                     frame_surface = pygame.image.fromstring(resized_frame.tobytes(), resized_frame.size, resized_frame.mode)
#                     screen.blit(frame_surface, (0, 0))
#                     pygame.display.flip()
#                     pygame.time.delay(image.info['duration'])

#                     for event in pygame.event.get():
#                         if event.type == pygame.KEYDOWN or event.type == pygame.USEREVENT:
#                             return

#                     if duration > 0 and time.time() - start_time >= duration:
#                         return
#             else:
#                 screen.blit(image, (0, 0))
#                 pygame.display.flip()

#                 if duration > 0 and time.time() - start_time >= duration:
#                     return

#             for event in pygame.event.get():
#                 if event.type == pygame.KEYDOWN or event.type == pygame.USEREVENT:
#                     return

#     except Exception as e:
#         print(f"Error displaying image: {e}")







@app.route('/')
def index():
    return render_template('index.html')

@app.route('/images/<path:file_id>', methods=['GET'])
def file(file_id):
    file_id = unquote(file_id)
    directory = os.path.dirname(file_id)
    file_name = os.path.basename(file_id)
    return send_from_directory(directory, file_name)

def start_websocket_server(host, port):
    global server
    server = WebsocketServer(host=host, port=port, loglevel=logging.ERROR)
    server.set_fn_new_client(on_open_client)
    server.set_fn_client_left(on_left_client)
    server.run_forever()

def start_flask_app(host, port):
    app.run(host=host, port=port, debug=False)




if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-MP", "--media_path", required=True, help="Absolute path to your media folder. You can download free images at https://giphy.com/")
    ap.add_argument("-CON", "--connection", default="127.0.0.1:8079", required=False, help="Connection to data feeder")
    ap.add_argument("-HFO", "--high_finish_on", type=int, choices=range(1, 171), default=None, required=False, help="Individual score for highfinish")
    ap.add_argument("-HF", "--high_finish_images", default=None, required=False, nargs='*', help="image-definition when high-finish occurs")
    ap.add_argument("-G", "--game_won_images", default=None, required=False, nargs='*', help="image-definition when game won occurs")
    ap.add_argument("-M", "--match_won_images", default=None, required=False, nargs='*', help="image-definition when match won occurs")
    ap.add_argument("-B", "--busted_images", default=None, required=False, nargs='*', help="image-definition when bust occurs")
    for v in range(0, 181):
        val = str(v)
        ap.add_argument("-S" + val, "--score_" + val + "_images", default=None, required=False, nargs='*', help="WLED image-definition for score " + val)
    for a in range(1, 13):
        area = str(a)
        ap.add_argument("-A" + area, "--score_area_" + area + "_images", default=None, required=False, nargs='*', help="WLED image-definition for score-area")
    ap.add_argument("-WEB", "--web_gif", required=False, type=int, choices=range(0, 3), default=0, help="If '1' the application will host an web-endpoint, '2' it will do '1' and default gif-functionality.")
    ap.add_argument("-DEB", "--debug", type=int, choices=range(0, 2), default=False, required=False, help="If '1', the application will output additional information")

    args = vars(ap.parse_args())

    MEDIA_PATH = Path(args['media_path'])
    CON = args['connection']
    HIGH_FINISH_ON = args['high_finish_on']
    WEB = args['web_gif']
    DEBUG = args['debug']

    GAME_WON_IMAGES = parse_images_argument(args['game_won_images'])
    MATCH_WON_IMAGES = parse_images_argument(args['match_won_images'])
    BUSTED_IMAGES = parse_images_argument(args['busted_images'])
    HIGH_FINISH_IMAGES = parse_images_argument(args['high_finish_images'])
    
    SCORE_IMAGES = dict()
    for v in range(0, 181):
        parsed_score = parse_images_argument(args["score_" + str(v) + "_images"])
        SCORE_IMAGES[str(v)] = parsed_score
        # ppi(parsed_score)
    SCORE_AREA_IMAGES = dict()
    for a in range(1, 13):
        parsed_score_area = parse_score_area_images_argument(args["score_area_" + str(a) + "_images"])
        SCORE_AREA_IMAGES[a] = parsed_score_area
        # ppi(parsed_score_area)

    args_post_check = None
    try:
        if os.path.commonpath([MEDIA_PATH, main_directory]) == main_directory:
            args_post_check = 'MEDIA_PATH resides inside MAIN-DIRECTORY! It is not allowed!'
    except:
        pass
    
   
    global WS_DATA_FEEDER
    WS_DATA_FEEDER = None

    if DEBUG:
        ppi('Started with following arguments:')
        ppi(json.dumps(args, indent=4))

    osType = platform.system()
    osName = os.name
    osRelease = platform.release()
    ppi('\r\n', None, '')
    ppi('##########################################', None, '')
    ppi('       WELCOME TO AUTODARTS-GIF', None, '')
    ppi('##########################################', None, '')
    ppi('VERSION: ' + VERSION, None, '')
    ppi('RUNNING OS: ' + osType + ' | ' + osName + ' | ' + osRelease, None, '')
    ppi('SUPPORTED GAME-VARIANTS: ' + " ".join(str(x) for x in SUPPORTED_GAME_VARIANTS), None, '')
    ppi('\r\n', None, '')

    if args_post_check == None: 
        try:
            connect_data_feeder()

            if WEB > 0:
                websocket_server_thread = threading.Thread(target=start_websocket_server, args=('192.168.3.19', 8039))
                websocket_server_thread.start()
                flask_app_thread = threading.Thread(target=start_flask_app, args=('192.168.3.19', '5001'))
                flask_app_thread.start()

                # root.mainloop()
                image_queue = queue.Queue()

                # Starte den Hauptanzeigethread
                display_thread = threading.Thread(target=display_images, args=(image_queue,))
                display_thread.start()


                # Beende den Hauptanzeigethread
                # image_queue.put((None, 0))
                display_thread.join()

                websocket_server_thread.join()
                flask_app_thread.join() 
                # root.destroy()
            # else:
            #     root.mainloop()
            #     root.destroy()

        except Exception as e:
            ppe("Connect failed: ", e)
    else:
        ppi('Please check your arguments: ' + args_post_check)


time.sleep(30)
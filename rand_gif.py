import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import quote


sites = [
    'giphy.com',
    'tenor.com',
    'gfycat.com',
    # 'reddit.com',
    'imgur.com'
]


tag = 'darts 180'



def sanitize_tag(tag):
    tag = tag.replace(' ', '-')
    tag = quote(tag, safe="")
    # print(tag)
    return tag


tag = sanitize_tag(tag)
sites_tested = sites.copy()


gif_url = None
while(gif_url is None and sites_tested != []):
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
                gif_url_tag = random.choice(gif_divs).find('img')
                gif_url = gif_url_tag.get('src') if gif_url_tag else None

        elif rand_site == 'gfycat.com':
            site_url = 'https://gfycat.com/gifs/search/{tag}'.format(tag=tag)
            response = requests.get(site_url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            gif_url_tags = soup.find_all('img', {'class': 'image'})
            if gif_url_tags:
                gif_url = random.choice(gif_url_tags).get('src')

        # elif rand_site == 'reddit.com':
        #     site_url = 'https://www.reddit.com/r/{tag}/random.json'.format(tag=tag)
        #     response = requests.get(site_url)
        #     html_content = response.text
        #     soup = BeautifulSoup(html_content, 'html.parser')
        #     json_data = response.json()
        #     gif_url = json_data[0]['data']['children'][0]['data']['url']

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
                gif_url = json_data['data']['images']['original']['url']


    except Exception as e:
        print("error fetching image", str(e))
        continue



if gif_url is not None:
    print(gif_url)
else:
    print(f"Failed to fetch random image")

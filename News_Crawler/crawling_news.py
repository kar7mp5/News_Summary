# crawling_news.py
import requests 
from bs4 import BeautifulSoup




def get_req():
    """Get request from GeekNews and parse the HTML to extract topic information.
    URL: https://news.hada.io/
    
    Returns:
        list: A list of dictionaries, each containing the title, points, and link of a topic.
    """
    url = "https://news.hada.io/"
    try:
        res = requests.get(url, auth=("user", "pass")) 
        res.raise_for_status() # check status code for response received 

    except requests.exceptions.HTTPError as err:
        print(err)

    # HTML parsing
    soup = BeautifulSoup(res.text, 'lxml')
 
    # extract all divs with class 'topic_row'
    topics = soup.find_all('div', class_='topic_row')

    # result
    data = []

    for topic in topics:
        title = topic.find('div', class_='topictitle').text.strip()
        points = topic.find('span', id=lambda x: x and x.startswith('tp')).text.strip()
        link = topic.find('a', rel='nofollow')['href']
        # add URL 'https://'
        if not link.startswith(('http://', 'https://')):
            link = 'https://news.hada.io/' + link

        data.append({
            'title': title,
            'points': points,
            'link': link,
        })

    return data




if __name__=="__main__":
    print(get_req())

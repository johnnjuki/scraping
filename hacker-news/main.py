import requests
from bs4 import BeautifulSoup
import pprint

base_url = "https://news.ycombinator.com/news"
second_page_url = base_url + "?p=2"

res = requests.get(base_url)
res2 = requests.get(second_page_url)

soup = BeautifulSoup(res.text, 'html.parser')  # The BeautifulSoup object
soup2 = BeautifulSoup(res2.text, "html.parser")

body = soup.body  # The body

contents = body.contents  # The entire content in list form

divs = soup.find_all('div')  # Find all the divs in the soup object

# links = soup.find_all('a')  # Find all the links on the page

title = soup.title  # The title tag of the soup object

first_link = soup.a  # The first link

links = soup.select('.titleline')
subtext = soup.select('.subtext')

links2 = soup2.select('.titleline')
subtext2 = soup2.select('.subtext')

mega_links = links + links2
mega_subtexts = subtext + subtext2


def create_custom_hn(links, subtext):
    hn = []
    for index, item in enumerate(links):
        text = item.text
        href = item.find('a').get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].text.replace(' points', ""))
            if points >= 100:
                hn.append({
                    "text": text,
                    "link": href,
                    "votes": points
                })
    return sort_stories_by_votes(hn)


def sort_stories_by_votes(hn_list):
    return sorted(hn_list, key=lambda key: key['votes'], reverse=True)


if __name__ == '__main__':
    pprint.pprint(create_custom_hn(mega_links, mega_subtexts))

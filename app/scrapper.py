from bs4 import BeautifulSoup as Soup
import requests

URL = 'https://www.reuters.com'
TIMEZONE = 'Europe/Copenhagen'

def pages(page: str) -> dict[any]:

    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "da,en-US;q=0.9,en;q=0.8,fi;q=0.7,nb;q=0.6,sv;q=0.5,fr;q=0.4,fa;q=0.3,de;q=0.2",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    }
    request = requests.get(f'{URL}/{page}', headers=HEADERS)
    # print('response code: ', request.status_code)
    # print('response code: ', request.text)
    html = Soup(request.content, 'html.parser')

    selector = "ul > li > a[data-testid='Body']"
    # button with attr data-testid = 'Body'
    buttons = html.select(selector)
    data = []

    for (index, button) in enumerate(buttons, 1):
        row = {'id': index, 'name': None, 'description': None, 'query': None}
        if button.has_attr('href'):
            (_, *category) = button['href'].strip('/').split('/')
            category = category[0] if category else ''
            row['name'] = category if category else page
            row['description'] = button.text
            row['query'] = f'?page={page}&category={category}'
            data.append(row)
    return {'total': len(data), 'page': page, 'items': data}

def feeds(page: str, category: str) -> dict[any]:
    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "da,en-US;q=0.9,en;q=0.8,fi;q=0.7,nb;q=0.6,sv;q=0.5,fr;q=0.4,fa;q=0.3,de;q=0.2",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    }
    request = requests.get(f'{URL}/{page}/{category}', headers=HEADERS)
    html = Soup(request.content, 'html.parser')

    data = []
    # get all li with data-testid="FeedListItem"
    cards = html.find_all('li', {'data-testid': 'FeedListItem'})
    for (index, card) in enumerate(cards):
        row = {
            'id': None, 'category': None, 'title': None,
            'link': None, 'image': None, 'datetime': None
        }
        # get image URL
        image = card.find('img')
        row['image'] = image['src'] if image else None
        title_heading = card.find('div', {'data-testid': 'Title'})
        if title_heading:
            row['title'] = title_heading.text
            a = title_heading.find('a', {'data-testid': 'TitleLink'})
            row['link'] = a['href'] if a else 'NO-Link-Found'
        label = card.find('span', {'data-testid': 'KickerLabel'})
        if label:
            row['category'] = label.text.replace('category', '')
        date_time = card.find('time', {'data-testid': 'DateLineText'})
        if date_time:
            row['datetime'] = date_time['datetime']
        data.append(row)
    return {
        'total': len(data), 'source': URL, 'page': page,
        'category': category, 'items': data
    }

from app.scrapers.base import BaseScraper


class ReutersScraper(BaseScraper):
    """Scraper for Reuters news site"""

    def __init__(self):
        super().__init__(base_url='https://www.reuters.com')

    def scrape_pages(self, page: str) -> dict:
        """
        Scrape available pages/categories from Reuters

        Args:
            page: The page identifier (e.g., 'world', 'business')

        Returns:
            Dictionary with total, page, and items list
        """
        html = self._fetch_html(f'{self.base_url}/{page}')

        selector = "ul > li > a[data-testid='Body']"
        buttons = html.select(selector)
        data = []

        for (index, button) in enumerate(buttons, 1):
            if button.has_attr('href'):
                (_, *category) = button['href'].strip('/').split('/')
                category = category[0] if category else ''
                name = category if category else page

                row = {
                    'id': self.generate_page_id(name, page),
                    'name': name,
                    'description': button.text,
                    'query': f'?page={page}&category={category}'
                }
                data.append(row)

        return {'total': len(data), 'page': page, 'items': data}

    def scrape_feeds(self, page: str, category: str, subcategory: str) -> dict:
        """
        Scrape news feeds from Reuters

        Args:
            page: The page identifier
            category: The category identifier
            subcategory: The SubCategory identifier

        Returns:
            Dictionary with total, source, page, category, and items list
        """
        html = self._fetch_html(f'{self.base_url}/{page}/{category}/{subcategory}')

        data = []
        # Get all li with data-testid="FeedListItem"
        cards = html.find_all('li', {'data-testid': 'FeedListItem'})

        for (index, card) in enumerate(cards, 1):
            # Get title and link first
            title_heading = card.find('div', {'data-testid': 'Title'})
            title = None
            link = None
            if title_heading:
                title = title_heading.text
                a = title_heading.find('a', {'data-testid': 'TitleLink'})
                link = a['href'] if a else 'NO-Link-Found'

            # Generate ID based on link
            article_id = self.generate_article_id(link, fallback_index=index)

            # Get image URL
            image = card.find('img')
            image_url = image['src'] if image else None

            # Get category label
            label = card.find('span', {'data-testid': 'KickerLabel'})
            cat_name = label.text.replace('category', '') if label else None

            # Get datetime
            date_time = card.find('time', {'data-testid': 'DateLineText'})
            datetime_str = date_time['datetime'] if date_time else None

            row = {
                'id': article_id,
                'category': cat_name,
                'title': title,
                'link': link,
                'image': image_url,
                'datetime': datetime_str
            }
            data.append(row)

        return {
            'total': len(data), 'source': self.base_url, 'page': page,
            'category': category, 'items': data
        }

from app.scrapers.base import BaseScraper


class BBCScraper(BaseScraper):
    """Scraper for BBC News site"""

    def __init__(self):
        super().__init__(base_url='https://www.bbc.com')

    def scrape_pages(self, page: str) -> dict:
        """
        Scrape available pages/categories from BBC News

        Args:
            page: The page identifier (e.g., 'home', 'news')

        Returns:
            Dictionary with total, page, and items list
        """
        html = self._fetch_html(f'{self.base_url}/{page}')

        nav_links = html.find_all('a', {'data-testid': 'subNavigationLink'})
        data = []

        for (index, link) in enumerate(nav_links, 1):
            if link.has_attr('href'):
                href = link['href']
                category = href.split('/')[-1] if '/' in href else href
                row = {
                    'id': self.generate_page_id(category, page),
                    'name': category,
                    'description': link.text.strip(),
                    'query': f'?page={page}&category={category}'
                }
                data.append(row)

        return {'total': len(data), 'page': page, 'items': data}

    def scrape_feeds(self, page: str, category: str, subcategory: str) -> dict:
        """
        Scrape news feeds from BBC News

        Args:
            page: The page identifier
            category: The category identifier
            subcategory: The SubCategory identifier

        Returns:
            Dictionary with total, source, page, category, and items list
        """
        html = self._fetch_html(f'{self.base_url}/{page}/{category}/{subcategory}')

        data = []
        # BBC uses different HTML structure - this is a basic example
        # You'll need to inspect BBC's HTML for accurate selectors
        articles = html.select("[data-testid='liverpool-card']")

        for (index, article) in enumerate(articles, 1):
            # Get title and link
            title = None
            link = None
            title_elem = article.select_one('h2')
            if title_elem:
                title = title_elem.text.strip()
                link_elem = article.select_one('a')
                if link_elem and link_elem.has_attr('href'):
                    href = link_elem['href']
                    # BBC sometimes uses relative URLs
                    link = href if href.startswith('http') else f'https://www.bbc.com{href}'

            # Generate ID based on link
            article_id = self.generate_article_id(link, fallback_index=index)

            # Get image
            img = article.select_one('div[data-testid="card-media"] img')
            image_url = img['src'] if img and img.has_attr('src') else None

            # Get datetime if available
            time_elem = article.select_one('span[data-testid="card-metadata-lastupdated"]')
            datetime_str = time_elem.text if time_elem else None

            row = {
                'id': article_id,
                'category': category,
                'subcategory': subcategory,
                'title': title,
                'link': link,
                'image': image_url,
                'datetime': datetime_str
            }
            data.append(row)

        return {
            'total': len(data),
            'source': self.base_url,
            'page': page,
            'category': category,
            'subcategory': subcategory,
            'items': data
        }

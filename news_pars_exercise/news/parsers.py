import json
from datetime import timezone, datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from news_pars_exercise.news.models import New, Tag


class ParsingCore:
    source = 'example'
    url = None
    news_count = 10

    def create_news(self, title: str, description: str, publish_at: str, tags: list) -> New:
        """Create new by params."""
        tags_objects = []
        title = title
        description = description
        publish_at = publish_at
        new, created = New.objects.get_or_create(source=self.source, title=title, defaults=dict(
            description=description,
            publish_at=datetime.strptime(publish_at, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        ))
        for tag in tags:
            tags_objects.append(Tag(name=tag))
        Tag.objects.bulk_create(tags_objects, ignore_conflicts=True)
        new.tags.add(*Tag.objects.filter(name__in=tags))
        return new

    def get_news(self) -> list:
        """Extract news from url."""
        pass

    def parse_news(self) -> None:
        """Create save or update news"""
        pass


class YandexParsing(ParsingCore):
    source = 'y'
    main_url = 'https://market.yandex.ru'
    url = 'https://market.yandex.ru/partners/api/news-more/news'

    def get_news(self) -> list:
        """Extract news from url."""
        news_array = requests.get(self.url).json()
        while len(news_array) < self.news_count:
            next_url = '{}{}'.format(self.main_url, news_array[-1]['nextUrl'])
            next_page = requests.get(next_url).json()
            news_array += next_page
        return news_array[:self.news_count]

    def parse_news(self) -> None:
        """Create save or update news"""
        news_array = self.get_news()
        for new_array in news_array:
            tags = [t['displayName'] for t in new_array.get('tags')]
            self.create_news(new_array['approvedTitle'], new_array['approvedPreview']['html'], new_array['publishDate'],
                             tags)


class OzonParsing(ParsingCore):
    source = 'o'
    url = 'https://seller.ozon.ru/content-api/news/'
    # ?_limit = 8 & _start = 8

    def __init__(self):
        options = Options()
        self.headless = webdriver.Chrome('././chromedriver', options=options)
        super().__init__()

    def get_news(self) -> list:
        """Extract news from url."""
        self.headless.get('{}?_limit={}'.format(self.url, str(self.news_count)))
        news_array = json.loads(self.headless.find_element(By.TAG_NAME, 'pre').text)
        return news_array

    def parse_news(self) -> None:
        """Create save or update news"""
        news_array = self.get_news()
        for new_array in news_array:
            if New.objects.filter(title=new_array['title']).exists():
                continue
            self.headless.get('{}{}'.format(self.url, new_array.get('slug')))
            new_detail_array = json.loads(self.headless.find_element(By.TAG_NAME, 'pre').text)
            tags = [t['name'] for t in new_array['theme']]
            self.create_news(new_array['title'], new_detail_array['htmlContent'], new_detail_array['published_at'],
                             tags)

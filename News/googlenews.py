import feedparser
import urllib
import requests
from dateparser import parse as parse_date

class GoogleNews:
    def __init__(self, lang='pt', country='PT'):
        self.lang = lang.lower()
        self.country = country.upper()
        self.BASE_URL = 'https://news.google.com/rss'

    def __ceid(self):
        """Compile correct country-lang parameters for Google News RSS URL"""
        return f'?ceid={self.country}:{self.lang}&hl={self.lang}&gl={self.country}'

    def __parse_feed(self, feed_url):
        try:
            response = requests.get(feed_url)
            response.raise_for_status()  # Checks for HTTP errors
            return feedparser.parse(response.text)
        except requests.exceptions.RequestException as e:
            print(f'Error fetching the feed: {e}')
            return None

    def __search_helper(self, query):
        return urllib.parse.quote_plus(query)

    def __from_to_helper(self, validate=None):
        try:
            return parse_date(validate).strftime('%Y-%m-%d')
        except Exception as e:
            print(f'Could not parse your date: {e}')
            return None

    def top_news(self):
        """Return a list of all articles from the main page of Google News"""
        feed_url = self.BASE_URL + self.__ceid()
        return self.__parse_feed(feed_url)

    def search(self, query: str, when=None, from_=None, to_=None):
        """Return a list of all articles given a full-text search parameter"""
        query_params = [f'q={self.__search_helper(query)}']
        if when:
            query_params.append(f'when:{when}')
        if from_:
            query_params.append(f'after:{self.__from_to_helper(from_)}')
        if to_:
            query_params.append(f'before:{self.__from_to_helper(to_)}')
        
        search_ceid = self.__ceid().replace('?', '&')
        feed_url = self.BASE_URL + '/search?' + '&'.join(query_params) + search_ceid
        return self.__parse_feed(feed_url)

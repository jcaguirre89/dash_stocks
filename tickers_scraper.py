"""
Scrapes list of tickers in S&P 500 from wikipedia


"""

from urllib import request
import bs4

def get_tickers():
    """
    Scrape wikipedia for tickers and names
    :return: dictionary
    """
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    with request.urlopen(url) as response:
        html = response.read()
    soup = bs4.BeautifulSoup(html, 'lxml')
    table = soup.find('table', attrs={'class': 'wikitable'})

    companies = {}
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if cols:
            ticker = cols[0].text.strip().lower()
            name = cols[1].text.strip()
            companies[ticker] = name
    return companies




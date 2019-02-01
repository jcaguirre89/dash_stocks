import requests
import time
import json


def get_nyt_news(params, pages=1, outfile=None):
    if pages > 100:
        raise ValueError('pages max is 100')
    nyt_data = []
    # Restrict result to certain fields
    params.update({'fl': 'snippet, headline, keywords'})
    for i in range(pages):
        page = str(i)
        params.update({'page': page})
        url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json"

        response = requests.get(url, params=params)
        out = response.json()

        nyt_data += out['response']['docs']
        time.sleep(1)

    if outfile:
        with open(outfile, 'w') as f:
            json.dumps(nyt_data, f)

    return nyt_data

def get_cnbc_news(params, outfile=None):
    """
    get articles from cnbc an related
    :param params: dictionary of parameters, must include at least apiKey and q.
    e.g: params = {'q': query, 'from': start_date, 'sortBy': 'popularity',
          'language': 'en', 'apiKey': cnbc_key}
    :param outfile: if given, save result to json file. must be a string like 'results.json'
    :return: list of articles
    """

    url = 'https://newsapi.org/v2/everything'

    response = requests.get(url, params=params, verify=False)
    out = response.json()
    articles = out['articles']

    if outfile:
        with open(outfile, 'w') as f:
            json.dumps(articles, f)

    return articles

if __name__ == '__main__':
    nyt_key = '26dcf973b8544fb1aa51c8680dd60f74'
    cnbc_key = 'd13a111d345643afa9b5585280adbbb2'
    query = 'Apple Inc'
    start_date = '20180601'
    query = query.replace(' ', '+')

    params = {'api-key': nyt_key, 'q': query, 'begin_date': start_date, 'sort': 'newest'}

    nyt_data = get_nyt_news(params, pages=2)

    start_date = '2018-09-01'
    params = {'q': query, 'from': start_date, 'sortBy': 'popularity',
              'language': 'en', 'apiKey': cnbc_key}

    cnbc_data = get_cnbc_news(params)
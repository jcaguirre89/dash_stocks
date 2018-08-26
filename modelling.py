from tickers_scraper import get_tickers
from price_scraper import Company
import pandas as pd
import pickle

def build_company_data(debug=False, pickle=True):
    """
    Get ticker dictionary from wiki and build dataframe with financial data
    :param debug: if true, use a single company (for testing)
    :param pickle: if true, pickle result
    :return: dataframe
    """
    names_and_tickers = get_tickers()
    if debug:
        names_and_tickers = {k: names_and_tickers[k] for k in ['aapl']}
    tickers = list(names_and_tickers.keys())
    companies = pd.DataFrame()
    for ticker in tickers:
        company = Company(ticker)
        company.data['name'] = names_and_tickers[ticker]
        df = pd.Series(company.data, name=ticker)
        companies = pd.concat([companies, df], axis=1)

    # transpose
    companies = companies.transpose()

    if pickle:
        companies.to_pickle(path='sp500_data.pkl')
    return companies


companies = build_company_data(debug=False, pickle=True)
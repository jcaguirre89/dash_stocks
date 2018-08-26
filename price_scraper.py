from urllib import request
import json
import datetime
import pandas as pd
import numpy as np


class Security:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_price(self, start, end):
        """
        scrapes yahoo finance to get historical adjusted close price and volume
        returns a dataframe
        """
        ticker = self.ticker
        # convert to timestamp
        start_ts = int(pd.Timestamp(start).timestamp())
        end_ts = int(pd.Timestamp(end).timestamp())

        price_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?symbol={ticker}&period1={start_ts}&period2={end_ts}&interval=1d&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=qntR3hW5Tko&corsDomain=finance.yahoo.com"

        with request.urlopen(price_url) as url:
            data = json.loads(url.read().decode())

        adj_close = data['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
        volume = data['chart']['result'][0]['indicators']['quote'][0]['volume']
        high = data['chart']['result'][0]['indicators']['quote'][0]['high']
        low = data['chart']['result'][0]['indicators']['quote'][0]['low']
        open_price = data['chart']['result'][0]['indicators']['quote'][0]['open']
        timestamps = data['chart']['result'][0]['timestamp']
        dates = [datetime.date.fromtimestamp(ts) for ts in timestamps]

        df = pd.DataFrame({'Close': adj_close, 'Volume': volume,
                           'Open': open_price, 'High': high,
                           'Low': low}, index=dates)
        df['Ticker'] = ticker

        return df


class ETF(Security):
    def __init__(self, ticker):
        super().__init__(ticker)


class Company(Security):
    def __init__(self, ticker):
        super().__init__(ticker)

    @property
    def country(self):
        return self.data['country']

    @property
    def sector(self):
        return self.data['sector']

    @property
    def industry(self):
        return self.data['industry']

    @property
    def city(self):
        return self.data['city']

    @property
    def state(self):
        return self.data['state']

    @property
    def zip_code(self):
        return self.data['zip_code']

    @property
    def summary(self):
        return self.data['summary']

    @property
    def data(self):
        """
        Scrapes Yahoo for latest fundamental data available

        :return: a dictionary with the retrieved data
        """
        fin_data_url = ('https://query2.finance.yahoo.com'
                        f'/v10/finance/quoteSummary/{self.ticker}?formatted=true'
                        '&lang=en-US'
                        '&region=US'
                        '&modules=summaryProfile'
                        '%2CfinancialData'
                        '%2CrecommendationTrend'
                        '%2CupgradeDowngradeHistory'
                        '%2Cearnings'
                        '%2CdefaultKeyStatistics'
                        '%2CcalendarEvents'
                        '&corsDomain=finance.yahoo.com'
                        )
        with request.urlopen(fin_data_url) as url:
            data = json.loads(url.read().decode())

        try:
            main_data = data['quoteSummary']['result'][0]['financialData']
        except KeyError:
            main_data = {}

        try:
            debt_to_equity = main_data['debtToEquity']['raw']
        except KeyError:
            debt_to_equity = np.nan
        try:
            earnings_growth = main_data['earningsGrowth']['raw']
        except KeyError:
            earnings_growth = np.nan
        try:
            profit_margin = main_data['profitMargins']['raw']
        except KeyError:
            profit_margin = np.nan
        try:
            roe = main_data['returnOnEquity']['raw']
        except KeyError:
            roe = np.nan
        try:
            rev_growth = main_data['revenueGrowth']['raw']
        except KeyError:
            rev_growth = np.nan
        try:
            n_shares = data['quoteSummary']['result'][0]['defaultKeyStatistics']['floatShares']['raw']
        except KeyError:
            n_shares = np.nan
        try:
            eps_t = data['quoteSummary']['result'][0]['defaultKeyStatistics']['trailingEps']['raw']
        except KeyError:
            eps_t = np.nan
        try:
            price_book = data['quoteSummary']['result'][0]['defaultKeyStatistics']['priceToBook']['raw']
        except KeyError:
            price_book = np.nan
        try:
            price = data['quoteSummary']['result'][0]['financialData']['currentPrice']['raw']
        except KeyError:
            price = np.nan
        try:
            eps_f = data['quoteSummary']['result'][0]['defaultKeyStatistics']['forwardEps']['raw']
        except KeyError:
            eps_f = np.nan
        try:
            beta = data['quoteSummary']['result'][0]['defaultKeyStatistics']['beta']['raw']
        except KeyError:
            beta = np.nan
        try:
            ev_ebitda = data['quoteSummary']['result'][0]['defaultKeyStatistics']['enterpriseToEbitda']['raw']
        except KeyError:
            ev_ebitda = np.nan
        try:
            ev_rev = data['quoteSummary']['result'][0]['defaultKeyStatistics']['enterpriseToRevenue']['raw']
        except KeyError:
            ev_rev = np.nan
        try:
            peg = data['quoteSummary']['result'][0]['defaultKeyStatistics']['pegRatio']['raw']
        except KeyError:
            peg = np.nan
        try:
            ebitda_margin = main_data['ebitdaMargins']['raw']
        except KeyError:
            ebitda_margin = np.nan
        try:
            n_analysts = main_data['numberOfAnalystOpinions']['raw']
        except KeyError:
            n_analysts = np.nan
        try:
            gross_margin = main_data['grossMargins']['raw']
        except KeyError:
            gross_margin = np.nan
        try:
            recommendation = main_data['recommendationKey']
        except KeyError:
            recommendation = np.nan
        try:
            target_price = main_data['targetMedianPrice']['raw']
        except KeyError:
            target_price = np.nan
        try:
            roa = main_data['returnOnAssets']['raw']
        except KeyError:
            roa = np.nan
        try:
            sector = data['quoteSummary']['result'][0]['summaryProfile']['sector']
        except KeyError:
            sector = np.nan
        try:
            industry = data['quoteSummary']['result'][0]['summaryProfile']['industry']
        except KeyError:
            industry = np.nan
        try:
            country = data['quoteSummary']['result'][0]['summaryProfile']['country']
        except KeyError:
            country = np.nan
        try:
            state = data['quoteSummary']['result'][0]['summaryProfile']['state']
        except KeyError:
            state = np.nan
        try:
            zip_code = data['quoteSummary']['result'][0]['summaryProfile']['zip']
        except KeyError:
            zip_code = np.nan
        try:
            city = data['quoteSummary']['result'][0]['summaryProfile']['city']
        except KeyError:
            city = np.nan
        try:
            address = data['quoteSummary']['result'][0]['summaryProfile']['address1']
        except KeyError:
            address = np.nan
        try:
            summary = data['quoteSummary']['result'][0]['summaryProfile']['longBusinessSummary']
        except KeyError:
            summary = np.nan

        # Get this quarter's actual and estimated earnings, the previous quarter's actual and estimate and the
        # last year's actual

        ret_dict = {
            'scrape_date': datetime.datetime.today().date(),
            'debt_to_equity': debt_to_equity,
            'earnings_growth': earnings_growth,
            'profit_margin': profit_margin,
            'roe': roe,
            'rev_growth': rev_growth,
            'eps_t': eps_t,
            'price_book': price_book,
            'ebitda_margin': ebitda_margin,
            'n_analysts': n_analysts,
            'gross_margin': gross_margin,
            'eps_f': eps_f,
            'price': price,
            'recommendation': recommendation,
            'target_price': target_price,
            'roa': roa,
            'summary': summary,
            'country': country,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'sector': sector,
            'industry': industry,
            'beta': beta,
            'ev_ebitda': ev_ebitda,
            'ev_rev': ev_rev,
            'peg': peg,
            'n_shares': n_shares,
            'address': address,
        }
        return ret_dict


if __name__ == '__main__':
    company = Company(ticker='aapl')
    start = datetime.date(2000, 1, 1)
    end = datetime.datetime.today().date()
    prices = company.get_price(start, end)

    tickers = ['tsla', 'aapl', 'ford']
    companies = pd.DataFrame()
    for ticker in tickers:
        company = Company(ticker)
        df = pd.Series(company.data, name=ticker)
        companies = pd.concat([companies, df], axis=1)

import pandas as pd
import sys

if 'google.colab' in sys.modules:
    dir_name = '/content/drive/MyDrive/DB_twstock'
else:
    dir_name = 'DB_twstock'
    
class DataReader():

    def get_twstock_close(dir_name=dir_name) -> pd.DataFrame:
        '''
        type:收盤價
        '''
        return pd.read_pickle(f"{dir_name}/Close.pkl")


    def get_twstock_open(dir_name=dir_name) -> pd.DataFrame:
        '''
        type:開盤價
        '''
        return pd.read_pickle(f"{dir_name}/Open.pkl")
    

    def get_twstock_high(dir_name=dir_name) -> pd.DataFrame:
        '''
        type:最高價
        '''
        return pd.read_pickle(f"{dir_name}/High.pkl")
    

    def get_twstock_low(dir_name=dir_name) -> pd.DataFrame:
        '''
        type:最低價
        '''
        return pd.read_pickle(f"{dir_name}/Low.pkl")
    

    def get_twstock_volume(dir_name=dir_name) -> pd.DataFrame:
        '''
        type:成交股數
        '''
        return pd.read_pickle(f"{dir_name}/Volume.pkl")
    

    def get_twstock_industry(dir_name=dir_name) -> pd.DataFrame:
        '''
        type:產業族群表
        '''
        return pd.read_pickle(f"{dir_name}/industry.pkl")
    

    def get_twstock_monthly_revenue(dir_name=dir_name) -> pd.DataFrame:
        '''
        type:當月營收
        '''
        return pd.read_pickle(f"{dir_name}/monthly_revenue.pkl")
    

    def get_twstock_margin_trading(dir_name=dir_name) -> pd.DataFrame:
        '''
        type:融資買超股數
        '''
        return pd.read_pickle(f"{dir_name}/margin_trading.pkl")
    

    def get_twstock_short_selling(dir_name=dir_name) -> pd.DataFrame:
        '''
        type:融券賣超股數
        '''
        return pd.read_pickle(f"{dir_name}/short_selling.pkl")
    

    def get_twstock_foreign_investors(dir_name=dir_name) -> pd.DataFrame:
        '''
        type:外資買賣超股數
        '''
        return pd.read_pickle(f"{dir_name}/foreign_investors.pkl")
    

    def get_twstock_investment_trust(dir_name=dir_name) -> pd.DataFrame:
        '''
        type:投信買賣超股數
        '''
        return pd.read_pickle(f"{dir_name}/investment_trust.pkl")
    

    def get_twstock_dealer(dir_name=dir_name) -> pd.DataFrame:
        '''
        type:自營商買賣超股數
        '''
        return pd.read_pickle(f"{dir_name}/dealer.pkl")
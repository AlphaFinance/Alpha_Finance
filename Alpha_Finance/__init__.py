import os
import sys
import os
import sys
import pandas as pd
import numpy as np
import concurrent.futures

__version__ = '0.2.3'

def create_dir(dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

def download_data(dir_name,data_name):
    if not os.path.isfile(f"{dir_name}/{data_name}.pkl"):
        datum = pd.read_pickle(f"https://github.com/AlphaFinance/DB_twstock/raw/main/database/{data_name}.pkl")
        datum.to_pickle(f"{dir_name}/{data_name}.pkl")
        print(data_name,'🆗')
        
def download_data_multithreading(dir_name):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        data_names = ['Close','Open','High','Low','Volume','monthly_revenue','industry','margin_trading','short_selling','dealer','foreign_investors','investment_trust']
        data = {executor.submit(download_data,dir_name,data_name):data_name for data_name in data_names}
        for datum in concurrent.futures.as_completed(data):
            break
            
            
def download():

    if 'google.colab' in sys.modules:
        from google.colab import drive
        drive.mount('/content/drive')
        dir_name = '/content/drive/MyDrive/DB_twstock'

    else:
        dir_name = 'DB_twstock'
        
    create_dir(dir_name)
    download_data_multithreading(dir_name)
    print('⭐⭐⭐⭐⭐ Finish ⭐⭐⭐⭐⭐')
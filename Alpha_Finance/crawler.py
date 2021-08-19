import requests
import datetime
import io
import pandas as pd
import time
import random
import concurrent.futures
from Alpha_Finance.data import DataReader


def crawl_price(date):
    
    # 將json改成csv ---refer to FinLab部落格
    url = f"https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date={date.strftime('%Y%m%d')}&type=ALLBUT0999&_=1629263883842"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/555.22 (KHTML, like Gecko) Chrome/92.0.1234.567 Safari/111.11'}
    res = requests.get(url,headers=headers)
    
    data = '\n'.join([l for l in res.text.split('\n') if len(l.split(',"'))>=12]).replace('=','')
    df_sii = pd.read_csv(io.StringIO(data)).rename(columns={'證券代號':'stock_id'}).set_index('stock_id')[['開盤價','收盤價','最高價','最低價','成交股數']]
    df_sii = df_sii.applymap(lambda s:pd.to_numeric(str(s).replace(',',''),errors='coerce')).dropna(axis=1,how='all')
    df_sii['date'] = pd.to_datetime(date)
    df_sii = df_sii.loc[[sid for sid in df_sii.index if len(sid)==4]]
    
    url = f"https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&o=csv&d={str(date.year-1911)+'/'+date.strftime('%m/%d')}&se=EW&s=0,asc,0"
    res = requests.get(url,headers=headers)
    
    data = '\n'.join([l for l in res.text.split('\n') if len(l.split(',"'))>=12])
    df_otc = pd.read_csv(io.StringIO(data))
    df_otc.columns = res.text.split('\n')[3].replace(' ','').split(',')
    df_otc = df_otc.rename(columns={'代號':'stock_id','收盤':'收盤價','開盤':'開盤價','最高':'最高價','最低':'最低價'}).set_index('stock_id')[['開盤價','收盤價','最高價','最低價','成交股數']]
    df_otc = df_otc.applymap(lambda s:pd.to_numeric(str(s).replace(',',''),errors='coerce')).dropna()
    df_otc['date'] = pd.to_datetime(date)
    df_otc = df_otc.loc[[sid for sid in df_otc.index if len(sid)==4]]
    
    time.sleep(random.randint(5,7))
    return df_sii.append(df_otc)



def crawl_price_multithreading(dates):
    
    print('========= Start crawling price =========')
    database = pd.DataFrame()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        data = {executor.submit(crawl_price,date):date for date in dates}
        for datum in concurrent.futures.as_completed(data):
            try:
                df = datum.result()
                database = database.append(df)
                print(df['date'].iloc[-1].strftime('%Y-%m-%d'),'🆗')
            except:
                pass
    
    try:
        database = database.sort_values('date')
        df = DataReader.get_twstock_close().append(database.pivot_table('收盤價','date','stock_id'))
        df.groupby(df.index).last()
        df.to_pickle('DB_twstock/Close.pkl')
        df = DataReader.get_twstock_open().append(database.pivot_table('開盤價','date','stock_id'))
        df.groupby(df.index).last()
        df.to_pickle('DB_twstock/Open.pkl')
        df = DataReader.get_twstock_high().append(database.pivot_table('最高價','date','stock_id'))
        df.groupby(df.index).last()
        df.to_pickle('DB_twstock/High.pkl')
        df = DataReader.get_twstock_low().append(database.pivot_table('最低價','date','stock_id'))
        df.groupby(df.index).last()
        df.to_pickle('DB_twstock/Low.pkl')
        df = DataReader.get_twstock_volume().append(database.pivot_table('成交股數','date','stock_id'))
        df.groupby(df.index).last()
        df.to_pickle('DB_twstock/Volume.pkl')
    except:
        pass
    print('=========       Finish✔         =========')
    
    
    
def crawl_institution(date):
    
    url = f"https://www.twse.com.tw/fund/T86?response=csv&date={date.strftime('%Y%m%d')}&selectType=ALLBUT0999&_=1629339983742"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/555.22 (KHTML, like Gecko) Chrome/92.0.1234.567 Safari/111.11'}
    res = requests.get(url,headers=headers)
    
    data = '\n'.join([l for l in res.text.split('\n') if len(l.split(',"'))>=12])
    df_sii = pd.read_csv(io.StringIO(data.replace('=',''))).rename(columns={'證券代號':'stock_id'}).set_index('stock_id')
    df_sii = df_sii.applymap(lambda s:pd.to_numeric(str(s).replace(',',''),errors='coerce')).dropna(axis=1,how='all')[['外陸資買賣超股數(不含外資自營商)','外資自營商買賣超股數','投信買賣超股數','自營商買賣超股數']]
    df_sii['date'] = pd.to_datetime(date)
    df_sii = df_sii.loc[[sid for sid in df_sii.index if len(sid)==4]]

    url = f"https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&o=csv&se=EW&t=D&d={str(date.year-1911)+'/'+date.strftime('%m/%d')}&s=0,asc"
    res = requests.get(url,headers=headers)
    
    data = '\n'.join([l for l in res.text.split('\n') if len(l.split(',"'))>=12])
    df_otc = pd.read_csv(io.StringIO(data))
    df_otc.columns = res.text.split('\n')[1].replace(' ','').replace('-','').split(',')
    df_otc = df_otc.rename(columns={'代號':'stock_id','外資及陸資(不含外資自營商)買賣超股數':'外陸資買賣超股數(不含外資自營商)'}).set_index('stock_id')
    df_otc = df_otc.applymap(lambda s:pd.to_numeric(str(s).replace(',',''),errors='coerce')).dropna(axis=1,how='all')[['外陸資買賣超股數(不含外資自營商)','外資自營商買賣超股數','投信買賣超股數','自營商買賣超股數']]
    df_otc['date'] = pd.to_datetime(date)
    df_otc = df_otc.loc[[sid for sid in df_otc.index if len(sid)==4]]
    
    time.sleep(random.randint(5,7))
    return df_sii.append(df_otc)


def crawl_institution_multithreading(dates):
    
    print('========= Start crawling institution =========')
    database = pd.DataFrame()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        data = {executor.submit(crawl_institution,date):date for date in dates}
        for datum in concurrent.futures.as_completed(data):
            try:
                df = datum.result()
                database = database.append(df)
                print(df['date'].iloc[-1].strftime('%Y-%m-%d'),'🆗')
            except:
                pass
                
    try:
        database = database.sort_values('date')
        database['外資買賣超股數'] = database[['外陸資買賣超股數(不含外資自營商)','外資自營商買賣超股數']].sum(axis=1)
        df = DataReader.get_twstock_foreign_investors().append(database.pivot_table('外資買賣超股數','date','stock_id'))
        df = df.groupby(df.index).last()
        df.to_pickle('DB_twstock/foreign_investors.pkl')
        df = DataReader.get_twstock_investment_trust().append(database.pivot_table('投信買賣超股數','date','stock_id'))
        df = df.groupby(df.index).last()
        df.to_pickle('DB_twstock/investment_trust.pkl')
        df = DataReader.get_twstock_dealer().append(database.pivot_table('自營商買賣超股數','date','stock_id'))
        df = df.groupby(df.index).last()
        df.to_pickle('DB_twstock/dealer.pkl')
    except:
        pass
    print('=========       Finish✔         =========')
    
    
    
def crawl_margin(date):
    
    url = f"https://www.twse.com.tw/exchangeReport/MI_MARGN?response=csv&date={date.strftime('%Y%m%d')}&selectType=ALL&_=1629348061458"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/555.22 (KHTML, like Gecko) Chrome/92.0.1234.567 Safari/111.11'}
    res = requests.get(url,headers)
    data = '\n'.join([l for l in res.text.split('\n') if len(l.split(',"'))>=12])
    df_sii = pd.read_csv(io.StringIO(data.replace('=',''))).rename(columns={'股票代號':'stock_id'}).set_index('stock_id')
    df_sii = df_sii.applymap(lambda s:pd.to_numeric(str(s).replace(',',''),errors='coerce')).dropna(axis=1,how='all')
    df_sii['融資買超股數'] = df_sii['買進']-df_sii['賣出']
    df_sii['融券賣超股數'] = df_sii['賣出.1']-df_sii['買進.1']
    df_sii['date'] = pd.to_datetime(date)
    df_sii = df_sii[['融資買超股數','融券賣超股數','date']].loc[[sid for sid in df_sii.index if len(sid)==4]]
    
    url = f"https://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal_result.php?l=zh-tw&o=csv&d={str(date.year-1911)+'/'+date.strftime('%m/%d')}&s=0,asc"
    res = requests.get(url,headers=headers)
    data = '\n'.join([l for l in res.text.split('\n') if len(l.split(',"'))>=12])
    df_otc = pd.read_csv(io.StringIO(data))
    df_otc.columns = res.text.split('\n')[2].replace(' ','').split(',')
    df_otc = df_otc.rename(columns={'代號':'stock_id'}).set_index('stock_id').applymap(lambda s:pd.to_numeric(str(s).replace(',',''),errors='coerce')).dropna(axis=1,how='all')
    df_otc['融資買超股數'] = df_otc['資買']-df_otc['資賣']
    df_otc['融券賣超股數'] = df_otc['券賣']-df_otc['券買']
    df_otc['date'] = pd.to_datetime(date)
    df_otc = df_otc[['融資買超股數','融券賣超股數','date']].loc[[sid for sid in df_otc.index if len(sid)==4]]
    
    time.sleep(random.randint(5,7))
    return df_sii.append(df_otc)


def crawl_margin_multithreading(dates):
    
    print('========= Start crawling margin =========')
    database = pd.DataFrame()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        data = {executor.submit(crawl_margin,date):date for date in dates}
        for datum in concurrent.futures.as_completed(data):
            try:
                df = datum.result()
                database = database.append(df)
                print(df['date'].iloc[-1].strftime('%Y-%m-%d'),'🆗')
            except:
                pass
    try:        
        database = database.sort_values('date')
        df = DataReader.get_twstock_margin_trading().append(database.pivot_table('融資買超股數','date','stock_id'))
        df = df.groupby(df.index).last()
        df.to_pickle('DB_twstock/margin_trading.pkl')
        df = DataReader.get_twstock_short_selling().append(database.pivot_table('融券賣超股數','date','stock_id'))
        df = df.groupby(df.index).last()
        df.to_pickle('DB_twstock/short_selling.pkl')
    except:
        pass
    print('=========       Finish✔         =========')
    
    
    
    
def crawl_monthly_revenue(month):
    
    if month.month==1:
        month_str = str(month.year-1912)+'_'+'12'
    else:
        month_str = str(month.year-1911)+'_'+str(month.month-1)
    
    url = 'https://mops.twse.com.tw/server-java/FileDownLoad'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/555.22 (KHTML, like Gecko) Chrome/92.0.1234.567 Safari/111.11'}
    payload = {
        'step': '9',
        'functionName': 'show_file',
        'filePath': '/home/html/nas/t21/sii/',
        'fileName': f"t21sc03_{month_str}.csv"
    }
    res = requests.post(url,headers=headers,data=payload)
    res.encoding = 'utf-8'
    df_sii = pd.read_csv(io.StringIO(res.text)).rename(columns={'公司代號':'stock_id','營業收入-當月營收':'當月營收'}).set_index('stock_id')
    df_sii = df_sii.applymap(lambda s:pd.to_numeric(str(s).replace(',',''),errors='coerce')).dropna(axis=1,how='all')
    df_sii['date'] = pd.to_datetime(month.strftime('%Y-%m')+'-10')
    
    time.sleep(7)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 20.0; Win64; x64) AppleWebKit/152.52 (KHTML, like Gecko) Chrome/93.0.1459.321 Safari/234.01'}
    payload = {
        'step': '9',
        'functionName': 'show_file',
        'filePath': '/home/html/nas/t21/otc/',
        'fileName': f"t21sc03_{month_str}.csv"
    }
    res = requests.post(url,headers=headers,data=payload)
    res.encoding = 'utf-8'
    df_otc = pd.read_csv(io.StringIO(res.text)).rename(columns={'公司代號':'stock_id','營業收入-當月營收':'當月營收'}).set_index('stock_id')
    df_otc = df_otc.applymap(lambda s:pd.to_numeric(str(s).replace(',',''),errors='coerce')).dropna(axis=1,how='all')
    df_otc['date'] = pd.to_datetime(month.strftime('%Y-%m')+'-10')
    time.sleep(8)

    return df_sii.append(df_otc)[['當月營收','date']]


def crawl_monthly_revenue_multithreading(months):
    
    print('========= Start crawling monthly_revenue =========')
    database = pd.DataFrame()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        data = {executor.submit(crawl_monthly_revenue,month):month for month in months}
        for datum in concurrent.futures.as_completed(data):
            try:
                df = datum.result()
                database = database.append(df)
                print(df['date'].iloc[-1].strftime('%Y-%m'),'🆗')
            except:
                print('查詢過於頻繁,請稍後再試!')
                
    try:
        database = database.sort_values('date')
        database.index = database.index.astype(str)

        df = DataReader.get_twstock_monthly_revenue().append(database.pivot_table('當月營收','date','stock_id'))
        df = df.groupby(df.index).last()
        df.to_pickle('DB_twstock/monthly_revenue.pkl')
    except:
        pass
    print('=========       Finish✔         =========')
    
    

def auto_crawler():
    
    start_date = DataReader.get_twstock_close().index[-1]+datetime.timedelta(1)
    end_date = datetime.datetime.now()
    dates = pd.date_range(start_date,end_date)
    crawl_price_multithreading(dates)
    
    start_date = DataReader.get_twstock_foreign_investors().index[-1]+datetime.timedelta(1)
    end_date = datetime.datetime.now()
    dates = pd.date_range(start_date,end_date)
    crawl_institution_multithreading(dates)
    
    start_date = DataReader.get_twstock_margin_trading().index[-1]+datetime.timedelta(1)
    end_date = datetime.datetime.now()
    dates = pd.date_range(start_date,end_date)
    crawl_margin_multithreading(dates)
    
    start_date = DataReader.get_twstock_monthly_revenue().index[-1]
    end_date = datetime.datetime.now()
    dates = pd.date_range(start_date,end_date)
    months = pd.to_datetime(sorted(list(set(dates.strftime('%Y-%m')))))
    crawl_monthly_revenue_multithreading(months)
    
    print('⭐⭐⭐⭐⭐ All Finish ⭐⭐⭐⭐⭐')
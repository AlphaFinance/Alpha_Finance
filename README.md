## Installation
Install using pip

```python
pip install Alpha_Finance
```

* 本地端環境  
[安裝talib](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)並儲存至user
```python
pip install TA_Lib-0.4.20-cp37-cp37m-win_amd64.whl
```

* colab環境  
```python
pip install talib-binary
```

---------------------------------------------------------------------------------------

## Taiwan Stock API

**Alpha_Finance** 為專門分析臺灣股市的Python套件，附帶自動化爬蟲及建立DB

最新版爬蟲數據包含

|面向|數據|
|-|-|
|技術面|開高低收量|
|籌碼面|三大法人、融資融券|
|基本面|月營收|


* 資料來源:
  [證交所](https://www.twse.com.tw/zh/), [櫃買中心](https://www.tpex.org.tw/web/)
  , [公開資訊觀測站](https://mops.twse.com.tw/mops/web/index)
  , [期交所](https://www.taifex.com.tw/cht/index)。
* API用於財務教育、非商業用途。資料僅供參考，使用者依本資料交易發生之損失需自行負責，本API不對資料內容錯誤、更新延誤或傳輸中斷負任何責任。

---------------------------------------------------------------------------------------------------------------------------------

### **Quick Start**

* #### [Colab ![](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/16hhqppSYhFqNiCeVbV_aAj0nsf6B3r2c?usp=sharing)

#### 下載歷史數據
```python
import Alpha_Finance

Alpha_Finance.download()
```

industry 🆗  
monthly_revenue 🆗  
dealer 🆗  
foreign_investors 🆗  
investment_trust 🆗  
Close 🆗  
Volume 🆗  
margin_trading 🆗  
Low 🆗  
short_selling 🆗  
High 🆗  
Open 🆗  
⭐⭐⭐⭐⭐ Finish ⭐⭐⭐⭐⭐

#### 取得數據庫資料
```python
from Alpha_Finance.data import DataReader

DataReader.get_twstock_close()
```

|date|0015|0050|0051|0052|0053|0054|
|-|-|-|-|-|-|-|
|2021-08-12|NaN|136.95|57.20|124.05|66.00|31.81|22.38|
|2021-08-13|NaN|135.65|56.35|122.55|65.40|31.30|22.45|
|2021-08-16|NaN|135.35|55.50|122.50|65.30|30.93|22.06|
|2021-08-17|NaN|134.35|54.80|121.20|64.70|30.67|

#### 自動化爬蟲
```python
from Alpha_Finance.crawler import auto_crawler

auto_crawler()
```
========= Start crawling price =========  
2021-07-12 🆗  
2021-07-13 🆗  
=========       Finish✔         =========  
========= Start crawling institution =========  
2021-07-12 🆗  
2021-07-13 🆗 
=========       Finish✔         =========  
========= Start crawling margin =========  
2021-07-12 🆗  
2021-07-13 🆗 
=========       Finish✔         =========  
========= Start crawling monthly_revenue =========  
2021-07 🆗  
=========       Finish✔         =========  
⭐⭐⭐⭐⭐ All Finish ⭐⭐⭐⭐⭐  

#### 模組套件
```python
from Alpha_Finance.stock import stock_dataframe,technical_chart

stock_id = '2330'
dfstock = stock_dataframe(stock_id)
technical_chart(dfstock,stock_id)
```
|date|open|close|low|high|volume|pct|
|----|----|-----|---|----|------|---|
|2021-08-13|585.0|581.0|579.0|585.0|25440.973|-0.85|
|2021-08-16|582.0|584.0|578.0|586.0|19949.389| 0.52|
|2021-08-17|580.0|580.0|578.0|582.0|31845.499|-0.68|
|2021-08-18|568.0|574.0|566.0|575.0|47063.629|-1.03|
|2021-08-19|573.0|559.0|559.0|573.0|42133.375|-2.61|

![](/images/technical_chart.png)  
  
#### 技術指標
```python
from Alpha_Finance import indicator

indicator.RSI(dfstock)
```  
|date  || 
|-|-|
|2021-08-13|42.373579|  
|2021-08-16|42.373579|  
|2021-08-17|40.643127|  
|2021-08-18|46.256672|  
|2021-08-19|42.602784|  

#### 個股回測
```python
from Alpha_Finance.backtest import backtest_single_stock
from Alpha_Finance.stock import stock_dataframe
import datetime

stock_id = '0050'
dfstock = stock_dataframe(stock_id)

def ma(n):
    return dfstock.close.rolling(n,min_periods=1).mean()

entry = (ma(5)>=ma(60))&(ma(5).shift()<ma(60).shift())
exit = (ma(5)<=ma(60))&(ma(5).shift()>ma(60).shift())
start_date = datetime.date(2014,5,5)
end_date = datetime.date(2021,8,23)

backtest_single_stock(dfstock,stock_id,entry,exit,start_date,end_date)
```

![](/images/backtest_chart.png)  
![](/images/backtest_roi.png)  
![](/images/backtest_log.png)  

----------------------------------------------------------------  

## Contact

##### 網站: https://alphafinance.github.io/  
##### Email: alphafinance.tw@gmail.com

---------------------------------------------------------------
## Reference

Alpha_Finance專案開發參考自:  
[twstock](https://twstock.readthedocs.io/zh_TW/latest/)  
[FinMind](https://finmindtrade.com/)  
[FinLab](https://www.finlab.tw/)  
[blog.louie.lu](https://blog.louie.lu/)

若有侵害版權疑慮，請來信或留言告知，我們將儘速移除相關內容。
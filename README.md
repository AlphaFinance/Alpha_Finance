## Installation
Install using pip

```python
pip install Alpha_Finance
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
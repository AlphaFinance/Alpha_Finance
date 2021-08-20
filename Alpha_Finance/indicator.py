import talib
import pandas as pd

def Convergence(dfstock,n=120):
    
    '''
    Inputs:
    date        open    close   low     high    volume     pct 
    ----------  -----   -----   -----   -----   ---------  -----
    2021-08-13  585.0   581.0   579.0   585.0   25440.973  -0.85
    2021-08-16  582.0   584.0   578.0   586.0   19949.389   0.52
    2021-08-17  580.0   580.0   578.0   582.0   31845.499  -0.68
    2021-08-18  568.0   574.0   566.0   575.0   47063.629  -1.03
    2021-08-19  573.0   559.0   559.0   573.0   42133.375  -2.61
    
    Parameters:
    n: 120
    
    Outputs:
    ub,mb,lb
    '''
    
    s = dfstock.copy()
    mb = ((s.open+s.close*3+s.low+s.high*3)/8).rolling(3,min_periods=1).mean()
    ub = mb.rolling(n).max()
    lb = mb-(ub-mb)
    
    return ub,mb,lb



def SMA(dfstock,n) -> pd.Series:
    
    '''
    Inputs:
    date        open    close   low     high    volume     pct 
    ----------  -----   -----   -----   -----   ---------  -----
    2021-08-13  585.0   581.0   579.0   585.0   25440.973  -0.85
    2021-08-16  582.0   584.0   578.0   586.0   19949.389   0.52
    2021-08-17  580.0   580.0   578.0   582.0   31845.499  -0.68
    2021-08-18  568.0   574.0   566.0   575.0   47063.629  -1.03
    2021-08-19  573.0   559.0   559.0   573.0   42133.375  -2.61
    '''
    
    return dfstock.close.rolling(n,min_periods=1).mean()



def RSI(dfstock,n=14) -> pd.Series:
    
    '''
    Inputs:
    date        open    close   low     high    volume     pct 
    ----------  -----   -----   -----   -----   ---------  -----
    2021-08-13  585.0   581.0   579.0   585.0   25440.973  -0.85
    2021-08-16  582.0   584.0   578.0   586.0   19949.389   0.52
    2021-08-17  580.0   580.0   578.0   582.0   31845.499  -0.68
    2021-08-18  568.0   574.0   566.0   575.0   47063.629  -1.03
    2021-08-19  573.0   559.0   559.0   573.0   42133.375  -2.61
    
    Parameters:
    n: 14
    '''
    
    return talib.RSI(dfstock.close,n)


def STOCH(dfstock,fastk_period=5,slowk_period=3,slowd_period=3) -> pd.Series:
    
    '''
    Inputs:
    date        open    close   low     high    volume     pct 
    ----------  -----   -----   -----   -----   ---------  -----
    2021-08-13  585.0   581.0   579.0   585.0   25440.973  -0.85
    2021-08-16  582.0   584.0   578.0   586.0   19949.389   0.52
    2021-08-17  580.0   580.0   578.0   582.0   31845.499  -0.68
    2021-08-18  568.0   574.0   566.0   575.0   47063.629  -1.03
    2021-08-19  573.0   559.0   559.0   573.0   42133.375  -2.61
    
    Parameters:
    fastk_period=5,slowk_period=3,slowd_period=3
    
    Outputs:
    slowk,slowd
    '''
    
    return talib.STOCH(dfstock.high,dfstock.low,dfstock.close,fastk_period=fastk_period,slowk_period=slowk_period,slowd_period=slowd_period)


def MACD(dfstock) -> pd.Series :
        
    '''
    Inputs:
    date        open    close   low     high    volume     pct 
    ----------  -----   -----   -----   -----   ---------  -----
    2021-08-13  585.0   581.0   579.0   585.0   25440.973  -0.85
    2021-08-16  582.0   584.0   578.0   586.0   19949.389   0.52
    2021-08-17  580.0   580.0   578.0   582.0   31845.499  -0.68
    2021-08-18  568.0   574.0   566.0   575.0   47063.629  -1.03
    2021-08-19  573.0   559.0   559.0   573.0   42133.375  -2.61
    '''
    
    return talib.MACD(dfstock.close)[2]
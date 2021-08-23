import pandas as pd
import yfinance as yf
from Alpha_Finance.data import DataReader
import talib
from pyecharts.charts import Kline,Line,Bar,Grid
import pyecharts.options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import CurrentConfig,NotebookType
from IPython.display import display,HTML
import os

CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB
Line().load_javascript()



def stock_dataframe(stock_id) -> pd.DataFrame:
    
    '''
    Output:
    date        open    close   low     high    volume     pct 
    ----------  -----   -----   -----   -----   ---------  -----
    2021-08-13	585.0	581.0	579.0	585.0	25440.973  -0.85
    2021-08-16	582.0	584.0	578.0	586.0	19949.389   0.52
    2021-08-17	580.0	580.0	578.0	582.0	31845.499  -0.68
    2021-08-18	568.0	574.0	566.0	575.0	47063.629  -1.03
    2021-08-19	573.0	559.0	559.0	573.0	42133.375  -2.61
    '''

    try:
        df = pd.DataFrame({
                'open':DataReader.get_twstock_open()[stock_id],
                'close':DataReader.get_twstock_close()[stock_id],
                'low':DataReader.get_twstock_low()[stock_id],
                'high':DataReader.get_twstock_high()[stock_id],
                'volume':DataReader.get_twstock_volume()[stock_id]/1000
            })
    except:
        s = yf.Ticker(stock_id).history('max')
        df = pd.DataFrame({
            'open':s['Open'],
            'close':s['Close'],
            'low':s['Low'],
            'high':s['High'],
            'volume':s['Volume']/1000
        })

    df['pct'] = round((df.close/df.close.shift()-1)*100,2)
    return df





def technical_chart(
    dfstock,
    stock_id,
    main_indicator=None,
    main_name=['','','','',''],
    second_indicator=None,
    second_name=['','','','',''],
    third_indicator=None,
    third_name='',
    markline = None
):
    '''
    dfstock:
    date        open    close   low     high    volume     pct 
    ----------  -----   -----   -----   -----   ---------  -----
    2021-08-13  585.0   581.0   579.0   585.0   25440.973  -0.85
    2021-08-16  582.0   584.0   578.0   586.0   19949.389   0.52
    2021-08-17  580.0   580.0   578.0   582.0   31845.499  -0.68
    2021-08-18  568.0   574.0   566.0   575.0   47063.629  -1.03
    2021-08-19  573.0   559.0   559.0   573.0   42133.375  -2.61
    
    stock_id = '2330' or '2330.TW'
    
    main_indicator = [ma5,ma20,ma60] , dtype:list
    main_name = ['ma5','ma20','ma60'] , dtype:list
    
    second_indicator = [RSI5,RSI10] , dtype:list
    second_name = ['RSI5','RSI10'] , dtype:list
    
    third_indicator = MACD , dtype:float
    third_name = 'MACD' , dtype:str
    '''
    
    s = dfstock.copy()
    x = s.index.astype(str).to_list()
    try:
        title = f"{stock_id} {DataReader.get_twstock_industry().loc[stock_id]['公司簡稱']}"
        subtitle = DataReader.get_twstock_industry().loc[stock_id]['族群類股']
    except:
        title = stock_id
        subtitle = None
    
    # 決定成交量顏色
    s['value'] = (s.close>s.open).astype(int)
    vol = s.reset_index().reset_index()[['index','volume','value']]

    kline = (
        Kline()
        .add_xaxis(x)
        .add_yaxis('Kline',s.values.tolist(),itemstyle_opts=opts.ItemStyleOpts(color="#f11421",color0="#34b298",border_color="#f11421",border_color0='#34b298'),
                   markline_opts=opts.MarkLineOpts(data=markline,symbol_size=8,symbol=['','triangle'],linestyle_opts=opts.LineStyleOpts(color='#003fa3',type_='',width=2.5)))
        # 建立多Y軸
        .extend_axis(yaxis=opts.AxisOpts('value','volume',max_=round(s.volume.max()*3)))
        .extend_axis(yaxis=opts.AxisOpts('value','pct',min_=0,max_=10000,offset=5000))
        .set_global_opts(
            title_opts=opts.TitleOpts(title,subtitle=subtitle),
            # 可互動介面
            tooltip_opts=opts.TooltipOpts(trigger='axis',axis_pointer_type='cross',background_color='rgba(0,0,0,0.4)'),
            # 多圖連接
            axispointer_opts=opts.AxisPointerOpts(True,[{'xAxisIndex':'all'}]),
            # 縮放時間軸
            datazoom_opts=[opts.DataZoomOpts(range_start=95,range_end=100,xaxis_index=[0,1,2]),opts.DataZoomOpts(type_='inside',range_start=95,range_end=100,xaxis_index=[0,1,2])],
            # 成交量顏色
            visualmap_opts=opts.VisualMapOpts(series_index=[1,4],dimension=2,is_piecewise=True,pieces=[{'value':0,'color':'#34b298'},{'value':1,'color':'#f11421'}]),
            # 背景
            yaxis_opts=opts.AxisOpts(is_scale=True,splitarea_opts=opts.SplitAreaOpts(areastyle_opts=opts.AreaStyleOpts(0.8)))
        )
    )

    bar = Bar().add_yaxis('volume',vol.values.tolist(),yaxis_index=1,label_opts=opts.LabelOpts(False))
    line = Line().add_xaxis(x).add_yaxis('pct',s.pct.tolist(),yaxis_index=2,label_opts=opts.LabelOpts(False))
    
    # 主圖指標
    main_line = Line().add_xaxis(x)
    if main_indicator is None:
        def ma(n):
            return round(s.close.rolling(n,min_periods=1).mean(),2)
        for n,color in zip([5,20,60,120,240],['#f6be10','#c82bff','#1088f6','#09d33b','#ff338f']):
            main_line.add_yaxis(f"ma{n}",ma(n),is_symbol_show=False,label_opts=opts.LabelOpts(False),itemstyle_opts=opts.ItemStyleOpts(color=color))
    else:
        for y,name,color in zip(main_indicator,main_name,['#f6be10','#c82bff','#1088f6','#09d33b','#ff338f']):
            main_line.add_yaxis(name,y,is_symbol_show=False,label_opts=opts.LabelOpts(False),itemstyle_opts=opts.ItemStyleOpts(color=color))
            
    kline.overlap(bar)
    kline.overlap(line)
    kline.overlap(main_line)
    
    # 副圖指標
    second_chart = (
        Line()
        .add_xaxis(x)
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_top='400px'),
            yaxis_opts=opts.AxisOpts(splitarea_opts=opts.SplitAreaOpts(areastyle_opts=opts.AreaStyleOpts(0.8)))
        )
    )
    if second_indicator is None:
        for n,color in zip([5,10],['#0772e4','#dd5570']):
            second_chart.add_yaxis(f"RSI{n}",round(talib.RSI(s.close.ffill(),n),2),xaxis_index=1,yaxis_index=3,is_symbol_show=False,label_opts=opts.LabelOpts(False),itemstyle_opts=opts.ItemStyleOpts(color))
    else:
        for y,name,color in zip(second_indicator,second_name,['#f6be10','#c82bff','#1088f6','#09d33b','#ff338f']):
            second_chart.add_yaxis(name,y,xaxis_index=1,yaxis_index=3,is_symbol_show=False,label_opts=opts.LabelOpts(False),itemstyle_opts=opts.ItemStyleOpts(color))

    # 底圖指標
    third_chart = (
        Bar()
        .add_xaxis(x)
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_top='520px'),
            yaxis_opts=opts.AxisOpts(splitarea_opts=opts.SplitAreaOpts(areastyle_opts=opts.AreaStyleOpts(0.8)))
        )
    )
    if third_indicator is None:
        third_chart.add_yaxis('MACD',round(talib.MACD(s.close.ffill())[2],2).tolist(),xaxis_index=2,yaxis_index=4,label_opts=opts.LabelOpts(False),
                              itemstyle_opts=opts.ItemStyleOpts(color=JsCode("""function(params) {var colorList;if (params.data >= 0) {colorList='#f11421'} else {colorList='#34b298'} return colorList}""")))
    else:
        third_chart.add_yaxis(third_name,third_indicator.tolist(),xaxis_index=2,yaxis_index=4,label_opts=opts.LabelOpts(False),
                              itemstyle_opts=opts.ItemStyleOpts(color=JsCode("""function(params) {var colorList;if (params.data >= 0) {colorList='#f11421'} else {colorList='#34b298'} return colorList}""")))

    grid = Grid(init_opts=opts.InitOpts('1200px','650px'))
    grid.add(kline,grid_opts=opts.GridOpts('5%','50px',height='320px'),is_control_axis_index=True)
    grid.add(second_chart,grid_opts=opts.GridOpts('5%','430px',height='60px'),is_control_axis_index=True)
    grid.add(third_chart,grid_opts=opts.GridOpts('5%','550px',height='60px'),is_control_axis_index=True)
    
    grid.render()
    display(HTML(filename='render.html'))
    os.remove('render.html')
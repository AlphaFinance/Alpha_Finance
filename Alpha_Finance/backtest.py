import datetime
import numpy as np
import pandas as pd
import tqdm
import plotly.figure_factory as ff
from Alpha_Finance.stock import technical_chart
from pyecharts.charts import Line,Grid
import pyecharts.options as opts
from pyecharts.globals import CurrentConfig,NotebookType
from IPython.display import display,HTML
import os

CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB
Line().load_javascript()

def backtest_single_stock(dfstock,stock_id,entry,exit,start_date,end_date,stop_loss=np.nan,stop_profit=np.nan,stop_drawdown=np.nan,discount_rate=0.6):
    
    '''
    Parameters
    ----------
    
    dfstock:
    date        open    close   low     high    volume     pct 
    ----------  -----   -----   -----   -----   ---------  -----
    2021-08-13  585.0   581.0   579.0   585.0   25440.973  -0.85
    2021-08-16  582.0   584.0   578.0   586.0   19949.389   0.52
    2021-08-17  580.0   580.0   578.0   582.0   31845.499  -0.68
    2021-08-18  568.0   574.0   566.0   575.0   47063.629  -1.03
    2021-08-19  573.0   559.0   559.0   573.0   42133.375  -2.61
    
    stock_id = '2330' or '2330.TW'
    
    entry(exit):
    date
    2018-05-02    False
    2018-05-03     True
    2018-05-04    False
    2018-05-07    False
    2018-05-08     True
                  ...  
    2021-08-16    False
    2021-08-17     True
    2021-08-18    False
    2021-08-19     True
    2021-08-20    False
    
    start_date(end_date) = datatime.date(2018,5,2) or '2018-05-02'
    
    stop_loss = -10 or 10 -> -10
    stop_profit = -10 or 10 -> -10
    stop_drawdown = -10 or 10 -> -10
    
    Output:
    yc = backtest_single_stock(dfstock,stock_id,entry,exit,start_date,end_date)
    '''
    
    dates = entry[entry][start_date:end_date].index
    log = pd.DataFrame()
    yc = pd.DataFrame()
    init = 1
    init_fees = 1
    markline = []

    for i in tqdm.tqdm_notebook(range(0,len(dates))):
        sd = dates[i]
        try:
            ed = dates[i+1]
        except:
            ed = end_date

        s = dfstock[sd:ed].close.copy()
        s = pd.Series(np.where(exit[sd:ed].shift().fillna(False).cumsum()==0,s[sd:ed],np.nan),index=s.index)
        s = pd.Series(np.where(((s/s.iloc[0]-1)*100<=-abs(stop_loss)).shift().fillna(False).cumsum()==0,s[sd:ed],np.nan),index=s.index)
        s = pd.Series(np.where(((s/s.cummax()-1)*100<=-abs(stop_drawdown)).shift().fillna(False).cumsum()==0,s[sd:ed],np.nan),index=s.index)
        s = pd.Series(np.where(((s/s.iloc[0]-1)*100>=abs(stop_profit)).shift().fillna(False).cumsum()==0,s[sd:ed],np.nan),index=s.index)

        log = log.append(pd.DataFrame({
            'entry_date':s.index[0],
            'entry_price':round(s.iloc[0],2),
            'exit_date':s.dropna().index[-1],
            'exit_price':round(s.dropna().iloc[-1],2),
            'ROI':round((s.dropna().iloc[-1]/s.dropna().iloc[0]-1)*100,2),
            'ROI_fees':round((s.dropna().iloc[-1]/s.dropna().iloc[0]/(1+3/1000+1.425*2/1000*discount_rate)-1)*100,2),
        },index=[stock_id]))

        yc = yc.append(pd.DataFrame({
            'ROI':s.ffill()/s.iloc[0]*init,
            'ROI_fees':s.ffill()/s.iloc[0]/(1+3/1000+1.425/1000*2*discount_rate)*init_fees
        }))
        init = yc.iloc[-1]['ROI']
        init_fees = yc.iloc[-1]['ROI_fees']

        markline.append([{'xAxis':s.index.astype(str)[0],'yAxis':s.iloc[0]},{'xAxis':s.dropna().index.astype(str)[-1],'yAxis':s.dropna().iloc[-1]}])

    log[['entry_date','exit_date']] = log[['entry_date','exit_date']].astype(str)
    yc = yc.groupby(yc.index).mean()
    yc['symbol'] = dfstock.close.reindex(yc.index)/dfstock.close.reindex(yc.index).iloc[0]
    for name in ['ROI','symbol']:
        yc[f"{name}_drawdown"] = round((yc/yc.cummax()-1)[name]*100,2)
        
    x = yc.index.astype(str).to_list()

    line = (Line().add_xaxis(x))
    for name,color in zip(['ROI','ROI_fees','symbol'],['#e07171','#3b5ac9','#858585']):
        line.add_yaxis(name,round(((yc[name]-1)*100),2).to_list(),label_opts=opts.LabelOpts(False),is_symbol_show=False,itemstyle_opts=opts.ItemStyleOpts(color=color),linestyle_opts=opts.LineStyleOpts(width=1.5))
    line.set_global_opts(
        title_opts=opts.TitleOpts(f"Backtest-{stock_id}"),
        tooltip_opts=opts.TooltipOpts(trigger='axis',axis_pointer_type='cross',background_color='rgba(0,0,0,0.4)'),
        datazoom_opts=[opts.DataZoomOpts(range_start=0,range_end=100,xaxis_index=[0,1]),opts.DataZoomOpts(type_='inside',range_start=0,range_end=100,xaxis_index=[0,1])],
        axispointer_opts=opts.AxisPointerOpts(True,[{'xAxisIndex':'all'}]),
        yaxis_opts=opts.AxisOpts(splitarea_opts=opts.SplitAreaOpts(areastyle_opts=opts.AreaStyleOpts(.8)),axislabel_opts=opts.LabelOpts(formatter='{value} %'),)
    )

    second_line = Line().add_xaxis(x)
    for name,color in zip(['ROI_drawdown','symbol_drawdown'],['#46c896','#858585']):
        second_line.add_yaxis(
            name,yc[name].tolist(),
            xaxis_index=1,yaxis_index=1,
            label_opts=opts.LabelOpts(False),is_symbol_show=False,itemstyle_opts=opts.ItemStyleOpts(color=color),
            linestyle_opts=opts.LineStyleOpts(width=2.5),areastyle_opts=opts.AreaStyleOpts(0.3)
        )
    second_line.set_global_opts(
        yaxis_opts=opts.AxisOpts(splitarea_opts=opts.SplitAreaOpts(areastyle_opts=opts.AreaStyleOpts(0.8)),axislabel_opts=opts.LabelOpts(formatter='{value} %'),),
        legend_opts=opts.LegendOpts(pos_top='450px')
    )

    grid = Grid(init_opts=opts.InitOpts('1200px','620px'))
    grid.add(line,grid_opts=opts.GridOpts(pos_top='5%',height='400px'),is_control_axis_index=True)
    grid.add(second_line,grid_opts=opts.GridOpts(pos_top='480px',height='60px'),is_control_axis_index=True)
    grid.render()
    display(HTML(filename='render.html'))
    os.remove('render.html')
    
    technical_chart(dfstock,stock_id,markline=markline)
    
    KPI = pd.DataFrame({
        'Start Date':start_date.strftime('%Y-%m-%d'),
        'End Date':end_date.strftime('%Y-%m-%d'),
        'Duration':len(pd.date_range(start_date,end_date)),
        'Win Rate':f"{round((log['ROI']>0).sum()/len(log)*100,2)} %",
        'Max Drawdown(%)':f"{round(yc['ROI_drawdown'].min(),2)} %",
        'Avg Drawdown(%)':f"{round(yc['ROI_drawdown'].mean(),2)} %",
        'Avg ROI(%)':f"{round(log['ROI'].mean(),2)} %",
        'Ann ROI(%)':f"{round((yc['ROI'].iloc[-1]**(1/(len(yc)/250))-1)*100,2)} %",
        'Sharpe Ratio (Ann)':round((yc['ROI'].pct_change()*100).mean()/(yc['ROI'].pct_change()*100).std()*(252**(1/2)),3),
        'ROI Final(%)':f"{round((yc.iloc[-1]['ROI']-1)*100,2)} %",
        'ROI_fees Final(%)':f"{round((yc.iloc[-1]['ROI_fees']-1)*100,2)} %",
        'Symbol Final(%)':f"{round((yc.iloc[-1]['symbol']-1)*100,2)} %",
    },index=['Key Performance Indicator']).transpose()
    
    for t,w in zip([KPI,round(log,2)],[450,1000]):
        fig = ff.create_table(t,index=True)
        fig.layout.width = w
        fig.show()
        
    return yc
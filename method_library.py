#Standard Python library imports
import numpy as np 
import pandas as pd 

#Local imports


def calc_rsi(prices, n=14):
    '''
    Calculates the Relative Strength Index 

    Parameters:
    ------------
    prices : Series
        The column from a dataframe for which you want to calculate RSI.
    n : int, optional (default=14) 
        The number of periods to calculate RSI over.

    Returns:
    ------------
    rsi_df : dataframe object        
    '''

    deltas = np.diff(prices)
    seed = deltas[:n]
    up = seed[seed>=0].sum()+0.000001/n
    down = -seed[seed<0].sum()+0.000001/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[n] = 100. - (100./(1.+rs))
    
    for i in range(n, len(prices)):
        delta = deltas[i-1]
        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n
        rs = up/down
        rsi[i] = 1. - (1./(1.+rs))
    rsi_df=pd.DataFrame(rsi)
    rsi_df=rsi_df.round(2)
    return rsi_df


def slow_stochs_k(series,period=14):
    '''
    Calculates the slow stochastic oscillator. 

    Parameters:
    -----------
    series : series
        The dataframe column for which you want to calculate SSK
    period : int, optional (default=14)
        The period over which youn want SSK calculated.

    Returns:
    -----------
    result : dataframe object
        The original series joined with the new SSK data.

    '''
    period_max=series.rolling(window=period,center=False).max()
    period_min=series.rolling(window=period,center=False).min()
    result=(series-period_min)/(period_max - period_min)
    return result    


def roc(series,period):
    '''
    Method for calculating the Rate of Change indicator.

    Parameters:
    -----------
    series : series, 
        The dataframe column that you want ROC calculated over.
    period : int
        The number of periods over which you want ROC calculated.    
    '''
    result = series-series.shift(period)
    return result    


def simple_moving_average(series, period):
    '''
    Calculated a simple moving average

    Parameters:
    ----------
    series : series 
        The dataframe column that you want the SMA calculated for.
    '''
    x=series.rolling(window=period,center=False).mean()
    return x    


def moving_average_deviation(series01,series02):
    '''
    Calculates the ratio of two time series. Typically a closing price series 
    and a moving average series.   

    Parameters:
    ----------
    series01 : series 
        Can be any time series column, including another moving average
    series02 : series
        Can be any time series column, including another moving average
    '''
    x=(series01-series02)/series02
    return x    


def prox_to_bollinger_bands(series,period, deviation):
    '''
    Calculates the proximity of the time series to the UPPER bollinger band.  A value of 0 indicates
    coincidence with the lower bollinger band. A value of 1 indicates coincidence with the upper bollinger band.
    Values are theoretically unbounded (normally distributed)

    Parameters:
    -----------
    series : series,
        Dataframe column that you want to calculate proximity for.  Typically the closing price.
    period : int 
        The period that you want the bollinger bands calculated over. 
    deviation : int 
        The number of standard deviations from the mean you want the bolllinger bands to represent.        
    '''
    x=series.rolling(window=period).mean()
    x_std=series.rolling(window=period).std()
    upper_bollinger=x+(deviation*x_std)
    lower_bollinger=x-(deviation*x_std)
    prox=(series-lower_bollinger)/(upper_bollinger-lower_bollinger)
    return prox   


def bollinger_bands(series, period, deviation):
    '''
    Calculates the upper and lower bollinger bands for a timeseries

    Parameters:
    -----------
    series : series
        The dataframe column the bollinger bands will be calculated for.
    '''
    x=series.rolling(window=period).mean()
    x_std=series.rolling(window=period).std()
    upper_bollinger=x+(deviation*x_std)
    lower_bollinger=x-(deviation*x_std)
    return upper_bollinger, lower_bollinger
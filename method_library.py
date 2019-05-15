#Standard Python library imports
import numpy as np 
import pandas as pd 

#Local imports


def CalcRSI(prices, n=14):
    '''
    Calculates the Relative Strength Index 

    Parameters:
    ___________
    prices : Series
        The column from a dataframe for which you want to calculate RSI.
    n : int, optional (default=14) 
        The number of periods to calculate RSI over.    
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
    rsiDF=pd.DataFrame(rsi)
    rsiDF=rsiDF.round(2)
    return rsiDF
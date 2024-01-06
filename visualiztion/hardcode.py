import plotly.graph_objects as go
from patterns.candles import *

def init_figure(df):
    # Create the candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'],
                                         name='Candlestick')])
    return fig 


def add_patterns_to_figure(fig, df):
    df['Doji'] = is_doji(df)
    df['Bullish_Engulfing'] = is_bullish_engulfing(df)
    df['Bearish_Engulfing'] = is_bearish_engulfing(df)

    doji_indices = df['Doji']
    bullish_engulfing_indices = df['Bullish_Engulfing']
    bearish_engulfing_indices = df['Bearish_Engulfing']
    
    
    # # Find where patterns are True
    # doji_days = df[df['Doji'] == True]
    # bullish_engulfing_days = df[df['Bullish_Engulfing'] == True]
    # bearish_engulfing_days = df[df['Bearish_Engulfing'] == True]

    # Add markers for Doji
    fig.add_trace(go.Scatter(
        x=df.index[doji_indices],
        y=df['Close'][doji_indices],
        mode='markers',
        marker=dict(color='blue', size=10),
        name='Doji'
    ))

    # Add markers for Bullish Engulfing
    fig.add_trace(go.Scatter(
        x=df.index[bullish_engulfing_indices],
        y=df['Close'][bullish_engulfing_indices],
        mode='markers',
        marker=dict(color='green', size=10),
        name='Bullish Engulfing'
    ))

    # Add markers for Bearish Engulfing
    fig.add_trace(go.Scatter(
        x=df.index[bearish_engulfing_indices],
        y=df['Close'][bearish_engulfing_indices],
        mode='markers',
        marker=dict(color='red', size=10),
        name='Bearish Engulfing'
    ))

def update_layout_bla_bla(fig):
    # Update layout
    fig.update_layout(
        title='Candlestick chart with pattern markers',
        yaxis_title='Price',
        xaxis_title='Date',
        xaxis=dict(fixedrange=False),
        yaxis=dict(fixedrange=False)
    )


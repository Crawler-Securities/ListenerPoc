# installed imports
import plotly.graph_objects as go
import pandas as pd

# pure python imports
from typing import Callable
from datetime import datetime, timedelta
import re


class ChartInstance:
    """
    ChartInstance class for managing and displaying financial chart data.

    Attributes:
        DEFAULT_SHOWTIME_DEVIATION (int): The default deviation for showtime calculation.
        ticker (str): The ticker symbol for the financial instrument.
        _candle_interval (str): The interval of the candlestick data (e.g., '1d' for one day).
        _time_range (Tuple[datetime, datetime]): The start and end times for the chart data.
        _showtime (Tuple[datetime, datetime]): The start and end times for displaying the chart.
        _chart_provider (Callable[[str, datetime, datetime, str], pd.DataFrame]): 
            A callable that provides chart data. It takes a ticker symbol, start time, end time, 
            and candle interval as arguments and returns a pandas DataFrame. The dataframe
            is expected to have the following columns: 'Open', 'High', 'Low', 'Close' and datetime for index.
    """
    DEFAULT_SHOWTIME_DEVIATION = 10

    ticker: str
    _candle_interval: str
    _time_range: tuple[datetime, datetime]
    _showtime: tuple[datetime, datetime]
    _chart_provider: Callable[[str, datetime, datetime, str], pd.DataFrame]

    def __init__(self,
                 ticker: str,
                 time_range: tuple[datetime, datetime],
                 candle_period: str = '1d',
                 showtime: tuple[datetime, datetime] or None = None,
                 chart_provider: callable or None = None,
                 ) -> None:
        # none optional arguments
        self.ticker = ticker
        self._candle_interval = candle_period
        self._time_range = time_range

        # optional arguments
        self._showtime = showtime or self._get_default_showtime(time_range)
        self._chart_provider = chart_provider or self._default_chart_provider

    def get_figure(self) -> go.Figure:
        """
        Retruns a figure of simple candle sticks of the showtime timerange
        using the chart provider
        """
        df = self._get_chart_data()
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                                             open=df['Open'],
                                             high=df['High'],
                                             low=df['Low'],
                                             close=df['Close'],
                                             name='Candlestick')])
        self._mark_timerange(fig)
        self._update_layout(fig)
        return fig

    # region private methods

    def _default_chart_provider(self,
                                ticker: str,
                                start: datetime,
                                end: datetime,
                                interval: str) -> pd.DataFrame:
        """
        The default chart provider is the one that is used by the ChartInstance
        to get the chart data. it uses the yfinance library to get the data.
        
        """
        import yfinance as yf
        return yf.Ticker(ticker) \
            .history(
                start=start,
                end=end,
                interval=interval,)

    def _get_chart_data(self) -> pd.DataFrame:
        """
        Get the chart data from the chart provider.
        """
        return self._chart_provider(
            ticker=self.ticker,
            start=self._showtime[0],
            end=self._showtime[1],
            interval=self._candle_interval,
        )

    def _get_default_showtime(self, time_range: tuple[datetime, datetime]):
        """
        The default showtime is
        DEFAULT_SHOWTIME_DEVIATION time periods before the start of the time range 
        and DEFAULT_SHOWTIME_DEVIATION time periods after the end of the time range.
        """

        start_time, end_time = time_range

        # Parse the candle period
        match = re.match(r"(\d+)([dhm])", self._candle_interval)
        if not match:
            raise ValueError("Invalid candle period format")

        quantity, unit = int(match.group(1)), match.group(2)

        # Calculate the timedelta for one period
        if unit == 'd':
            delta = timedelta(days=quantity)
        elif unit == 'h':
            delta = timedelta(hours=quantity)
        elif unit == 'm':
            delta = timedelta(minutes=quantity)
        else:
            raise ValueError("Unsupported time unit")

        # Extend the time range
        extended_start = start_time - self.DEFAULT_SHOWTIME_DEVIATION * delta
        extended_end = end_time + self.DEFAULT_SHOWTIME_DEVIATION * delta

        return extended_start, extended_end

    def _mark_timerange(self, fig: go.Figure) -> None:
        """
        Mark the timerange on the figure.
        """
        # add two vertical lines to mark the start and end of the self._time_range
        fig.add_vline(x=self._time_range[0], line_width=1, line_dash="dash", line_color="green")
        fig.add_vline(x=self._time_range[1], line_width=1, line_dash="dash", line_color="green")
    def _update_layout(self, fig: go.Figure) -> None:
        """
        Update the layout of the figure.
        """
        # get rid of the time slider
        fig.update_layout(xaxis_rangeslider_visible=False)
    # endregion

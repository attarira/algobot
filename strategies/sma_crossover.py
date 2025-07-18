import pandas as pd

class SMACrossoverStrategy:
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']
        signals['short_sma'] = data['Close'].rolling(window=self.short_window, min_periods=1).mean()
        signals['long_sma'] = data['Close'].rolling(window=self.long_window, min_periods=1).mean()
        signals['signal'] = 0
        signals.loc[signals.index[self.short_window:], 'signal'] = (
            signals['short_sma'][self.short_window:] > signals['long_sma'][self.short_window:]
        ).astype(int)
        signals['positions'] = signals['signal'].diff().fillna(0)
        return signals 
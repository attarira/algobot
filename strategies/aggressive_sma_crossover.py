import pandas as pd
from strategies.sma_crossover import SMACrossoverStrategy

class AggressiveSMACrossoverStrategy(SMACrossoverStrategy):
    def __init__(self, short_window, long_window, stop_loss_pct=0.03, momentum_window=3, momentum_threshold=0.01):
        super().__init__(short_window, long_window)
        self.stop_loss_pct = stop_loss_pct  # e.g., 0.03 for 3%
        self.momentum_window = momentum_window
        self.momentum_threshold = momentum_threshold

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']
        signals['short_sma'] = data['Close'].rolling(window=self.short_window, min_periods=1).mean()
        signals['long_sma'] = data['Close'].rolling(window=self.long_window, min_periods=1).mean()
        signals['positions'] = 0
        # Buy when short SMA crosses above long SMA, sell when it crosses below
        signals['positions'] = (signals['short_sma'] > signals['long_sma']).astype(int)
        signals['positions'] = signals['positions'].replace({0: -1})

        # Momentum filter: only trade if price change over momentum_window exceeds threshold
        signals['momentum'] = signals['price'].pct_change(self.momentum_window)
        signals['positions'] = signals.apply(
            lambda row: row['positions'] if abs(row['momentum']) > self.momentum_threshold else 0, axis=1
        )

        # Stop-loss logic: add a column for stop-loss price
        signals['stop_loss'] = signals['price'] * (1 - self.stop_loss_pct)
        return signals

import pandas as pd

class SandboxBroker:
    def __init__(self, starting_capital=10000, max_risk_per_trade=0.05):
        self.starting_capital = starting_capital
        self.cash = starting_capital
        self.max_risk_per_trade = max_risk_per_trade
        self.position = 0
        self.portfolio_value = starting_capital
        self.trades = []

    def run_paper_trading(self, data, signals):
        for date, row in signals.iterrows():
            price = row['price']
            position_signal = row['positions']
            if position_signal == 1 and self.cash > 0:  # Buy signal
                max_trade_value = self.cash * self.max_risk_per_trade
                shares = max_trade_value // price
                if shares > 0:
                    self.position += shares
                    self.cash -= shares * price
                    self.trades.append({'date': date, 'type': 'BUY', 'shares': shares, 'price': price})
                    print(f"BUY {shares} @ {price:.2f} on {date.date()}")
            elif position_signal == -1 and self.position > 0:  # Sell signal
                self.cash += self.position * price
                self.trades.append({'date': date, 'type': 'SELL', 'shares': self.position, 'price': price})
                print(f"SELL {self.position} @ {price:.2f} on {date.date()}")
                self.position = 0
            # Update portfolio value
            self.portfolio_value = self.cash + self.position * price
        print(f"Final Portfolio Value: ${self.portfolio_value:.2f}")
        print(f"Total Trades: {len(self.trades)}") 
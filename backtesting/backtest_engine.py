import pandas as pd
import numpy as np

class BacktestEngine:
    def __init__(self, data, strategy, starting_capital=10000, risk_per_trade=0.05, symbol_for_strategy=None):
        self.data = data
        self.strategy = strategy
        self.starting_capital = starting_capital
        self.risk_per_trade = risk_per_trade
        self.symbol_for_strategy = symbol_for_strategy # New
        self.trades = []
        self.portfolio_history = []

    def run(self):
        # Pass symbol to strategy if it's the sentiment-aware one
        if self.symbol_for_strategy:
            signals = self.strategy.generate_signals(self.data, self.symbol_for_strategy)
        else:
            signals = self.strategy.generate_signals(self.data)
            
        cash = self.starting_capital
        position = 0
        portfolio_value = self.starting_capital

        for date, row in signals.iterrows():
            price = row['price']
            
            # Handle Buy/Sell signals
            if row['positions'] == 1 and cash > 0:  # Buy
                trade_value = cash * self.risk_per_trade
                shares_to_buy = trade_value // price
                if shares_to_buy > 0:
                    cash -= shares_to_buy * price
                    position += shares_to_buy
                    self.trades.append({'date': date, 'type': 'BUY', 'shares': shares_to_buy, 'price': price})

            elif row['positions'] == -1 and position > 0:  # Sell
                cash += position * price
                self.trades.append({'date': date, 'type': 'SELL', 'shares': position, 'price': price})
                position = 0
            
            # Update portfolio value for this day
            portfolio_value = cash + position * price
            self.portfolio_history.append({'date': date, 'portfolio_value': portfolio_value})

        return pd.DataFrame(self.portfolio_history)

    def calculate_metrics(self, portfolio_history_df):
        if portfolio_history_df.empty:
            return {}
            
        final_value = portfolio_history_df['portfolio_value'].iloc[-1]
        total_return = (final_value / self.starting_capital) - 1
        
        returns = portfolio_history_df['portfolio_value'].pct_change().dropna()
        sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std() if returns.std() != 0 else 0
        
        # Max Drawdown
        rolling_max = portfolio_history_df['portfolio_value'].cummax()
        daily_drawdown = portfolio_history_df['portfolio_value'] / rolling_max - 1.0
        max_drawdown = daily_drawdown.min()

        # Win/Loss Rate
        wins = sum(1 for t in self.trades if t['type'] == 'SELL' and t['price'] > self._get_last_buy_price(t['date']))
        losses = len([t for t in self.trades if t['type'] == 'SELL']) - wins
        win_rate = wins / (wins + losses) if (wins + losses) > 0 else 0

        return {
            "Total Return": f"{total_return:.2%}",
            "Sharpe Ratio": f"{sharpe_ratio:.2f}",
            "Max Drawdown": f"{max_drawdown:.2%}",
            "Win Rate": f"{win_rate:.2%}",
            "Total Trades": len([t for t in self.trades if t['type'] == 'SELL']),
            "Final Portfolio Value": f"${final_value:,.2f}"
        }

    def _get_last_buy_price(self, sell_date):
        # Helper to find the price of the corresponding buy trade
        buy_trades = [t for t in self.trades if t['date'] < sell_date and t['type'] == 'BUY']
        return buy_trades[-1]['price'] if buy_trades else 0 
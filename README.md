# Algorithmic Trading Bot (MVP)

## Overview

This project is an extensible algorithmic trading bot designed for sandbox (paper) trading, data-driven strategies, and backtesting. It is modular and ready for future integration with real brokerage APIs.

## Phase 1: Core Bot

- Data fetcher for historical and live data (Yahoo Finance)
- Simple Moving Average (SMA) crossover strategy
- Sandbox paper trading (simulated broker)
- CLI to configure parameters (capital, assets, etc.)

## Folder Structure

```
trading_bot/
│
├── data_fetcher/
│   ├── market_data.py
│
├── strategies/
│   ├── sma_crossover.py
│
├── broker/
│   ├── sandbox_broker.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run the bot: `python main.py`

## Future Phases

- News & sentiment analysis
- Backtesting engine
- Brokerage API integration
- Web dashboard

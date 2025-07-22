import subprocess
import itertools

# Define parameter ranges
symbols = ['AAPL', 'MSFT', 'GOOG']
capitals = [10000]
short_windows = [2, 5, 10]
long_windows = [15, 20, 30]
stop_loss_pcts = [0.02, 0.03]
momentum_windows = [3, 5]
momentum_thresholds = [0.01, 0.015]

results = []

for symbol, capital, short_window, long_window, stop_loss_pct, momentum_window, momentum_threshold in itertools.product(
    symbols, capitals, short_windows, long_windows, stop_loss_pcts, momentum_windows, momentum_thresholds):
    cmd = [
        'python', 'main.py', 'trade',
        '--symbol', symbol,
        '--capital', str(capital),
        '--short_window', str(short_window),
        '--long_window', str(long_window),
        '--stop_loss_pct', str(stop_loss_pct),
        '--momentum_window', str(momentum_window),
        '--momentum_threshold', str(momentum_threshold)
    ]
    print(f"Running: {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    output = proc.stdout
    print(output)
    results.append({
        'symbol': symbol,
        'capital': capital,
        'short_window': short_window,
        'long_window': long_window,
        'stop_loss_pct': stop_loss_pct,
        'momentum_window': momentum_window,
        'momentum_threshold': momentum_threshold,
        'output': output
    })

# Optionally, save results to a file for analysis
with open('trade_test_results.txt', 'w') as f:
    for r in results:
        f.write(f"{r['symbol']} {r['capital']} {r['short_window']} {r['long_window']} {r['stop_loss_pct']} {r['momentum_window']} {r['momentum_threshold']}\n")
        f.write(r['output'])
        f.write("\n---\n")

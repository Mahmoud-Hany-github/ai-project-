import backtrader as bt
import datetime
# Create a simple strategy
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt}, {txt}')

    def next(self):
        self.log(f'Close: {self.datas[0].close[0]}')

# Initialize the backtesting engine
cerebro = bt.Cerebro()

# Load sample data
data = bt.feeds.YahooFinanceData(dataname='AAPL', fromdate=datetime(2020, 1, 1), todate=datetime(2023, 1, 1))
cerebro.adddata(data)

# Add the strategy
cerebro.addstrategy(TestStrategy)

# Run the backtest
cerebro.run()

# Plot results
cerebro.plot()

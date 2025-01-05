import backtrader as bt
import yfinance as yf

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        """Log messages with timestamps."""
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt}, {txt}')

    def next(self):
        # Log closing price for each time step
        self.log(f'Close: {self.datas[0].close[0]}')

        # Example: Buy if the closing price drops below a threshold
        if self.datas[0].close[0] < self.datas[0].close[-1]:
            self.log(f'BUY ORDER TRIGGERED: {self.datas[0].close[0]}')
            self.buy()

        # Example: Sell if the closing price rises above a threshold
        elif self.datas[0].close[0] > self.datas[0].close[-1]:
            self.log(f'SELL ORDER TRIGGERED: {self.datas[0].close[0]}')
            self.sell()


# Download data
data = yf.download("AAPL", start="2020-01-01", end="2023-01-01")
data.to_csv("AAPL.csv")  # Save data to a CSV file

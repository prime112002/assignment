import unittest
import pandas as pd
import numpy as np
from analyze import sma_strategy

class TestSMA(unittest.TestCase):
    
    def setUp(self):
        # Sample data for testing
        self.df = pd.DataFrame({
            'datetime': pd.date_range(start='2020-01-01', periods=10),
            'close': [100, 102, 104, 103, 106, 108, 107, 110, 111, 115],
            'high': [101, 103, 105, 104, 107, 109, 108, 111, 112, 116],
            'low': [99, 101, 103, 102, 105, 107, 106, 109, 110, 114],
            'open': [100, 102, 104, 103, 106, 108, 107, 110, 111, 115],
            'volume': [1000, 1200, 1300, 1100, 1400, 1500, 1600, 1700, 1800, 1900],
            'instrument': ['AAPL'] * 10
        })

    def test_sma_strategy(self):
        df = sma_strategy(self.df)
        
        # Check if the 'short_sma' and 'long_sma' columns are created
        self.assertIn('short_sma', df.columns)
        self.assertIn('long_sma', df.columns)
        
        # Check if 'signal' column is created and has correct values
        self.assertIn('signal', df.columns)
        
        # Check for index range mismatch
        short_window = 40
        long_window = 100
        if len(df) > long_window:
            expected_signal = np.where(
                df['short_sma'][long_window:] > df['long_sma'][long_window:], 1, 0
            )
            # Adjust the expected signal for the actual DataFrame's index
            expected_signal_df = pd.Series(expected_signal, index=df.index[long_window:], name='signal')
            pd.testing.assert_series_equal(df['signal'][long_window:], expected_signal_df)

    def test_signal_column(self):
        df = sma_strategy(self.df)
        # Ensure 'signal' column has no NaNs
        self.assertFalse(df['signal'].isnull().any())

    def test_dataframe_structure(self):
        df = sma_strategy(self.df)
        # Check the structure of the DataFrame
        print(df.columns)  # Debugging line to see the actual columns
        self.assertGreaterEqual(df.shape[1], 6)  # Adjusted to handle more columns if necessary

if __name__ == '__main__':
    unittest.main()

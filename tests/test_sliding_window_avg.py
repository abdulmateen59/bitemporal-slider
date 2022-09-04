from datetime import datetime
from unittest import mock
from unittest import TestCase

import pandas as pd

from src.sliding_window_avg import SlidingWindowAvg


class TestSlidingWindowAvg(TestCase):
    data_path: str = 'data/input.csv'

    def __init__(self, *args, **kwargs):
        super(TestSlidingWindowAvg, self).__init__(*args, **kwargs)
        self._slider = SlidingWindowAvg(self.data_path)

    def test_compute_avg(self):
        # Average Test 01
        initial_start = '2001-01-03'
        end = '2001-01-05'
        system_time = '2001-01-06'
        sliding_steps = 3
        sliding_delta = 1
        df = self._slider.compute_avg(initial_start, end, system_time, sliding_steps, sliding_delta)
        assert float(df.data) == 3.0

        # Average Test 02
        initial_start = '2001-01-01'
        end = '2001-01-06'
        system_time = '2001-01-07'
        sliding_steps = 4
        df = self._slider.compute_avg(initial_start, end, system_time, sliding_steps, sliding_delta)
        assert float(df.data) == 2.575

        # Test where delta is 0
        sliding_delta = 0
        with self.assertRaises(ValueError):
            self._slider.compute_avg(initial_start, end, system_time, sliding_steps, sliding_delta)

        # Test where sliding_steps is 0
        sliding_delta, sliding_steps = 1, 0
        with self.assertRaises(ValueError):
            self._slider.compute_avg(initial_start, end, system_time, sliding_steps, sliding_delta)

        # window initial date is greater than end
        initial_start, end = '2001-01-06', '2001-01-01'
        sliding_delta, sliding_steps = 1, 3
        with self.assertRaises(ValueError):
            self._slider.compute_avg(initial_start, end, system_time, sliding_steps, sliding_delta)

        # system time is less than window
        initial_start, end = '2001-01-03', '2001-01-05'
        system_time = '2001-01-02'
        with self.assertRaises(ValueError):
            self._slider.compute_avg(initial_start, end, system_time, sliding_steps, sliding_delta)

    def test_write_results(self):
        df = pd.DataFrame.from_dict({'system': [datetime(2001, 1, 7)],
                                     'valid': [datetime(2001, 1, 5)],
                                     'data': [3.0]})

        with mock.patch("pandas.DataFrame.to_csv") as to_csv_mock:
            self._slider.write_results(df, sliding_delta=1, sliding_steps=3, path='')
            to_csv_mock.assert_called()

from datetime import datetime
from datetime import timedelta
from unittest import TestCase

from src import ColumnName
from src.bitemporal_moving_average import BitemporalMovingAverage
from src.bitemporal_slider import BitemporalSlider
from src.reader_writer import read_data


class TestSlidingWindowAvg(TestCase):
    data = read_data(filename='input.csv', path='data/')

    def test_compute_avg(self):

        expected_averages = [1.0, 1.5, 1.5, 3.0, 3.6]
        actual_results = BitemporalMovingAverage(self.data, '2001-01-03', 3, 1)
        for result, average in zip(actual_results, expected_averages):
            self.assertEqual(average, result[2])

        result = BitemporalMovingAverage(self.data, '2001-01-07', 2, 1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][2], 4.0)
        self.assertEqual(result[0][0], '2001-01-07')

        result = BitemporalMovingAverage(self.data, '2001-01-03', 1, 0)
        self.assertEqual(result[0][0], '2001-01-03')
        self.assertEqual(result[0][2], 0.0)

    def _test_bitemporal_slider(self, system_date, sliding_window, sliding_delta):

        for provided_date, win_end, slided_data in BitemporalSlider(system=self.data[ColumnName.SYSTEM.value],
                                                                    valid=self.data[ColumnName.VALID.value],
                                                                    data=self.data[ColumnName.DATA.value],
                                                                    window_size=sliding_window,
                                                                    delta=sliding_delta,
                                                                    sys=system_date):
            self.assertEqual(provided_date.strftime('%Y-%m-%d'), system_date)
            self.assertEqual(win_end, datetime.strptime(system_date, '%Y-%m-%d').date() - timedelta(days=sliding_delta))
            self.assertLessEqual(len(slided_data), sliding_window)
            system_date = str(datetime.strptime(system_date, '%Y-%m-%d').date() + timedelta(days=1))

    def test_bitemporal_slider(self):

        param_input = [('2001-01-03', 1, 1),
                       ('2001-01-03', 3, 1),
                       ('2001-01-03', 2, 3),
                       ('2001-01-03', 1, 0),
                       ('2001-01-03', 9, 9),
                       ('2001-01-07', 1, 1),
                       ('2001-01-07', 1, 0)]
        for element in param_input:
            self._test_bitemporal_slider(element[0], element[1], element[2])

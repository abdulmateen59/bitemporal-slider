import itertools
from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import Iterable

from more_itertools import locate


class BitemporalSlider:
    """
    Slides over the bitemporal time series.

    """

    def _dateparser(x): return datetime.strptime(
        x, '%Y-%m-%d').date()  # TODO: E731 violated

    @staticmethod
    def get_lagged_dates(current_date: date,
                         period: int,
                         delta: int) -> list[date]:
        """
        Generates previous dates using current date period(sliding_steps) and delta(sliding_delta).

        :param current_date: Current date (system date)
        :param period: Window size
        :param delta: Delay in number of days

        :return: window with all dates
        """

        if (period <= 0) or (delta < 0):
            raise RuntimeError("Sliding steps and delta cannot be negative...")
        start = current_date - timedelta(days=delta)
        return [start - timedelta(days=day) for day in reversed(range(period))]

    @classmethod
    def preprocess(cls,
                   system: list[str],
                   valid: list[str],
                   data: list[str]) -> tuple[list[date], list[date], list[float]]:
        """
        Type cast list of strings to list of dates and floats
        """
        return list(map(cls._dateparser, valid)), list(map(cls._dateparser, system)), list(map(float, data))

    def __new__(cls,
                system: list[str],
                valid: list[str],
                data: list[str],
                window_size: int,
                delta: int,
                sys: str) -> Iterable[tuple[date, date, dict[date, float]]]:
        """
        Extracts the window for each system value based on the sliding steps and sliding delta

        ** Time Complexity **
            The algorithm has a time complexity of O(n) + O(m^5) -> O(n + m^5), n represents the sequence series and m
            represents the window size. For complexity details, see the comment to the right of the code.
        ** Space Complexity **
            The algorithm generates one result for each system date, i.e. it does not store all values in memory,
            but generates them on the fly. However, in order to store all values in the memory, O(N) is going to be the
            space complexity.

        :param system: system dates
        :param valid:  valid dates
        :param data: Numeric values
        :param window_size: Sliding window size
        :param delta: Number of delayed days
        :param sys: Given system date

        :returns: Iterable, A tuple with system_date, window_end_date and a dict with all rolled date value pairs
        """

        system_date: date = cls._dateparser(sys)
        valid_seq, system_seq, data_seq = cls.preprocess(
            system=system, valid=valid, data=data)

        while system_date <= system_seq[-1]:  # O(n)
            window_dates: list[date] = BitemporalSlider.get_lagged_dates(
                current_date=system_date,
                period=window_size,
                delta=delta)  # O(m) -> m represents the window
            filtered_dates: set[date] = set(window_dates).intersection(
                valid_seq)  # O(min(m, n)) -> O(m)
            filtered_date_idx: list[int | None] = []
            for x in filtered_dates:  # O(m^2)
                index_pos_list = list(locate(valid_seq, lambda a: a == x))
                filtered_date_idx.extend(
                    index for index in index_pos_list if system_date >= system_seq[index])

            out = {element[1]: element[2]
                   for i, (index, element) in itertools.product(filtered_date_idx,
                                                                enumerate(zip(system_seq, valid_seq, data_seq)))
                   if i == index}  # O(m)
            yield system_date, window_dates[-1], dict(zip(out.keys(), out.values()))
            system_date = system_date + timedelta(days=1)

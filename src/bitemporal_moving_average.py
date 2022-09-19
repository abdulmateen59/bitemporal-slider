from bitemporal_slider import BitemporalSlider
from src import ColumnName


class BitemporalMovingAverage:

    @staticmethod
    def mean(values: list[float]):
        """
        Calculates the average value of the given list.

        :param values: Data

        :return: Average value
        """
        return round(sum(values) / len(values), 2) if values else 0.0

    def __new__(cls,
                dataset: dict[str, list[str]],
                system_date: str,
                sliding_steps: int = 3,
                sliding_delta: int = 1) -> list[list[str | float]]:
        """


        :param dataset:
        :param system_date:
        :param sliding_steps
        :param sliding_delta:

        :return
        """

        return [[str(provided_date), str(win_end), BitemporalMovingAverage.mean(list(slided_data.values()))]
                for provided_date, win_end, slided_data in BitemporalSlider(system=dataset[ColumnName.SYSTEM.value],
                                                                            valid=dataset[ColumnName.VALID.value],
                                                                            data=dataset[ColumnName.DATA.value],
                                                                            window_size=sliding_steps,
                                                                            delta=sliding_delta,
                                                                            sys=system_date)]

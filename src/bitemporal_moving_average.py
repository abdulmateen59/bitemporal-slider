from src import ColumnName
from src.bitemporal_slider import BitemporalSlider


class BitemporalMovingAverage:
    """
    Calculates the mean value over moving data
    """

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
        Takes the data set, derives the slider and calculates the average using the parameters

        :param dataset: complete data with system, value and data
        :param system_date: system date
        :param sliding_steps: Number of sliding steps
        :param sliding_delta: Sliding delta

        :return: List of lists where first element is the system_date, second window end date and late the mean
        """

        return [[str(provided_date), str(win_end), BitemporalMovingAverage.mean(list(slided_data.values()))]
                for provided_date, win_end, slided_data in BitemporalSlider(system=dataset[ColumnName.SYSTEM.value],
                                                                            valid=dataset[ColumnName.VALID.value],
                                                                            data=dataset[ColumnName.DATA.value],
                                                                            window_size=sliding_steps,
                                                                            delta=sliding_delta,
                                                                            sys=system_date)]

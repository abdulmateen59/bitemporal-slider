import os
from datetime import date
from datetime import datetime
from datetime import timedelta
from enum import Enum
from pathlib import Path

import pandas as pd
from loguru import logger
from pandas import DataFrame

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class ColumnName(Enum):
    SYSTEM = 'system'
    VALID = 'valid'
    DATA = 'data'


class SlidingWindowAvg:
    """
    The bitemporal data model associates two time intervals with each record - system time and valid time.
    This class implements a method for calculating the average for bitemporal data by specifying the start,
    end, system time, number of sliding steps and time delta.
    """

    def __init__(self, file_path: str) -> None:
        """
        Loads csv file.

        :param file_path: Path from where the file will be loaded
        :return: None
        """
        try:
            self._df: DataFrame = pd.read_csv(filepath_or_buffer=Path(file_path),
                                              parse_dates=[ColumnName.SYSTEM.value,
                                                           ColumnName.VALID.value],
                                              date_parser=self.convert_str_to_date)
            logger.info('CSV loaded successfully')
        except Exception as E:
            logger.error(E)
            raise E

    def __repr__(self):
        return repr(self._df)

    @staticmethod
    def convert_str_to_date(timestamp: str) -> date:
        """
        Converts str to a date with the format 2021-12-31
        """
        return datetime.strptime(timestamp, '%Y-%m-%d').date()

    def compute_avg(self,
                    initial_start: str,
                    end: str,
                    system_time: str,
                    sliding_steps: int,
                    sliding_delta: int) -> DataFrame:
        """
        Computes the rolling average based on the provided input.

        :param initial_start: Window start time
        :param end: Window end time
        :param system_time: Exact system time for which the average is required
        :param sliding_steps: Number of records to roll to computer average
        :param sliding_delta: Number of days to be delayed

        :return: Dataframe with a single row where data is the average

        --------------------------------------------------------------
        TIME COMPLEXITY: O(n^2)
                        The algorithms for index maintenance usually have a linear complexity with respect to the
                        number of events/rows, in the implementation there is a `loc` operation that has
                        the complexity of O(n), in addition there is also rolling operation that is also a linear
                        operation, and it sums up the complexity to O(n^2).

        SPACE COMPLEXITY: 0(2N)
                        Assuming the memory required to load the data is N. A new data frame is also created
                        in the implementation, this memory could also be a constant N, and this sums the space
                        complexity to O(2N).

        Q: Can you think of an implementation with smaller space and/or time complexity?
        A: Yes, instead of creating a new data frame, manipulate the current data frame with the `Shift` operation and
           then perform a rolling operation, both time and space complexity will be reduced.

        Q: Do you see any edge cases that need be handled explicitly?
        A: Take a look at the test cases.
        """

        if ((self.convert_str_to_date(end) < self.convert_str_to_date(initial_start)) or
                (sliding_steps <= 0) or
                (sliding_delta <= 0) or
                (self.convert_str_to_date(system_time) < self.convert_str_to_date(end))):
            logger.error("Please make sure that the start date is smaller than the end date and sliding_steps / "
                         "sliding_delta are greater than 0.")
            raise ValueError("Incorrect arguments")

        # Getting the delayed date
        system_delta = self.convert_str_to_date(system_time) - timedelta(days=sliding_delta)

        logger.info(f'Lagged date: {system_delta}')

        # Extract the rows that are in the time duration
        df = self._df.loc[(self._df.valid.between(initial_start, end)) &
                          (self._df.system <= str(system_delta + timedelta(days=1)))].copy()

        # Dropping the replicates and keep the latest one
        df = df.drop_duplicates(subset=[ColumnName.VALID.value], keep='last')
        logger.info(f'Number of transactions: {len(df)}')
        # logger.info(f'\n {df}')

        # Computing average based on the sliding steps
        df.data = df.data.rolling(sliding_steps, min_periods=0).mean()

        # Keeping the last row
        df = df[-1:].reset_index(drop=True)

        # Updating system time and delta based on the given input
        df.loc[0, [ColumnName.SYSTEM.value, ColumnName.VALID.value]] = [system_time, system_delta]
        return df

    def write_results(self,
                      data: DataFrame,
                      sliding_steps: int,
                      sliding_delta: int,
                      path: str) -> None:
        """
        Writes data to a csv file, if the file with the same sliding_steps and sliding_delta already exists,
        the data will be appended to the existing file.

        :param data: Dataframe to be written
        :param sliding_steps: Number of sliding steps
        :param sliding_delta: Number of days to be delayed
        :param path: path where the data will be saved
        :return: None
        """

        logger.info(f'\n {data}')
        file_path = os.path.join(path, f'output_steps-{sliding_steps}_delta-{sliding_delta}.csv')
        if os.path.exists(file_path):
            existing_df = pd.read_csv(file_path,
                                      parse_dates=[ColumnName.SYSTEM.value, ColumnName.VALID.value],
                                      date_parser=self.convert_str_to_date)
            output = pd.concat([existing_df.astype({'valid': 'str'}), data.astype({'valid': 'str'})],
                               axis=0).drop_duplicates()
            output.to_csv(file_path, index=False)
        else:
            logger.info(f'Creating new file {file_path}')
            data.to_csv(file_path, index=False)

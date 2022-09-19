import argparse

from src.bitemporal_moving_average import BitemporalMovingAverage
from src.reader_writer import read_data
from src.reader_writer import write_result

from src import logger


def run():
    """
    Entry point.
    """

    parser = argparse.ArgumentParser(description="Provide initial start, end, system time, "
                                                 "delta and number of sliding steps")
    parser.add_argument("--initial_start", type=str,
                        required=True, help="Initial valid start date")
    parser.add_argument("--end", type=str, required=True,
                        help="End valid date")
    parser.add_argument("--system_time", type=str,
                        required=True, help="System time")
    parser.add_argument("--sliding_steps", type=int, required=True,
                        help="Number of sliding steps for which the average will be calculated")
    parser.add_argument("--sliding_delta", type=int,
                        required=True, help="Number of lag days")
    parser.add_argument("--path", type=str,
                        default="data/input.csv", help="Number of lag days")

    args = parser.parse_args()

    data = read_data(filename="data/input.csv", path="")
    results = BitemporalMovingAverage(
        data, args.system_time, args.sliding_steps, args.sliding_delta)
    write_result(output=results,
                 filename=f"output_{args.system_time}_{args.sliding_steps}_{args.sliding_delta}",
                 path="data/")

    for result in results:
        logger.info(result)


if __name__ == "__main__":
    run()

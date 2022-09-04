import argparse

from src.sliding_window_avg import SlidingWindowAvg


def run():
    """
    Entry point.
    """

    parser = argparse.ArgumentParser(description='Provide initial start, end, system time,'
                                                 'delta and number of sliding steps')

    parser.add_argument('--initial_start',
                        type=str,
                        required=True,
                        help='Initial valid start date')
    parser.add_argument('--end',
                        type=str,
                        required=True,
                        help='End valid date')
    parser.add_argument('--system_time',
                        type=str,
                        required=True,
                        help='System time')
    parser.add_argument('--sliding_steps',
                        type=int,
                        required=True,
                        help='Number of sliding steps for which the average will be calculated')
    parser.add_argument('--sliding_delta',
                        type=int,
                        required=True,
                        help='Number of lag days')
    parser.add_argument('--path',
                        type=str,
                        default="data/input.csv",
                        help='Number of lag days')

    args = parser.parse_args()

    # Using same data provided in example
    slider = SlidingWindowAvg(file_path=args.path)
    result = slider.compute_avg(initial_start=args.initial_start,
                                end=args.   end,
                                system_time=args.system_time,
                                sliding_steps=args.sliding_steps,
                                sliding_delta=args.sliding_delta)
    slider.write_results(data=result,
                         sliding_steps=args.sliding_steps,
                         sliding_delta=args.sliding_delta,
                         path='data')


if __name__ == "__main__":
    run()

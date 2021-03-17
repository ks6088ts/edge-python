import argparse
import time

import drivers

DEVICE_NAMES = [
    "mock",
    "imu0",
    # add device names here
]


def get_driver(name):  ## pylint: disable=redefined-outer-name
    if name == DEVICE_NAMES[0]:
        return drivers.Mock()
    if name == DEVICE_NAMES[1]:
        return drivers.Imu0()
    # add drivers here
    raise ValueError(f'Invalid name "{name}" was specified')


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dt", help="sampling interval[sec]", type=float, default=1.0)
    parser.add_argument(
        "--name",
        help="driver name(mock)",
        type=str,
        default="mock",
        choices=DEVICE_NAMES,
    )
    args = parser.parse_args()
    return args.dt, args.name


if __name__ == "__main__":

    dt, name = parse_arguments()
    driver = get_driver(name)
    driver.initialize()

    try:
        while True:
            t, states = driver.get_states()
            print(f"{t:6.6f},{','.join(map(str,states))}")
            time.sleep(dt)
    finally:
        driver.finalize()

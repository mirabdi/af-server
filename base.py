import argparse
import os
import pathlib

import zmq


class DistributionBase:
    def __init__(
            self,
            af2_out_path,
            port,
    ):
        self.path = pathlib.Path(af2_out_path).expanduser()
        self.port = port
        self.ctx = zmq.Context()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dir",
        help="Path to folder with AlphaFold outputs",
        nargs='?',
        default=os.getcwd(),
        type=str,
    )
    args = parser.parse_args()
    return args

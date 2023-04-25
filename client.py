import configparser
import time
import zmq
import json
import sys
import os
from base import DistributionBase, get_args
import platform

DIR = os.getcwd()


import platform
computer_id = platform.node()


class ConsumerClient(DistributionBase):
    def __init__(
            self,
            af2_out_path,
            port,
            server_ip,
    ):
        super().__init__(af2_out_path, port)
        self.server_ip = server_ip

        self.sock = self.ctx.socket(zmq.REQ)
        self.sock.connect(f'tcp://{self.server_ip}:{self.port}')

    def request_4ever(self):
        while True:
            time.sleep(0.5)
            self.request_one()

    def request_one(self):
        self.sock.send_string(computer_id)
        seq = self.sock.recv_string()
        # sys.stdout.write("")
        sys.stdout.write(seq)
        # print(f"Received sequence {seq}")
        


if __name__ == '__main__':
    args = get_args()

    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    client = ConsumerClient(
        args.dir,
        port=cfg['DEFAULT']['PORT'],
        server_ip=cfg['DEFAULT']['SERV_IP'],
    )
    # print("Requesting one: ")
    client.request_one()

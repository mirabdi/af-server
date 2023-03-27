import datetime
import configparser
import pickle
import os
import pathlib
from tqdm import tqdm
from typing import List
import glob
import zmq
from pathlib import Path
from base import DistributionBase, get_args
import msgpack
import numpy as np




def make_list(path, folder_name):
    main_paths =  ["mTag", "PafA"]
    remaining = []
    print("Starting to prepare the list")
    for curr in main_paths:
        current_path = path.parent
        current_path = current_path.joinpath(f"AF/{curr}/{folder_name}")
        print(f"Looking for folders containing fasta files in AF/{curr}") 
        for seqpath in tqdm(current_path.iterdir()):
            fasta_files = glob.glob(os.path.join(seqpath, '*.fasta'))
            if len(fasta_files) != 0:
                remaining.append(seqpath.parts[-1])
        print(f"AF/{curr} completed!")
    remaining = sorted(list(set(remaining)))
    # print(remaining)
    return remaining 


class DistributionServer(DistributionBase):
    def __init__(
            self,
            af2_out_path,
            port
    ):
        print("Initializing the seqence distribution server ...")
        super().__init__(af2_out_path, port)
        
        self.sock = self.ctx.socket(zmq.REP)
        self.sock.bind(f'tcp://*:{self.port}')

        # self.results_path = self.path.joinpath('AF2_results')
        self.folder_name = "fasta"
        self.remaining = make_list(self.path, self.folder_name)


        print(f"There are {len(self.remaining)} sequences to fold. Ready to serve.")

    def serve_4ever(self):
        print("Serving forever ...")
        while True:
            if len(self.remaining) == 0:
                print("NO SEQUENCE LEFT! ---")
                break
            msg = self.sock.recv()
            print(msg)
            seqs = []
            for _ in range(100):
                if len(self.remaining) == 0:
                    break
                seqs.append(self.remaining.pop())
            
            print(f"[{datetime.datetime.now()}]"
                  f" ===== Got request, sending {len(seqs)} sequences")
            print(f"[{datetime.datetime.now()}]"
                  f" ===== Seqs remaining to fold: {len(self.remaining)}")
            message = msgpack.dumps(seqs)
            self.sock.send(message)
            
            

if __name__ == '__main__':
    args = get_args()

    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    serv = DistributionServer(
        af2_out_path=args.dir,
        port=cfg['DEFAULT']['PORT']
    )
    serv.serve_4ever()

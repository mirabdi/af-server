import datetime
import configparser
import logging
import pickle
import os
import pathlib
from tqdm import tqdm
from typing import List
import glob
import zmq
from pathlib import Path
from base import DistributionBase, get_args
import numpy as np




def make_list():
    base = Path("/data/Protein/AFsequences/")
    main_paths =  ["PDB", "mTag", "PafA", "GFP"]
    remaining = []
    print("Starting to prepare the list")
    for curr in main_paths:
        current_path = base.joinpath(f"{curr}/AFpred")
        print(f"Looking for folders containing not containing pdb files in AFsequences/{curr}/AFpred") 
        for seqpath in tqdm(current_path.iterdir()):
            pdb_files = sorted(seqpath.glob('*.pdb'))
            if len(pdb_files) == 0:
                remaining.append(f"/{curr}/AFpred/{seqpath.name}")
                print(remaining[-1])
        print(f"Finished adding paths from AF/{curr}!")
    # remaining = sorted(list(set(remaining)))
    return remaining[::-1] 


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

        self.remaining = make_list()

        self.count = 0
        self.make_list_every = 500

        print(f"There are {len(self.remaining)} sequences to fold. Ready to serve.")
        # print(self.remaining)
    def serve_4ever(self):
        print("Serving forever ...")
        while True:
            if len(self.remaining) == 0:
                print("NO SEQUENCE LEFT! ---")
                break
            msg = self.sock.recv()
            seq = str(self.remaining.pop())
            self.sock.send_string(seq)
            
            self.count += 1
            self.load_extra_seq()

    def load_extra_seq(self):
        seq_path = Path('../extra_seq.txt')
        if seq_path.exists():
            extra = [l.strip('\n') for l in open(seq_path)]
            os.remove(seq_path)
            self.remaining.extend(extra)

    def log_client_request(self, msg, seq):
        with open('log/server.log', 'a') as o:
            o.write(f"{msg}\n")
            o.write(f"[{datetime.datetime.now()} ===== Got request, sending the sequence: {seq}\n")
            o.write(f"[{datetime.datetime.now()}] ===== Seqs remaining to fold: {len(self.remaining)}\n")

    def log_extra_seq(self, extra):
        with open('log/server.log', 'a') as o:
            o.write(f"EXTRA SEQ FOUND: {len(extra)} sequences appended to the front of the queue\n")


if __name__ == '__main__':
    args = get_args()

    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    serv = DistributionServer(
        af2_out_path=args.dir,
        port=cfg['DEFAULT']['PORT']
    )
    serv.serve_4ever()

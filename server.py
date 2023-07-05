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



### Creates the initial list of sequences to be served.
### Run once when starting the server.
def make_list():
    base = Path("/data/Protein/AFsequences/")
    main_paths =  ["ddG"]
    remaining = []
    print("Starting to prepare the list")
    for curr in main_paths:
        current_path = base.joinpath(f"{curr}/AFpred")
        print(f"Looking for folders containing not containing pdb files in AFsequences/{curr}/AFpred") 
        for seqpath in tqdm(current_path.iterdir()):
            # Sort the files so that they are presented in a predictable manner
            pdb_files = sorted(seqpath.glob('*.pdb'))
            if len(pdb_files) == 0:
                remaining.append(f"/{curr}/AFpred/{seqpath.name}")
        print(f"Finished adding paths from AF/{curr}!")
    # Present the list in reverse order, since sequences are drawn from the end of the list
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
            print(f"[{datetime.datetime.now()} ===== Got request, sending the sequence: {seq}")
            print(f"[{datetime.datetime.now()}] ===== Seqs remaining to fold: {len(self.remaining)}\n")

            self.log_client_request(msg, seq)          
            self.count += 1
            self.load_extra_seq()


    def load_extra_seq(self):
        seq_path = Path('../extra_seq.txt')
        if seq_path.exists():
            extra = [l.strip('\n') for l in open(seq_path, 'r')]
            os.remove(seq_path)
            self.remaining.extend(extra)
            self.log_extra_seq(extra)


    def reload_seq_list(self):
        seq_path = Path('../reload_seq_list.txt')
        if seq_path.exists():
            seq_list = [l.strip('\n') for l in open(seq_path, 'r')]
            os.remove(seq_path)
            # Present the list in reverse order, since sequences are drawn from the end of the list
            self.remaining = seq_list[::-1]
            self.log_reload_seq(extra)


    def log_client_request(self, msg, seq):
        with open('log/server.log', 'a') as o:
            o.write(f"{msg}\n")
            o.write(f"[{datetime.datetime.now()} ===== Got request, sending the sequence: {seq}\n")
            o.write(f"[{datetime.datetime.now()}] ===== Seqs remaining to fold: {len(self.remaining)}\n")


    def log_extra_seq(self, extra):
        with open('log/server.log', 'a') as o:
            o.write(f"EXTRA SEQ FOUND: {len(extra)} sequences appended to the front of the queue\n")


    def log_reload_seq(self, seq_list):
        with open('log/server.log', 'a') as o:
            o.write(f"SEQ LIST RELOADED: {len(seq_list)} sequences found\n")



if __name__ == '__main__':
    args = get_args()

    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    serv = DistributionServer(
        af2_out_path=args.dir,
        port=cfg['DEFAULT']['PORT']
    )
    serv.serve_4ever()

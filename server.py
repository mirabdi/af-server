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




def make_list(path):
    main_paths =  ["PDB", "mTag", "PafA", "GFP"]
    remaining = []
    print("Starting to prepare the list")
    for curr in main_paths:
        current_path = path.parent
        current_path = current_path.joinpath(f"././AFsequences/{curr}/AFpred")
        print(f"Looking for folders containing not containing pdb files in AFsequences/{curr}/AFpred") 
        for seqpath in tqdm(current_path.iterdir()):
            pdb_files = glob.glob(os.path.join(seqpath, '*.pdb'))
            if len(pdb_files) == 0:
                remaining.append(f"/{curr}/AFpred/"+str(seqpath.parts[-1]))
        print(f"AF/{curr} completed!")
    # remaining = sorted(list(set(remaining)))
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

        self.remaining = make_list(self.path)


        print(f"There are {len(self.remaining)} sequences to fold. Ready to serve.")
        # print(self.remaining)
    def serve_4ever(self):
        print("Serving forever ...")
        while True:
            if len(self.remaining) == 0:
                print("NO SEQUENCE LEFT! ---")
                break
            msg = self.sock.recv()
            print(msg)
            seq = str(self.remaining.pop())
            print(f"[{datetime.datetime.now()}]"
                  f" ===== Got request, sending the sequence: {seq}")
            print(f"[{datetime.datetime.now()}]"
                  f" ===== Seqs remaining to fold: {len(self.remaining)}")
            self.sock.send_string(seq)
            
            

if __name__ == '__main__':
    args = get_args()

    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    serv = DistributionServer(
        af2_out_path=args.dir,
        port=cfg['DEFAULT']['PORT']
    )
    serv.serve_4ever()

#!/usr/bin/bash

source /home/kstk/code/alphafold/af2-run-scripts/seq-distribution/venv_zmq/bin/activate

python3 server.py /home/kstk/code/alphafold/nfs_mount/inputs/Pairs

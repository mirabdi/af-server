source $PWD/Scripts/activate
while true; do
    sequence=$(python client.py)
    echo $sequence
    rsync -a -e 'ssh -p 50000' amirbek@10.70.10.47:/home/protein/Protein/AFsequences/$sequence .
    
done
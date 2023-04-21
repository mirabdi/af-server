source "$PWD"/Scripts/activate
seqdir='..............'
while [ -n $seqdir ] ; do
    seqdir=$(python client.py)
    # seqdir format (mTag/AFpred/1111111111111) or 
    echo $seqdir
    if [ -n $seqdir ] ; then
       echo "Running colabfold_batch on " $seqdir
       echo "Running colabfold_batch on " $seqdir >> log/client.log
       colabfold_batch --amber --use-gpu-relax --num-seeds 5 --num-recycle 6  ../AFsequences/$seqdir ../AFsequences/$seqdir 2>> log/client.log
    fi    
    # rsync -a -e 'ssh -p 50000'  ../AFsequences/$seqdir  amirbek@10.70.10.47:/home/protein/Protein/AFsequences/$seqdir
done

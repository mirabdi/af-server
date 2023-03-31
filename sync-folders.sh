#while true; do 
#   for f in $(find ../AFsequences -maxdepth 3 -mindepth 3 -type d -mmin -60); do
#      echo $f
      rsync -a --include "*/" --include="*pdb" --include="*json" --exclude="*" -e 'ssh -p 50000'  ../AFsequences amirbek@10.70.10.47:/data/Protein
#   done
#   sleep 1800
#done

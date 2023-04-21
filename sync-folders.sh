#while true; do 
#   for f in $(find ../AFsequences -maxdepth 3 -mindepth 3 -type d -mmin -60); do
#      echo $f
      src="/home/main/dev/AFsequences"
      dest="amirbek@10.70.10.47:/data/Protein"
      rsync -arv -P --include "*/" --include="*pdb" --include="*json" --exclude="*" -e 'ssh -p 50000'  $src $dest
#   done
#   sleep 1800
done

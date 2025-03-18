# !/bin/bash

export path_prefix="./data/MAXDIFF"
for file in "$path_prefix"/cluster/*; do
  if [ -f "$file" ]; then
    wrong_file=$(head -n 1 "$file" | tr -d '[:space:]')
    correct_file=$(sed -n '2p' "$file" | tr -d '[:space:]')
    export wrong_id=$(basename $wrong_file .c)
    mkdir -p "$path_prefix"/bpex_result/"$wrong_id"
    echo running python3 Bpex feedback "$path_prefix"/input.txt "$path_prefix"/"$wrong_file" "$path_prefix"/"$correct_file" 
    python3 Bpex feedback "$path_prefix"/input.txt "$path_prefix"/"$wrong_file" "$path_prefix"/"$correct_file" | tee  "$path_prefix"/bpex_result/"$wrong_id"/feedback.txt
    python3 process.py tmp/res.json
    rm -r  "$path_prefix"/bpex_result/"$wrong_id"/tmp
    mv tmp/ "$path_prefix"/bpex_result/"$wrong_id"
  fi
done

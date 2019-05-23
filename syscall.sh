#!/bin/bash
set -o nounset

grep '^[0-9]' $1 | \
while read nr abi name entry; do
  if [[ "$abi" == "common" ]] || [[  "$abi" == "64" ]]; then
    echo "const int NR_${name} = ${nr};"
  fi
done

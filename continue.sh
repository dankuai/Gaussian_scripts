#!/bin/bash

## This code is to prepare the automatic Gaussian input files for continuing the previous sims. 
for filename in *.chk; do 
  filename=${filename%.chk}
##  rm $filename
  echo '%RWF='$(pwd)'/'$filename'.rwf' > "$filename".com
  echo '%NoSave' >> "$filename".com
  echo '%Chk='$(pwd)'/'$filename'.chk' >> "$filename".com
  echo '#P Restart' >> "$filename".com
  echo '' >> "$filename".com
  echo '' >> "$filename".com
done


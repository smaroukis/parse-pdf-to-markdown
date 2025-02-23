#!/bin/bash

INPUT="./6002-02-Notes-W01-MOSFET-SCS-Amplifier.pdf"
IMGDIR="./sandbox/z_attachments"
OUTPUT="./sandbox"

./clean.sh
python app.py -i $INPUT -d $IMGDIR -o $OUTPUT --quality 80

# Example with viewsize changed
# python app.py -i $INPUT -d $IMGDIR -o $OUTPUT --quality 60 --viewsize 350
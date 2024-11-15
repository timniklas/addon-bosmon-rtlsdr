#!/bin/bash

CONFIG_PATH=/data/options.json

FREQUENCY=$(jq --raw-output '.frequency // empty' $CONFIG_PATH)
URL=$(jq --raw-output '.bosmon_url // empty' $CONFIG_PATH)
ENDPOINT=$(jq --raw-output '.bosmon_endpoint // empty' $CONFIG_PATH)
USERNAME=$(jq --raw-output '.bosmon_username // empty' $CONFIG_PATH)
PASSWORD=$(jq --raw-output '.bosmon_password // empty' $CONFIG_PATH)

rtl_fm -d 0 -f $FREQUENCY -s 22050 -g 100 | multimon-ng -t raw -a POCSAG1200 /dev/stdin | python3 /app/bosmon.py $URL $ENDPOINT $USERNAME $PASSWORD
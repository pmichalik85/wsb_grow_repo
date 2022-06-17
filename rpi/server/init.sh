#!/bin/sh
DIR="venv"
sudo kill -9 $(sudo lsof -t -i:50051)
if [ -d "$DIR" ]; then
  echo "create venv"
  python3 -m venv venv 1>&2
fi
echo "activate venv";
. venv/bin/activate; 1>&2
echo "install python dependencies"
pip3 install -r requirements.txt 1>&2
echo "start app"
python3 server/grow.py
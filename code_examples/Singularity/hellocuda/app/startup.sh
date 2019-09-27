#!/bin/bash
echo executing nvidia-smihellocuda > /service/status.html
echo not done yet > /service/result.txt
(command -v nvidia-smi  >/dev/null 2>&1 && nvidia-smi || echo "failed to start nvidia-smi") 2>&1 | tee /service/result.txt
echo executing nvidia-smihellocuda > /service/status.html
/app/hellocuda  2>&1 | tee -a /service/result.txt
echo done

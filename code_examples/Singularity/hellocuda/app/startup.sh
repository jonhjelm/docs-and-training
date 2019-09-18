#!/bin/bash
echo executing hellocuda > /service/status.html
echo not done yet > /service/result.txt
/app/hellocuda  2>&1 | tee /service/result.txt
nvidia-smi 2>&1 >> /service/result.txt
echo done

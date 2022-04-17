# /bin/bash
set -e
gcc -std=c99  -shared -Wall -Werror -fPIC our_clib.c -o our_clib.so
python3 call_clib.py 
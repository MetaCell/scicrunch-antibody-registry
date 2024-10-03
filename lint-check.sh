#!/bin/bash
# Run autopep8 with --diff and capture the output

exclude='**/openapi/**/*,./cloud-harness/**/*,**/models/**,**/migrations/*,**/test/test*controller.py'
rules='E1,E2,E3,W,E4,E7,E502'

diff_output=$(python -m autopep8 --select=$rules --recursive --diff --exclude $exclude .)
# Check if the output is non-empty
if [ -n "$diff_output" ]; then
    printf "%s\n" "$diff_output"
    echo "Code style issues found in the above files. To fix you can run: "
    echo "autopep8 --select=$rules  --recursive --in-place --exclude $exclude ."
    exit 1
fi
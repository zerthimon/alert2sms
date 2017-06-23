#!/bin/bash
set -e

if [ "$1" = 'alert2sms.py' ]; then
    exec ./alert2sms.py
fi

exec "$@"

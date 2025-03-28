#!/bin/bash

#exec gunicorn --graceful-timeout 30 --max-requests 100000 --max-requests-jitter 2000 -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 protal:app
exec uvicorn portal:app --host 0.0.0.0 --port 8000 --timeout-keep-alive 60 --use-colors

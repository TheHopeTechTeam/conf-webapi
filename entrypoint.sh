#!/bin/bash

exec gunicorn --graceful-timeout 30 --max-requests 100000 --max-requests-jitter 2000 -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 protal:app

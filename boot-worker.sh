#!/bin/bash
source .venv/bin/activate
exec rq worker --url $REDIS_URL myflaskapp-tasks

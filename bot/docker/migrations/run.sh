#!/bin/bash

echo "Apply migrations"
/usr/local/bin/dbmate -d "/code/migrations" -e "DATABASE_URL" up

sleep 1m
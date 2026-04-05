#!/bin/bash
echo "Starting Compass with local user:"
# uid(id -u ${USER}) gid(id -g ${USER}) docker compose up
$uid 1000
$gid 1000
"uid($uid) gid($gid) docker compose up"
# $uid=(id -u ${USER})
# echo($uid)
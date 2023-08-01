#!/bin/bash
docker stop xyz_tts
docker rm xyz_tts

docker build -t xyz_tts .
docker run -v /etc/localtime:/etc/localtime:ro --name xyz_tts -p 2020:2020 \
-d xyz_tts



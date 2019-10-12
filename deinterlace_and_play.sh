#!/bin/bash
rm -f "$1.deint.mkv";
./deinterlace.sh "$1";
mpv -vo gl "$1.deint.mkv" -speed 0.033 --osd-msg3='${estimated-frame-number} / ${estimated-frame-count}' --osd-level=3
#mpv -vo opengl --vf scale=1176:1248 --sws-scaler=point "$1.deint.mkv" -speed 0.033 --osd-msg3='${estimated-frame-number} / ${estimated-frame-count}' --osd-level=3

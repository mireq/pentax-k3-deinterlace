#!/bin/bash
export VIDEO_SOURCE=$1
#vspipe ./deinterlace.vpy - --y4m|ffmpeg -i IMGP6645.MOV -c:v libx264 -x264opts "keyint=60" -preset slow -crf 13 -r 60000/1001 $1.deint.mkv
#vspipe ./deinterlace.vpy - --y4m|ffmpeg -i - -c:v libx264 -x264opts "keyint=60" -preset slow -crf 15 -r 60000/1001 -pix_fmt yuvj420p $1.deint.mkv
vspipe ./deinterlace.vpy - --y4m|ffmpeg -i - -c:v libx264 -preset slow -crf 15 -r 60000/1001 -pix_fmt yuvj420p $1.deint.mkv

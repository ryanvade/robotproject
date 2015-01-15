__author__ = 'ryanvade'
from subprocess import Popen
from os import system

web_directory = '/var/nginx/www/live.m3u8'
ts_directory = 'live/%08d.ts'
video_device = '/dev/video0'
ffmpeg_output_location = '/dev/null'
#command = ['ffmpeg', '-f', 'video4linux2', '-y', '-r', '4', '-i', '/dev/video0', '-vf', '-vframes ','20', '-vcodec', 'mpeg4', 'out.mp4']
command = ['ffmpeg', '-i live.h264', '-f s16le', '-i ', video_device, '-r:a 48000',  '-ac 2', '-c:v copy', '-c:a aac',
           '-b:a 128k', '-map 0:0', '-map 1:0', '-f segment', '-segment_list ', web_directory,'-segment_time 8',
           '-segment_format mpegts', '-segment_list_size 80', '-segment_list_flags live', ' -segment_wrap 10',
           '-segment_list_type m3u8', '-strict', '-2', ts_directory, '< ', ffmpeg_output_location]

Popen(command)
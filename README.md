# Blastoisoidal curve using DFT

I wanted to draw a Blastoise but I have no skills with a pen, so I made a program to draw a curve.
This program has no other purpose, is FAR from optimised or generic and was made for fun. The result can be seen on [youtube](http://youtube.com)
If you want to run it, just clone the project, install gizeh an run it with python 3.x. 
To turn a bunch of png file to a MP4 video you can use ffmpeg. See bellow for the full command.

```
pip3 install gizeh
python3 dft_draw.py
[wait until the program is finished]
cd temp
ffmpeg -framerate 60 -start_number 0 -i "%05d.png" -s:v 1920x1080 -c:v libx264 -profile:v high -crf 17 -pix_fmt yuv420p blastoisoidal.mp4
```

"""
Copyright (c) 2019 Léo Rousseau

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import math
from math import pi as PI
import gizeh as gz
import blastoise


DT = PI*2
SW = 1


def dft(values):
	N = len(values)
	res = []
	for k in range(N):
		number = sum([complex(val * math.cos((2*PI * k * n)/N), -val * math.sin((2*PI * k * n)/N)) for n, val in enumerate(values)])/N
		res.append({
			'number': number,
			'frequency': k,
			'amplitude': math.sqrt(number.real**2 + number.imag**2),
			'phase': math.atan2(number.imag, number.real),
			})
	return res

def epicycles(x, y, dftvals, surface, rotation, time):
	for value in dftvals:
		prevx = x
		prevy = y
		x += (value['amplitude'] * math.cos(value['frequency'] * time + value['phase'] + rotation))
		y += (value['amplitude'] * math.sin(value['frequency'] * time + value['phase'] + rotation))

		circle = gz.circle(value['amplitude'], xy=(prevx, prevy), fill=(0, 0, 0, 0), stroke=(1, 1, 1, 1), stroke_width=SW)
		line = gz.polyline(points=[(prevx, prevy), (x,y)], stroke_width=SW, stroke=(1, 1, 1, 1), fill=(0, 0, 0, 0))
		circle.draw(surface)
		line.draw(surface)

	return x,y

def draw_path(path, surface, fill=(0, 0, 0, 0)):
	poly = gz.polyline(points=path, stroke_width=3 * SW, stroke=(0, 0, 1, 1), fill=(0, 0, 0, 0))
	poly.draw(surface)


def main():
	width = 1920
	height = 1080

	print('... OK\ncomputing dft ....', end = '')

	dft_values = dft(blastoise.points)

	print('... OK\nsorting dft for x ....', end = '')

	dft_values = sorted(dft_values, key = lambda x: x['amplitude'], reverse=True)

	print('... OK')

	path = []
	xpos = width / 2, height / 2
	size = len(dft_values)
	dt = DT / size
	time = 0
	i = 0

	print('rendering frames ... (%d/%d)'%(0,size+1))

	while time <= DT:
		surface = gz.Surface(width, height, bg_color=(0,0,0))
		xx = epicycles(*xpos,dft_values,surface, -PI, time)
		path = [xx] + path
		draw_path(path, surface)
		frame_id = './temp/%05d.png'%i
		surface.write_to_png(frame_id)
		time += dt
		i += 1
		if not i % ((size + 1) // 10):
			print('rendering frames ... (%d/%d) %.2f%%'%(i,size + 1, i * 100 / (size + 1)))
	surface = gz.Surface(width, height, bg_color=(0, 0, 0))
	draw_path(path, surface, fill=(0, 0, 1, 1))
	i += 1
	surface.write_to_png('./temp/%05d.png'%i)


if __name__ == '__main__':
	main()
# Image downsampling converter

Inspired by [2bit](http://2bit.neocities.org/)

Usage: `python3 2bit.py infile.png [outfile.png] [bits] [--per-color] [--dither dither_value]`

dither\_value can be like `50%`, `50` or `.5`

Warning: Will probably turn transparency black

You can change the number of bits for different results. 1 would be just black and white, while 8 would be the original image in greyscale.

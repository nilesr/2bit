# Image downsampling converter

Inspired by [2bit](http://2bit.neocities.org/)

Usage: `python3 2bit.py infile.png [outfile.png] [bits] [--per-color] [--dither dither_value] [--non-random-dither num_pixels]`

You can change the number of bits for different results. 1 would be just black and white, while 8 would be the original image in greyscale.

dither\_value can be like `50%`, `50`, `.5` or `auto`

Note that using `--non-random-dither` without a dither argument will attempt to guess what dither percentage you want based on the number of bits

The best number for num\_pixels varies with the image. In general, the height of the image modulo num\_pixels + 1 should not equal zero. Experiment with it. Using `auto` will try to guess a good value such that you don't get horizontal bars, but it's not very good at it.

Warning: Will probably turn transparency black

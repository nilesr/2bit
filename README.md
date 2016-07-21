# Image downsampling converter

Inspired by [2bit](http://2bit.neocities.org/)

Usage: `python3 2bit.py infile.png [outfile.png] [bits] [--per-color] [--dither dither_value] [--non-random-dither num_pixels]`

dither\_value can be like `50%`, `50` or `.5`

Note that using `--non-random-dither` without a dither argument will attempt to guess what dither percentage you want based on the number of bits

The best number for num\_pixels is usually 7, but it should ideally be coprime with the height of the image

Warning: Will probably turn transparency black

You can change the number of bits for different results. 1 would be just black and white, while 8 would be the original image in greyscale.

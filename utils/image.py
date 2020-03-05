from itertools import chain
from itertools import filterfalse
from typing import Tuple

from PIL import Image

from utils import pixel_gen


def put_data(zip_obj, pixels, is_finish):
    buffer = []
    for obj in zip_obj:
        buffer.append(obj[0])
        pixel = obj[0][1]
        for i, e in enumerate(obj[1]):
            if e == '0' and pixel[i] % 2 != 0:
                pixel[i] -= 1
            elif e == '1' and pixel[i] % 2 == 0:
                pixel[i] += 1
    if not is_finish:
        if pixel[i + 1] % 2 != 0:
            pixel[i + 1] -= 1
    else:
        if pixel[i + 1] % 2 == 0:
            pixel[i + 1] += 1
    for coords, pixel in buffer:
        pixels[coords] = tuple(pixel)


def encode(img: Image, data: Tuple[str]) -> Image:
    if len(img.getdata()) < len(data) * 3:
        raise ValueError('Image to small to hide this data.')

    pixels = img.load()
    p = pixel_gen(img.size, pixels)
    data_length = len(data)

    for x, e in enumerate(data, start=1):
        zip_obj = list(zip(list(next(p) for _ in range(3)), list(e[i:i + 3] for i in range(0, len(e), 3))))
        put_data(zip_obj, pixels, x == data_length)

    img.save('new.png', 'png')


def fetch(data, buffer):
    s = []
    for e, pixel in enumerate(filterfalse(lambda x: x == 0, chain(*data))):
        if pixel % 2 == 0:
            s.append('0')
        else:
            s.append('1')
    last = s.pop()
    buffer.append(''.join(s))
    return last == '0'


def decode(i):
    pixels = i.load()
    p = pixel_gen(i.size, pixels)
    c = True
    buffer = []
    while c:
        c = fetch([next(p)[1] for _ in range(3)], buffer)
    return buffer

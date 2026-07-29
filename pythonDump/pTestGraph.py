import struct
import zlib
from typing import BinaryIO, List, Tuple
import re

'\\nRevision: (\d+)\\n'

Pixel = Tuple[int, int, int]
Image = List[List[Pixel]]

BLACK_PIXEL: Pixel = (0, 0, 0)
WHITE_PIXEL: Pixel = (255, 255, 255)
GREY_PIXEL: Pixel = (100,100,100)

HEADER = b'\x89PNG\r\n\x1A\n'
def generate_graph(width_used: int, height_used: int,list_y_used) -> Image:
    out = []
    for i in range(height_used):
        row = []
        for j in range(width_used):
            if i < height_used - list_y_used[j]:
                row.append(GREY_PIXEL)
            else:
                row.append(WHITE_PIXEL)
        out.append(row)
    return out


def get_checksum(chunk_type: bytes, data: bytes) -> int:
    checksum = zlib.crc32(chunk_type)
    checksum = zlib.crc32(data, checksum)
    return checksum


def chunk(out: BinaryIO, chunk_type: bytes, data: bytes) -> None:
    out.write(struct.pack('>I', len(data)))
    out.write(chunk_type)
    out.write(data)

    checksum = get_checksum(chunk_type, data)
    out.write(struct.pack('>I', checksum))


def make_ihdr(width: int, height: int, bit_depth: int, color_type: int) -> bytes:
    return struct.pack('>2I5B', width, height, bit_depth, color_type, 0, 0, 0)


def encode_data(img: Image) -> List[int]:
    ret = []

    for row in img:
        ret.append(0)

        color_values = [
            color_value
            for pixel in row
            for color_value in pixel
        ]
        ret.extend(color_values)

    return ret


def compress_data(data: List[int]) -> bytes:
    data_bytes = bytearray(data)
    return zlib.compress(data_bytes)


def make_idat(img: Image) -> bytes:
    encoded_data = encode_data(img)
    compressed_data = compress_data(encoded_data)
    return compressed_data


def dump_png(out: BinaryIO, img: Image) -> None:
    out.write(HEADER)  # start by writing the header

    assert len(img) > 0  # assume we were not given empty image data
    width = len(img[0])
    height = len(img)
    bit_depth = 8  # bits per pixel
    color_type = 2  # pixel is RGB triple

    ihdr_data = make_ihdr(width, height, bit_depth, color_type)
    chunk(out, b'IHDR', ihdr_data)

    compressed_data = make_idat(img)
    chunk(out, b'IDAT', data=compressed_data)

    chunk(out, b'IEND', data=b'')


def save_png(img: Image, filename: str) -> None:
    with open(filename, 'wb') as out:
        dump_png(out, img)

def f_graph_from_text(str_file):
	list_y_axis = []
	file = open(str_file, 'r')
	lines = file.readlines()
	for i in range(len(lines)):
		if str(lines[i]).startswith('7'):
			list_y_axis_values=re.findall("\d+\.\d+",lines[i][6:])
			for i in list_y_axis_values:
				i = float(i)
				list_y_axis.append(i)
	min_y_axis = min(j for j in list_y_axis)
	list_y_axis_x1 = [int(i-min_y_axis) for i in list_y_axis]
	list_y_axis_x10 = [min(int((i-min_y_axis)*10),500) for i in list_y_axis]
	list_y_axis_x100 = [min(int((i-min_y_axis)*100),500) for i in list_y_axis]
	width1 = len(list_y_axis_x1)
	height1 = max(list_y_axis_x1)
	width2 = len(list_y_axis_x10)
	height2 = max(list_y_axis_x10)
	width3 = len(list_y_axis_x100)
	height3 = max(list_y_axis_x100)
	img1 = generate_graph(width1, height1, list_y_axis_x1)
	img2 = generate_graph(width2, height2, list_y_axis_x10)
	img3 = generate_graph(width3, height3, list_y_axis_x100)
	save_png(img1, str_file[:-4]+'_x1.png')
	save_png(img2, str_file[:-4]+'_x10.png')
	save_png(img3, str_file[:-4]+'_x100.png')
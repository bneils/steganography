from PIL import Image
from math import ceil


def steganography_encode(im, message):
	"""Encode a utf-8 message within an image"""

	message = bytes(message, encoding='utf-8')
	assert len(message) <= im.width * im.height // 3, "insufficient space to encode image"
	assert im.mode == "RGB"

	# flatten the pixel array to a list of channels (RGBRGBRGB...)
	channels = [c for px in im.getdata() for c in px]

	for i in range(len(message)):
		cur_bit = 8
		bit = 1 << 8
		for j in range(i * 9, i * 9 + 8):
			bit >>= 1;
			cur_bit -= 1;

			# strip the channel of its little endian, replace it with the message's bit
			channels[j] = channels[j] & ~1 | (message[i] & bit) >> cur_bit

	return Image.frombytes('RGB', im.size, bytes(channels))


def steganography_decode(modified, original=None):
	"""Decodes a message within a steganographic image.
	If original is None, it will attempt to decode the entire image, regardless of size."""

	channels = [c for px in modified.getdata() for c in px]
	message = ""
	
	end = len(channels)

	if original:
		orig_channels = [c for px in original.getdata() for c in px]
		for i in range(len(orig_channels)):
			if orig_channels[i] != channels[i]:
				end = ceil(i / 9) * 9

	for i in range(0, end, 9):
		cur_char = 0
		cur_bit = 8

		for j in range(i, i + 8):
			cur_bit -= 1
			cur_char |= (channels[j] & 1) << cur_bit
		
		message += chr(cur_char)

	return message


if __name__ == '__main__':
	
	resp = input("Would you like to encode or decode? ").lower()
	while resp != 'encode' and resp != 'decode':
		resp = input("Would you like to encode or decode? ").lower()

	if resp == 'encode':
		im = Image.open(input("Image file path: "))
		
		with open(input("Message file path: ")) as f:
			message = f.read()

		steganography_encode(im, message).save('result.png')
	else:
		modified_fp = input("Modified image: ")
		original_fp = input("Original image (enter if none): ")

		message = steganography_decode(Image.open(modified_fp), Image.open(original_fp) if original_fp else None)
		with open('message.txt', 'w', encoding='utf-8') as f:
			f.write(message)

	input()
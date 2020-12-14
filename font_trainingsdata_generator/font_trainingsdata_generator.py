import os
import sys
import string
import random
import argparse

from PIL import Image, ImageFont, ImageDraw, ImageFilter
import numpy as np
from tqdm import tqdm


class ImageModifier:
    def __init__(self, rotate=False, blur=False, noise=False):
        self.filter_functions = []

        if rotate:
            self.filter_functions.append(self.rotate)
        if blur:
            self.filter_functions.append(self.blur)
        if noise:
            self.filter_functions.append(self.noise)

    def modify(self, img):
        if self.filter_functions:
            modified_img = img.copy()

            # Picks a random number of filter functions as a list
            random_filters = random.sample(population=self.filter_functions,
                                                    k=random.randint(0, len(self.filter_functions)))

            for random_filter in random_filters:
                modified_img = random_filter(modified_img)

            return modified_img

        return img

    @staticmethod
    def noise(img):
        img_array = np.asarray(img)

        noisey = img_array + np.random.normal(0.0, 100, img_array.shape)
        noise_img = Image.fromarray(np.uint8(np.clip(noisey, 0, 255)))

        return noise_img

    @staticmethod
    def blur(img):
        blur_img = img.filter(ImageFilter.GaussianBlur(radius=3))

        return blur_img

    @staticmethod
    def rotate(img):
        rotate_img = img.rotate(random.randint(0, 359), expand=True, resample=Image.BICUBIC, fillcolor="white")

        return rotate_img


def random_string_generator(count=1, length=1):
    for _ in range(count):
        yield ''.join(random.choices(string.ascii_letters, k=length))


def text_to_image(text, font_file, font_size, margin):
    font = ImageFont.truetype(font=font_file, size=font_size)
    size = list(font.getsize(text=text))
    font_width, font_height = size

    if margin:
        margin = [margin, margin]
    else:
        margin = [0, 0]

    size = (size[0] + 2 * margin[0], size[1] + 2 * margin[1])

    img_width, img_height = size
    center_pos = ((img_width - font_width) / 2, (img_height - font_height) / 2)

    img = Image.new('L', size, "white")
    draw = ImageDraw.Draw(img)
    draw.text(xy=center_pos, text=text, font=font, fill="black")

    filename = f"{os.path.splitext(os.path.basename(font_file))[0]}_{text.replace(' ', '')}.png"

    return img, filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random text (A-Z & a-z) as images.")
    parser.add_argument("-f", "--fonts", type=str, required=True, help="Directory containing all font files.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Directory where all images will be saved.")
    parser.add_argument("-c", "--count", type=int, required=True, help="Number of images for each font.")
    parser.add_argument("-l", "--length", type=int, required=True, help="Length of text.")
    parser.add_argument("-fs", "--fontsize", type=int, default=50, required=False, help="Font size in pt.")
    parser.add_argument("-m", "--margin", type=int, required=False, help="Margin around text.")
    parser.add_argument("-s", "--silent", action="store_true", help="Won't prompt user input.")

    # Image modifier arguments
    parser.add_argument("-n", "--noise", action="store_true", help="Add noise filter.")
    parser.add_argument("-b", "--blur", action="store_true", help="Add blur filter.")
    parser.add_argument("-r", "--rotate", action="store_true", help="Add rotation.")

    args = parser.parse_args()

    if not os.path.isdir(args.fonts):
        raise NotADirectoryError(args.fonts)

    if not os.path.isdir(args.output):
        raise NotADirectoryError(args.output)

    if len(os.listdir(args.output)) != 0 and not args.silent:
        user_input = input(f"Output directory '{args.output}' is not empty. Still want to continue? (y/n) ")
        if user_input.lower() != "y":
            print("Quitting...")
            sys.exit(0)

    image_modifier = ImageModifier(noise=args.noise, blur=args.blur, rotate=args.rotate)

    with tqdm(total=(len(os.listdir(args.fonts)) * args.count)) as pbar:
        for file in os.listdir(args.fonts):
            for random_string in random_string_generator(args.count, args.length):
                image, imagename = text_to_image(random_string, os.path.join(args.fonts, file), args.fontsize, args.margin)

                image = image_modifier.modify(image)

                image.save(os.path.join(args.output, imagename))
                pbar.update(1)

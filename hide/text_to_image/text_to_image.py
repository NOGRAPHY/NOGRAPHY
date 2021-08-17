from PIL import Image, ImageDraw, ImageFont
import os
import copy

def fit_text(letters_and_fonts, color, font_size, image_width, character_spacing, line_spacing, margin_left_right, margin_top_bottom):
    estimated_height = estimate_image_height(
            letters_and_fonts, font_size, line_spacing, image_width, margin_top_bottom)
    image = Image.new("RGB", (image_width, estimated_height), 'white')
    
    width = image.size[0] - margin_left_right * 2
    draw = ImageDraw.Draw(image)
    path, _ = os.path.split(os.path.abspath(__file__))
    measure_font = ImageFont.truetype(
        os.path.join(path, '../assets', '0.ttf'), font_size)

    lines = break_into_lines(letters_and_fonts, width,
                             measure_font, font_size, character_spacing, line_spacing, draw)
    # based on https://stackoverflow.com/questions/58041361/break-long-drawn-text-to-multiple-lines-with-pillow
    height = sum(l[2] for l in lines)
    if height > image.size[1]:
        raise ValueError("text doesn't fit")

    y = (image.size[1] - height) // 2
    for t, w, h in lines:
        x = margin_left_right
        for letter, font in t:
            draw.text((x, y), letter, font=font, fill=color)
            x = x + draw.textsize(letter, font=font)[0] + character_spacing
        y += h
    return image

def break_into_lines(letters_and_fonts, width, measure_font, font_size, character_spacing, line_spacing, draw):
    if not letters_and_fonts:
        return
    words = split_into_words(letters_and_fonts)
    lines = []
    line = []
    current_line_width = 0
    for word in words:
        required_width, _ = draw.textsize(
            ''.join([letter_and_font[0] for letter_and_font in word]), font=measure_font)
        required_width += len(word) * character_spacing
        if current_line_width + required_width <= width:
            current_line_width += required_width
            line.extend(word)
        else:
            lines.append((copy.copy(line), required_width,
                         font_size * line_spacing))
            line.clear()
            line.extend(word)
            current_line_width = required_width
    lines.append((copy.copy(line), required_width, font_size * line_spacing))
    return lines


def split_into_words(letters_and_fonts):
    words = []
    word = []

    for letter_and_font in letters_and_fonts:
        word.append(letter_and_font)
        if letter_and_font[0] == " ":
            words.append(copy.copy(word))
            word.clear()
    words.append(word)
    return words

def estimate_image_height(letters_and_fonts, font_size, line_spacing, image_width, margin):
    letters_per_line = (image_width - 2 * margin / font_size) // 45
    number_of_lines = len(letters_and_fonts) // letters_per_line
    height_without_margin = line_spacing * font_size * number_of_lines
    return int(height_without_margin) + 2 * margin
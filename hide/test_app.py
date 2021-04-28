from app import secret_fits_in_placeholder, get_letters_and_fonts
from PIL import ImageFont

def test_secret_fits_in_placeholder():
    assert True == secret_fits_in_placeholder('abc', 'abcdefghij')
    assert False == secret_fits_in_placeholder('abcde', 'abcdefghij')
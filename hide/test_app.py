from app import secret_fits_in_dummy, get_letters_and_fonts
from PIL import ImageFont

def test_secret_fits_in_dummy():
    assert True == secret_fits_in_dummy('abc', 'abcdefghij')
    assert False == secret_fits_in_dummy('abcde', 'abcdefghij')
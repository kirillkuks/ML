from typing import List

import cv2
import pytesseract
import re


class TextRecognizer:
    def __init__(self) -> None:
        pytesseract.pytesseract.tesseract_cmd = 'D:/Kuksenko/Tesseract/tesseract.exe'

    def extract_product_info(self, img_path: str):
        img = cv2.imread(img_path)
        text = pytesseract.image_to_string(img, lang='rus')
        
        print(text)
        key_words = self._contain_key_word(text)
        print(f'{img_path}: {key_words}')


    def _contain_key_word(self, text: str) -> List:
        new_str = ' ' + text + ' '
        key_words = []

        if re.search(r'\bжир[ыао]в?\b', new_str, re.IGNORECASE):
            key_words.append('жиры')

        if re.search(r'\bуглевод[ыо]в?\b', new_str, re.IGNORECASE):
            key_words.append('углеводы')
        
        if re.search(r'\bбелк[аио]в?\b', new_str, re.IGNORECASE):
            key_words.append('белки')
        
        return key_words

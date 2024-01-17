from typing import List

import cv2
import pytesseract
import re


def is_float(value):
  if value is None:
      return False
  try:
      float(value)
      return True
  except:
      return False


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
        new_str = ' ' + text.replace('\n', ' ') + ' '
        key_words = []

        product_info = {
            'protein' : None,
            'fats': None,
            'carbohydrates': None,
            'calorie_content': None,
            'sugar' : None,
            'expiration_date': None
        }

        def get_from_math(_match):
            s = _match[0].replace('—',' ')
            s = s.replace('-', ' ')
            found = s.split(' ')

            fff = [fs for fs in found if len(fs) > 0]
            if (len(fff) < 2):
                return None
            fff[1] = fff[1].replace(',', '.')

            if is_float(fff[1]):
                return float(fff[1])


        if re.search(r'\bжир[ыао]в?\b', new_str, re.IGNORECASE):
            key_words.append('жиры')

            match = re.search(r'\bжир[ыао]в?\s?[—-]?[0123456789]+[,\s.]?[0123456789]+\s?[г]?', new_str, re.IGNORECASE)
            if match:
                product_info['fats'] = get_from_math(match)


        if re.search(r'\bуглевод[ыо]в?\b', new_str, re.IGNORECASE):
            key_words.append('углеводы')

            match = re.search(r'углевод[ыо]в?\s?[—-]?\s?[0123456789]+[,.\s]?[0123456789]+\s?[г]?', new_str, re.IGNORECASE)
            if match:
                product_info['carbohydrates'] = get_from_math(match)
            
        
        if re.search(r'\bбелк[аио]в?\b', new_str, re.IGNORECASE):
            key_words.append('белки')

            match = re.search(r'белк[аио]в?\s?[—-]?\s?[0123456789]+[,.\s]?[0123456789]+\s?[г]?', new_str, re.IGNORECASE)
            if match:
                product_info['protein'] = get_from_math(match)

        if re.search(r'\bккал\b', new_str, re.IGNORECASE):
            key_words.append('ккал')

            match = re.search(r'[0123456789]+\s?ккал', new_str, re.IGNORECASE)
            if match:
                found = [fs for fs in match[0].split(' ') if len(fs) > 0]
                if len(found) > 1:
                    if is_float(found[0]):
                        product_info['calorie_content'] = int(float(found[0]))

        if re.search(r'срок годности', new_str, re.IGNORECASE) or re.search(r'годен', new_str, re.IGNORECASE):
            key_words.append('срок годности')

            match = re.search(r'годен\s?[0-9]+\s?[а-яА-Я]+', new_str, re.IGNORECASE)
            if match:
                print('!!!!!!!!!!!!!!!!!!!!!!')
                print(match[0])
                print('!!!!!!!!!!!!!!!!!!!!!!')

            else:
                match = re.search(r'срок годности\s?[:-—]?\s[0-9]+\s[а-яА-Я]+', new_str, re.IGNORECASE)
                if match:
                    print('!!!!!!!!!!!!!!!!!!!!!!')
                    print(match[0])
                    print('!!!!!!!!!!!!!!!!!!!!!!')

        if re.search(r'сахар[а]?', new_str, re.IGNORECASE) or re.search(r'сахароз[аы]', new_str, re.IGNORECASE):
            key_words.append('сахар')
        
        print(product_info)
        return key_words

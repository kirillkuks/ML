from typing import List

import cv2
import pytesseract
import re

from dataset import Product

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
        
        #print(text)
        #print(f'{img_path}: {key_words}')

        return self._contain_key_word(text)


    def _contain_key_word(self, text: str) -> List:
        new_str = ' ' + text.replace('\n', ' ') + ' '
        key_words = []

        product_info = {
            'product': None,
            'protein' : 0.0,
            'fats': 0.0,
            'carbohydrates': 0.0,
            'calorie_content': None,
            'sugar' : 0.0,
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

            match = re.search(r'жир[ыао]в?\s?[—-]?\s?[0123456789]+[,.\s]?[0123456789]+\s?[г]?', new_str, re.IGNORECASE)
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
            num = None
            time_metric = None
            if match:
                found = match[0].split(' ')
                if len(found) > 2:
                    num = found[1]
                    time_metric = found[2]

            else:
                match = re.search(r'срок годности\s?[:-—]?\s[0-9]+\s[а-яА-Я]+', new_str, re.IGNORECASE)
                if match:
                    found = match[0].split(' ')
                    if len(found) > 3:
                        num = found[2]
                        time_metric = found[3]

            if num and time_metric:
                if is_float(num):
                    num = int(float(num))

                    if re.search(r'час', time_metric, re.IGNORECASE):
                        num /= 24

                    product_info['expiration_date'] = num

        if re.search(r'сахар[а]?', new_str, re.IGNORECASE) or re.search(r'сахароз[аы]', new_str, re.IGNORECASE):
            key_words.append('сахар')

            match = re.search(r'сахар[а]?\s?[—-]?\s?[0-9]+[,.\s]?[0-9]+\s?[г]?', new_str, re.IGNORECASE)
            if match:
                product_info['sugar'] = get_from_math(match)

            else:
                match = re.search(r'сахароз[аы]\s?[—-]?\s?[0-9]+[,.\s]?[0-9]+\s?[г]?', new_str, re.IGNORECASE)
                if match:
                    product_info['sugar'] = get_from_math(match)

        if re.search(r'хлеб', new_str, re.IGNORECASE) or re.search(r'хлеб', new_str, re.IGNORECASE):
            product_info['product'] = Product.kBread
        elif re.search(r'молоко', new_str, re.IGNORECASE) or \
                re.search(r'сливки', new_str, re.IGNORECASE) or \
                re.search(r'молочный', new_str, re.IGNORECASE):
            product_info['product'] = Product.kMilk
        elif re.search(r'[йи]огурт', new_str, re.IGNORECASE):
            product_info['product'] = Product.kYogurt
        elif re.search(r'газированный', new_str, re.IGNORECASE):
            product_info['product'] = Product.kSoda
        elif re.search(r'сок[a]?', new_str, re.IGNORECASE) or \
                re.search(r'нектар', new_str, re.IGNORECASE):
            product_info['product'] = Product.kJuice
        
        return product_info

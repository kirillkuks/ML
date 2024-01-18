from typing import Tuple
import pandas as pd
import os

from text_recognition import TextRecognizer
from diet_prediction import DietPredictor
from dataset import get_dataset


kLoadModel = True


def main():
    # DietPredictor.find_opt_params(dataset)
    predictor = DietPredictor()

    if kLoadModel:
        predictor.load_model()
    else:
        dataset = pd.read_csv('dataset/dataset.csv')
        predictor.train1(dataset)
        predictor.save_model()

    product = {
        'product': 'milk',
        'protein' : 3.0,
        'fats': 3.5,
        'carbohydrates': 4.5,
        'calorie_content': 55,
        'sugar' : 0.0,
        'expiration_date': 5
    }

    person = {
        'sex': 'male',
        'age': 55,
        'height': 170,
        'weight': 76,
        'disease': 'acute infectious diseases'
    }

    prediction = predictor.predict(product, person)
    print(f'recommended daily norm - {prediction}')

    # products_dataset_path = 'dataset/'
    # products_imgs = os.listdir(products_dataset_path)
    # text_recognizer = TextRecognizer()

    # # img = 'milk11.jpg'
    # # text_recognizer.extract_product_info(f'{products_dataset_path}{img}')
    # # return

    # for product_img in products_imgs:
    #     if product_img.find('.jpg') > 0:
    #         text_recognizer.extract_product_info(f'{products_dataset_path}{product_img}')
    #         print('################################')
    # return


if __name__ == '__main__':
    main()

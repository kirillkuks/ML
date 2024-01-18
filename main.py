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

    person = {
        'sex': 'male',
        'age': 55,
        'height': 170,
        'weight': 76,
        'disease': 'acute infectious diseases'
    }

    products_dataset_path = 'dataset/'
    text_recognizer = TextRecognizer()

    img = 'milk11.jpg'
    product = text_recognizer.extract_product_info(f'{products_dataset_path}{img}')
    product_name = product['product']
    prediction = predictor.predict(product, person)
    print(f'product info {product}')
    print(f'recommended daily norm for this {product_name} - {prediction}')


    person = {
        'sex': 'female',
        'age': 42,
        'height': 165,
        'weight': 60,
        'disease': 'ulcer'
    }

    img = 'bread12.jpg'
    product = text_recognizer.extract_product_info(f'{products_dataset_path}{img}')
    product_name = product['product']
    prediction = predictor.predict(product, person)
    print(f'product info {product}')
    print(f'recommended daily norm for this {product_name} - {prediction}')


if __name__ == '__main__':
    main()

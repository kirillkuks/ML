from typing import Tuple
import pandas as pd
import os

from text_recognition import TextRecognizer
from diet_prediction import DietPredictor
from dataset import get_dataset


def main():
    # dataset = pd.read_csv('dataset/dataset.csv')

    # # DietPredictor.find_opt_params(dataset)
    # predictor = DietPredictor()
    # predictor.train1(dataset)
    # predictor.save_model()

    products_dataset_path = 'dataset/'
    products_imgs = os.listdir(products_dataset_path)
    text_recognizer = TextRecognizer()

    # img = 'milk11.jpg'
    # text_recognizer.extract_product_info(f'{products_dataset_path}{img}')
    # return

    for product_img in products_imgs:
        if product_img.find('.jpg') > 0:
            text_recognizer.extract_product_info(f'{products_dataset_path}{product_img}')
            print('################################')
    return


if __name__ == '__main__':
    main()

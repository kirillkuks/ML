from typing import Tuple
import pandas as pd

from text_recognition import TextRecognizer
from diet_prediction import DietPredictor
from dataset import get_dataset


def main():
    dataset = pd.read_csv('dataset/dataset.csv')
    predictor = DietPredictor()
    predictor.train(dataset)

    # products_dataset_path = 'dataset/'
    # products_imgs = os.listdir(products_dataset_path)

    # text_recognizer = TextRecognizer()

    # text_recognizer.extract_product_info('dataset/bread10.jpg')
    # return

    # for product_img in products_imgs:
    #     text_recognizer.extract_product_info(f'{products_dataset_path}{product_img}')
    #     print('################################')
    return


if __name__ == '__main__':
    main()

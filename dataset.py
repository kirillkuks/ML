import pandas as pd
import numpy as np


class Disease:
    kUlcer = 'ulcer'
    kConstipation = 'constipation'
    kDiarrhea = 'diarrhea'
    kDiabetes = 'diabetes'
    kInfectious = 'acute infectious diseases'
    kNoDisease = 'no disease'

diseases = [Disease.kUlcer, Disease.kConstipation,  Disease.kDiarrhea,
            Disease.kDiabetes, Disease.kInfectious, Disease.kNoDisease]


class Product:
    kBread = 'bread'
    kMilk = 'milk'
    kYogurt = 'yogurt'
    kJuice = 'juice'
    kSoda = 'soda'

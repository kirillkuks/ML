import pandas as pd
import numpy as np


class Disease:
    kUlcer = 'ulcer'
    kGastritis = 'gastritis'
    kConstipation = 'constipation'
    kDiarrhea = 'diarrhea'
    kLiver = 'bile duct and liver disease'
    kUrolithiasis = 'urolithiasis disease'
    kNephritis = 'nephritis'
    kObesity = 'obesity'
    kDiabetes = 'diabetes'
    kCardiovascular = 'cardiovascular disease'
    kTuberculosis = 'tuberculosis'
    kNervous = 'nervous system disease'
    kInfectious = 'acute infectious diseases'
    kKidney = 'kidney disease'
    kNoDisease = 'no disease'

diseases = [Disease.kUlcer, Disease.kConstipation,  Disease.kDiarrhea,
            Disease.kDiabetes, Disease.kInfectious, Disease.kNoDisease]


class Product:
    kBread = 'bread'
    kMilk = 'milk'
    kYogurt = 'yogurt'
    kJuice = 'juice'
    kSoda = 'soda'


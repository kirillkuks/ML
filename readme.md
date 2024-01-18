# Диеты

## Задача
По описанию продукта и характеристикам человека с болезнью определить
суточную норму продукта в рамках диеты при этом заболевании.

### Вход
Описание продукта (текстовое или фотография), параметры человека и заболевание.

### Выход
Суточная норма продукта (в граммах) в рамках диеты.

## Характеристики продуктов
### Поддерживаемые типы продуктов
* Молоко
* Хлеб
* Йогурт
* Газировка и сок

### Числовые характеристики
* Жиры
* Белки
* Углеводы
* Сахар
* Калорийность
* Максимальный срок годности

## Характеристики человека
### Заболевания
* Язва
* Запоры
* Диарея
* Сахарный диабет
* Острые инфекционные заболевания
* Без заболевания

### Числовые характеристики
* Пол
* Возраст
* Рост
* Вес

## Этапы алгоритма
1. Извлечение текста из изображение (Tesseract)
2. Извлечение числовых характеристик продукта из текста
3. Предсказание дневной нормы распознанного продукта для человека
с указанными параметрами на основе обученной модели градиентного бустинга (CatBoost)

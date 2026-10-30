Шаг 1. Открыть cmd в папке проекта
Шаг 2. Создать .venv

    python -m venv .venv

Шаг 3. Активировать виртуальное окружение

    .venv\Scripts\activate.bat

Шаг 4. Установить зависимости

   pip install -r requirements.txt

Шаг 5. Тесты
    python -m unittest test_my_sort -v

Шаг 6. Линтер
    pylint --rcfile=.pylintrc my_sort.py main.py

Шаг 7. CLI

    python main.py --input nums.txt --numbers --algorithm quick --  output out.txt
    type out.txt

    python main.py --input words.txt --reverse --algorithm tim
    python main.py --visualize 8 --algorithm merge

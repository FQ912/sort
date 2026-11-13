"""Тесты для модуля my_sort."""

import unittest

import my_sort  # pylint: disable=E0401


TEST_NUMBER = [
    [],
    [1],
    [1, 2, 3, 4, 5],
    [0, 0, 0, 55, 55, 60],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    [8, 0, 42, 3, 4, 8, 0, 45, 50, 9999, 7],
    [-5, 0, 9, -999, 874, 35, -4, -5, 0],
    [1, 1, 1],
]


TEST_STR = [
    [],
    ['a'],
    ['a', 'b', 'c', 'd', 'e'],
    ['aa', 'aa', 'aa', 'ab', 'ac', 'b'],
    ['e', 'd', 'c', 'b', 'a'],
    ['abc', 'a', 'foo', 'bar', 'booz', 'baz', 'spam', 'love'],
    ['abc', 'abc', 'abc'],
    [''],
]


class TestSort(unittest.TestCase):
    """Тест-кейс модуля my_sort для всех реализованных алгоритмов."""

    def setUp(self) -> None:
        """Получить список доступных алгоритмов перед каждым тестом."""
        self.algorithms = my_sort.available_algorithms()

    def test_sort_number_increase(self) -> None:
        """Тест сортировки числовых данных по возрастанию (все алгоритмы)."""
        for alg in self.algorithms:
            for data in TEST_NUMBER:
                with self.subTest(algorithm=alg, data=data):
                    self.assertEqual(
                        my_sort.my_sort(data, algorithm=alg),
                        sorted(data),
                        msg=f"Алгоритм {alg} не справился с {data}"
                    )

    def test_sort_number_decrease(self) -> None:
        """Тест сортировки числовых данных по невозрастанию (все алгоритмы)."""
        for alg in self.algorithms:
            for data in TEST_NUMBER:
                with self.subTest(algorithm=alg, data=data):
                    self.assertEqual(
                        my_sort.my_sort(data, reverse=True, algorithm=alg),
                        sorted(data, reverse=True),
                        msg=f"Алгоритм {alg} не справился с {data}"
                    )

    def test_sort_str_increase(self) -> None:
        """Тест сортировки строковых данных по возрастанию (все алгоритмы)."""
        for alg in self.algorithms:
            for data in TEST_STR:
                with self.subTest(algorithm=alg, data=data):
                    self.assertEqual(
                        my_sort.my_sort(data, algorithm=alg),
                        sorted(data),
                        msg=f"Алгоритм {alg} не справился с {data}"
                    )

    def test_sort_str_decrease(self) -> None:
        """Тест сортировки строковых данных по невозрастанию (все алгоритмы)."""
        for alg in self.algorithms:
            for data in TEST_STR:
                with self.subTest(algorithm=alg, data=data):
                    self.assertEqual(
                        my_sort.my_sort(data, reverse=True, algorithm=alg),
                        sorted(data, reverse=True),
                        msg=f"Алгоритм {alg} не справился с {data}"
                    )

    def test_sort_key(self) -> None:
        """Тест параметра key (порядок ключей, независимо от стабильности)."""
        words = ['bbb', 'a', 'cc', 'dddd', 'ee']
        for alg in self.algorithms:
            with self.subTest(algorithm=alg):
                result = my_sort.my_sort(words, key=len, algorithm=alg)
                # 1. Ключи должны идти по неубыванию
                keys = [len(w) for w in result]
                self.assertEqual(
                    keys, sorted(keys),
                    msg=f"Алгоритм {alg}: ключи не по возрастанию"
                )
                # 2. Мультимножество элементов должно совпадать с исходным
                self.assertEqual(
                    sorted(result), sorted(words),
                    msg=f"Алгоритм {alg}: потеряны или изменены элементы"
                )

    def test_sort_cmp(self) -> None:
        """Тест параметра cmp (убывание через cmp, все алгоритмы)."""
        data = [3, 1, 2, 2, 1]
        def desc_cmp(a, b):
            """Сравнение по убыванию."""
            return (b > a) - (b < a)
        expected = sorted(data, reverse=True)
        for alg in self.algorithms:
            with self.subTest(algorithm=alg):
                self.assertEqual(
                    my_sort.my_sort(data, cmp=desc_cmp, algorithm=alg),
                    expected,
                    msg=f"Алгоритм {alg} не справился с cmp"
                )

    def test_returns_new_list(self) -> None:
        """Тест того, что возвращается новый список (исходный не мутируется)."""
        for alg in self.algorithms:
            data = [3, 1, 2]
            original = list(data)
            result = my_sort.my_sort(data, algorithm=alg)
            with self.subTest(algorithm=alg):
                self.assertEqual(data, original,
                                 msg=f"Алгоритм {alg} изменил исходный список")
                self.assertIsNot(result, data,
                                 msg=f"Алгоритм {alg} вернул тот же объект")


if __name__ == '__main__':
    unittest.main()
    

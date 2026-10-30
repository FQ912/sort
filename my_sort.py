"""Модуль сортировки с поддержкой key, cmp, reverse и визуализации.

Реализованы алгоритмы:
    - сортировка слиянием (merge sort)
    - быстрая сортировка (quick sort)
    - плавная (пирамидальная) сортировка (smooth sort)
    - интроспективная сортировка (introsort)
    - Timsort (упрощённая реализация)

Публичный API:
    my_sort(array, reverse=False, key=None, cmp=None) -> list
    visualize_sort(size, algorithm="merge", reverse=False) -> None
    available_algorithms() -> List[str]
"""

import math
import random
from typing import Any, Callable, List, Optional


# ---------------------------------------------------------------------------
# Вспомогательные функции сравнения
# ---------------------------------------------------------------------------


def _compare(a: Any, b: Any,
             key: Optional[Callable[[Any], Any]] = None,
             cmp: Optional[Callable[[Any, Any], int]] = None) -> int:
    """Сравнить два элемента.

    :param a: первый элемент
    :param b: второй элемент
    :param key: функция вычисления ключа
    :param cmp: функция сравнения (имеет приоритет над key)
    :return: <0 если a<b, 0 если равны, >0 если a>b
    """
    if cmp is not None:
        return cmp(a, b)
    if key is not None:
        a, b = key(a), key(b)
    if a < b:
        return -1
    if a > b:
        return 1
    return 0


def _less(a: Any, b: Any, reverse: bool,
          key: Optional[Callable],
          cmp: Optional[Callable]) -> bool:
    """Проверить, что a должен стоять перед b при данной сортировке.

    :param a: первый элемент
    :param b: второй элемент
    :param reverse: направление сортировки
    :param key: функция ключа
    :param cmp: функция сравнения
    :return: True если a идёт перед b
    """
    c = _compare(a, b, key, cmp)
    return c > 0 if reverse else c < 0


# ---------------------------------------------------------------------------
# 1. Сортировка слиянием (merge sort)
# ---------------------------------------------------------------------------


def _merge(left: List[Any], right: List[Any], reverse: bool,
           key: Optional[Callable],
           cmp: Optional[Callable]) -> List[Any]:
    """Слить два отсортированных списка.

    :param left: левый список
    :param right: правый список
    :param reverse: направление
    :param key: функция ключа
    :param cmp: функция сравнения
    :return: объединённый отсортированный список
    """
    result: List[Any] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if _less(right[j], left[i], reverse, key, cmp):
            result.append(right[j])
            j += 1
        else:
            result.append(left[i])
            i += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(array: List[Any], reverse: bool = False,
               key: Optional[Callable] = None,
               cmp: Optional[Callable] = None,
               trace: Optional[List[List[Any]]] = None) -> List[Any]:
    """Сортировка слиянием.

    :param array: список
    :param reverse: направление
    :param key: функция ключа
    :param cmp: функция сравнения
    :param trace: если задан — сюда пишутся промежуточные состояния
    :return: новый отсортированный список
    """
    if len(array) <= 1:
        return list(array)
    mid = len(array) // 2
    left = merge_sort(array[:mid], reverse, key, cmp, trace)
    right = merge_sort(array[mid:], reverse, key, cmp, trace)
    merged = _merge(left, right, reverse, key, cmp)
    if trace is not None:
        trace.append(list(merged))
    return merged


# ---------------------------------------------------------------------------
# 2. Быстрая сортировка (quick sort)
# ---------------------------------------------------------------------------


def quick_sort(array: List[Any], reverse: bool = False,
               key: Optional[Callable] = None,
               cmp: Optional[Callable] = None,
               trace: Optional[List[List[Any]]] = None) -> List[Any]:
    """Быстрая сортировка (схема Ломуто).

    :param array: список
    :param reverse: направление
    :param key: функция ключа
    :param cmp: функция сравнения
    :param trace: коллектор промежуточных состояний
    :return: новый отсортированный список
    """
    data = list(array)
    _quick_sort_rec(data, 0, len(data) - 1, reverse, key, cmp, trace)
    return data


def _quick_sort_rec(data: List[Any], lo: int, hi: int, reverse: bool,
                    key: Optional[Callable], cmp: Optional[Callable],
                    trace: Optional[List[List[Any]]]) -> None:
    """Рекурсивная часть быстрой сортировки.

    :param data: список
    :param lo: левая граница
    :param hi: правая граница
    :param reverse: направление
    :param key: функция ключа
    :param cmp: функция сравнения
    :param trace: коллектор промежуточных состояний
    """
    if lo >= hi:
        return
    pivot = data[hi]
    i = lo
    for j in range(lo, hi):
        if _less(data[j], pivot, reverse, key, cmp):
            data[i], data[j] = data[j], data[i]
            i += 1
    data[i], data[hi] = data[hi], data[i]
    if trace is not None:
        trace.append(list(data))
    _quick_sort_rec(data, lo, i - 1, reverse, key, cmp, trace)
    _quick_sort_rec(data, i + 1, hi, reverse, key, cmp, trace)


# ---------------------------------------------------------------------------
# 3. Плавная (пирамидальная) сортировка (smooth sort)
# ---------------------------------------------------------------------------


def _sift_down(data: List[Any], start: int, end: int, reverse: bool,
               key: Optional[Callable], cmp: Optional[Callable]) -> None:
    """Просеять элемент вниз в двоичной куче.

    :param data: список
    :param start: индекс начала
    :param end: индекс конца
    :param reverse: направление
    :param key: функция ключа
    :param cmp: функция сравнения
    """
    root = start
    while 2 * root + 1 <= end:
        child = 2 * root + 1
        swap = root
        if _less(data[swap], data[child], reverse, key, cmp):
            swap = child
        if child + 1 <= end and _less(data[swap], data[child + 1],
                                      reverse, key, cmp):
            swap = child + 1
        if swap == root:
            return
        data[root], data[swap] = data[swap], data[root]
        root = swap


def smooth_sort(array: List[Any], reverse: bool = False,
                key: Optional[Callable] = None,
                cmp: Optional[Callable] = None,
                trace: Optional[List[List[Any]]] = None) -> List[Any]:
    """Плавная (пирамидальная) сортировка.

    :param array: список
    :param reverse: направление
    :param key: функция ключа
    :param cmp: функция сравнения
    :param trace: коллектор промежуточных состояний
    :return: новый отсортированный список
    """
    data = list(array)
    n = len(data)
    for start in range(n // 2 - 1, -1, -1):
        _sift_down(data, start, n - 1, reverse, key, cmp)
    for end in range(n - 1, 0, -1):
        data[0], data[end] = data[end], data[0]
        _sift_down(data, 0, end - 1, reverse, key, cmp)
        if trace is not None:
            trace.append(list(data))
    return data


# ---------------------------------------------------------------------------
# 4. Интроспективная сортировка (introsort)
# ---------------------------------------------------------------------------

_INSERTION_THRESHOLD = 16


def _insertion_sort(data: List[Any], lo: int, hi: int, reverse: bool,
                    key: Optional[Callable],
                    cmp: Optional[Callable]) -> None:
    """Сортировка вставками для малых подмассивов.

    :param data: список
    :param lo: левая граница
    :param hi: правая граница
    :param reverse: направление
    :param key: функция ключа
    :param cmp: функция сравнения
    """
    for i in range(lo + 1, hi + 1):
        val = data[i]
        j = i - 1
        while j >= lo and _less(val, data[j], reverse, key, cmp):
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = val


def _heap_sort_range(data: List[Any], lo: int, hi: int, reverse: bool,
                     key: Optional[Callable],
                     cmp: Optional[Callable]) -> None:
    """Пирамидальная сортировка на подмассиве (для introsort).

    :param data: список
    :param lo: левая граница
    :param hi: правая граница
    :param reverse: направление
    :param key: функция ключа
    :param cmp: функция сравнения
    """
    size = hi - lo + 1
    for start in range(size // 2 - 1, -1, -1):
        _sift_down(data, lo + start, hi, reverse, key, cmp)
    for end in range(hi, lo, -1):
        data[lo], data[end] = data[end], data[lo]
        _sift_down(data, lo, end - 1, reverse, key, cmp)


def introsort(array: List[Any], reverse: bool = False,
              key: Optional[Callable] = None,
              cmp: Optional[Callable] = None,
              trace: Optional[List[List[Any]]] = None) -> List[Any]:
    """Интроспективная сортировка (quick + heap + insertion).

    :param array: список
    :param reverse: направление
    :param key: функция ключа
    :param cmp: функция сравнения
    :param trace: коллектор промежуточных состояний
    :return: новый отсортированный список
    """
    data = list(array)
    max_depth = 2 * int(math.log2(len(data))) if len(data) > 1 else 0
    _introsort_rec(data, 0, len(data) - 1, max_depth,
                   reverse, key, cmp, trace)
    return data


def _introsort_rec(data: List[Any], lo: int, hi: int, depth: int,
                   reverse: bool, key: Optional[Callable],
                   cmp: Optional[Callable],
                   trace: Optional[List[List[Any]]]) -> None:
    """Рекурсивная часть интроспективной сортировки.

    :param data: список
    :param lo: левая граница
    :param hi: правая граница
    :param depth: оставшаяся глубина рекурсии
    :param reverse: направление
    :param key: функция ключа
    :param cmp: функция сравнения
    :param trace: коллектор промежуточных состояний
    """
    while hi - lo > _INSERTION_THRESHOLD:
        if depth == 0:
            _heap_sort_range(data, lo, hi, reverse, key, cmp)
            if trace is not None:
                trace.append(list(data))
            return
        depth -= 1
        pivot = data[(lo + hi) // 2]
        i, j = lo, hi
        while i <= j:
            while _less(data[i], pivot, reverse, key, cmp):
                i += 1
            while _less(pivot, data[j], reverse, key, cmp):
                j -= 1
            if i <= j:
                data[i], data[j] = data[j], data[i]
                i += 1
                j -= 1
        if trace is not None:
            trace.append(list(data))
        _introsort_rec(data, lo, j, depth, reverse, key, cmp, trace)
        lo = i
    _insertion_sort(data, lo, hi, reverse, key, cmp)


# ---------------------------------------------------------------------------
# 5. Timsort (упрощённая реализация)
# ---------------------------------------------------------------------------

_RUN = 32


def timsort(array: List[Any], reverse: bool = False,
            key: Optional[Callable] = None,
            cmp: Optional[Callable] = None,
            trace: Optional[List[List[Any]]] = None) -> List[Any]:
    """Упрощённый Timsort: сортировка вставками по «ранам» + слияние.

    :param array: список
    :param reverse: направление
    :param key: функция ключа
    :param cmp: функция сравнения
    :param trace: коллектор промежуточных состояний
    :return: новый отсортированный список
    """
    data = list(array)
    n = len(data)
    for start in range(0, n, _RUN):
        end = min(start + _RUN - 1, n - 1)
        _insertion_sort(data, start, end, reverse, key, cmp)
    size = _RUN
    while size < n:
        for lo in range(0, n, 2 * size):
            mid = min(lo + size - 1, n - 1)
            hi = min(lo + 2 * size - 1, n - 1)
            if mid < hi:
                left = data[lo:mid + 1]
                right = data[mid + 1:hi + 1]
                merged = _merge(left, right, reverse, key, cmp)
                data[lo:hi + 1] = merged
                if trace is not None:
                    trace.append(list(data))
        size *= 2
    return data


# ---------------------------------------------------------------------------
# Реестр алгоритмов и публичный API
# ---------------------------------------------------------------------------

_ALGORITHMS = {
    "merge": merge_sort,
    "quick": quick_sort,
    "smooth": smooth_sort,
    "intro": introsort,
    "tim": timsort,
}


def available_algorithms() -> List[str]:
    """Вернуть список доступных алгоритмов сортировки.

    :return: список имён алгоритмов
    """
    return list(_ALGORITHMS)


def my_sort(array: list, reverse: bool = False,
            key: Optional[Callable] = None,
            cmp: Optional[Callable] = None,
            algorithm: str = "tim") -> list:
    """Отсортировать список выбранным алгоритмом.

    :param array: сортируемый список
    :param reverse: False — по неубыванию, True — по невозрастанию
    :param key: функция, вычисляющая значение для сравнения
    :param cmp: функция сравнения двух аргументов
    :param algorithm: имя алгоритма: merge|quick|smooth|intro|tim
    :return: новый отсортированный список
    :raises ValueError: если algorithm неизвестен
    """
    if algorithm not in _ALGORITHMS:
        raise ValueError(f"Неизвестный алгоритм: {algorithm}")
    return _ALGORITHMS[algorithm](list(array), reverse, key, cmp)


# ---------------------------------------------------------------------------
# Визуализация по шагам
# ---------------------------------------------------------------------------


def visualize_sort(size: int = 10, algorithm: str = "merge",
                   reverse: bool = False) -> None:
    """Показать пошаговую сортировку случайного списка.

    :param size: размер списка
    :param algorithm: имя алгоритма
    :param reverse: направление сортировки
    :raises ValueError: если algorithm неизвестен
    """
    if algorithm not in _ALGORITHMS:
        raise ValueError(f"Неизвестный алгоритм: {algorithm}")
    data = [random.randint(-99, 99) for _ in range(size)]
    print(f"Исходный список: {data}")
    trace: List[List[Any]] = []
    result = _ALGORITHMS[algorithm](data, reverse, None, None, trace)
    for step, state in enumerate(trace, 1):
        print(f"Шаг {step:>3}: {state}")
    print(f"Результат: {result}")
    
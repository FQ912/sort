"""Консольная утилита сортировки данных.

Поддерживает:
    - числа и строки
    - сортировку по неубыванию/невозрастанию
    - чтение/запись файлов
    - визуализацию по шагам
"""

import argparse
from typing import List

import my_sort


def _read_file(path: str) -> List[str]:
    """Прочитать непустые строки из файла.

    :param path: путь к файлу
    :return: список строк
    """
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip()]


def _write_file(path: str, data: List[str]) -> None:
    """Записать строки в файл.

    :param path: путь к файлу
    :param data: список строк
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(data))


def _parse_args() -> argparse.Namespace:
    """Разобрать аргументы командной строки.

    :return: пространство имён с аргументами
    """
    parser = argparse.ArgumentParser(description="Сортировка данных")
    parser.add_argument("--input", help="входной файл")
    parser.add_argument("--output", help="выходной файл")
    parser.add_argument("--reverse", action="store_true",
                        help="по невозрастанию")
    parser.add_argument("--numbers", action="store_true",
                        help="интерпретировать данные как числа")
    parser.add_argument("--algorithm", default="tim",
                        choices=my_sort.available_algorithms(),
                        help="алгоритм сортировки")
    parser.add_argument("--visualize", type=int, metavar="N",
                        help="показать сортировку N случайных чисел")
    return parser.parse_args()


def main() -> None:
    """Точка входа утилиты."""
    args = _parse_args()

    if args.visualize:
        my_sort.visualize_sort(args.visualize, args.algorithm, args.reverse)
        return

    if not args.input:
        raise SystemExit("укажите --input или --visualize")

    data = _read_file(args.input)
    if args.numbers:
        data = [int(x) for x in data]

    result = my_sort.my_sort(data, reverse=args.reverse,
                             algorithm=args.algorithm)

    if args.output:
        _write_file(args.output, [str(x) for x in result])
    else:
        print(result)


if __name__ == "__main__":
    main()
    
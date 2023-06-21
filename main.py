import os
import types
from datetime import datetime


def logger(old_function):
    def new_function(*args, **kwargs):
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        result = old_function(*args, **kwargs)

        a = [float(i) for i in list(args)] if len(args) > 0 else None
        k = [float(i) for i in kwargs.values()] if len(kwargs) > 0 else None
        s = (sum(a) if a is not None else 0) + (sum(k) if k is not None else 0)

        with open('main.log', 'a', encoding='utf-8') as f:
            f.write(f'{date_time}, ')
            f.write(f'{old_function.__name__}, ')
            f.write(f'{a}, ')
            f.write(f'{k}, ')
            f.write(f'{None if a is None and k is None else s}\n')

        return result

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def logger_2(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            result = old_function(*args, **kwargs)

            a = [float(i) for i in list(args)] if len(args) > 0 else None
            k = [float(i) for i in kwargs.values()] if len(kwargs) > 0 else None
            s = (sum(a) if a is not None else 0) + (sum(k) if k is not None else 0)

            with open(path, 'a', encoding='utf-8') as f:
                f.write(f'{date_time}, ')
                f.write(f'{old_function.__name__}, ')
                f.write(f'{a}, ')
                f.write(f'{k}, ')
                f.write(f'{None if a is None and k is None else s}\n')

            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_2(path)
        def hello_world_2():
            return 'Hello World'

        @logger_2(path)
        def summator_2(a, b=0):
            return a + b

        @logger_2(path)
        def div_2(a, b):
            return a / b

        assert 'Hello World' == hello_world_2(), "Функция возвращает 'Hello World'"
        result = summator_2(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div_2(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator_2(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator_2' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def flat_generator(list_of_lists):
    for i in list_of_lists:
        for j in i:
            yield j


@logger
def test_3():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)
    return list(flat_generator(list_of_lists_1))


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()

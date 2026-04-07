Декораторы а питоне работают как обертка над функциями в питоне
декораторы позволяют добавлять новый функционал к нашей функции, не изменяя код самой функции

*Примеры использования*
- Подсчет времени выполнения функции
- Логирование
- Повтор в случае ошибки
- Ограничение на частой вызов функции



вот простейший пример декоратора:
```Python
from typing import Callable

def deco(func: Callable):
    def wrapper():
        res = func()
        return res
    return wrapper

@deco
def f():
    return 12
```

вот пример декоратора, который считает сколько времени работала функция
```Python
import time 

def time_deco(func: Callable):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f"время выполнения функции {end - start}")
        return res
    return wrapper 

@time_deco
def g(sec=1):
    time.sleep(sec)
    return 123

g(sec=2)
>>>время выполнения функции 2.0017080307006836
>>>123
```


вот так можно реализовать декоратор, который будет считать сколько раз я вызывал функцию:
```Python
def limit_calls(limit: int):
    def wrapper(func: Callable):
        def inner(*args, **kwargs):
            start = time.time()
            nonlocal limit
            if limit == 0:
                return "ERROR"
            res = func(*args, **kwargs)
            limit -= 1
            end = time.time()
            print(f"время выполнения функции {end - start}")
            return res
        return inner

    print(limit)
    return wrapper
    
@limit_calls(2)
def func(sec: int =1):
    time.sleep(sec)
    return 123
```
заметим, что тут важно обратить внимание на nonlocal, это нужно, чтобы питон понимал, что это не локальная перерменная, так как мы делаем операцию -= 1 с ней. Это эквивалентно `limit = limit - 1`, а это он воспринимает уже как присвоение и объявление новой переменной. А как мы помним из урока про области видимости у нас наш интерпритатор сначала смотрит на тело функции, запоминает, что там за переменные, а потом уже построчечно исполняет то, что мы написали.


хорошо было и передавать при декорировании и метаданные о функции
```Python
from functools import wraps

def limit_calls(limit: int):
    def wrapper(func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            start = time.time()
            nonlocal limit
            if limit == 2:
                print( "ERROR")
            res = func(*args, **kwargs)
            end = time.time()
            print(f"время выполнения функции {end - start}")
            return res
        return inner
    return wrapper
```

вот так он выглядит внутри
```Python
def my_wraps(original_func):
    """
    Кастомная реализация functools.wraps.
    Копирует метаданные из original_func в wrapper_func.
    """
    def decorator(wrapper_func):
        # 1. Копируем имя функции
        wrapper_func.__name__ = original_func.__name__
        
        # 2. Копируем строку документации (docstring)
        wrapper_func.__doc__ = original_func.__doc__
        
        # 3. Копируем имя модуля, в котором была создана функция
        wrapper_func.__module__ = original_func.__module__
        
        # 4. Копируем аннотации типов (если они есть)
        # Используем getattr на случай, если их нет, чтобы избежать ошибки
        wrapper_func.__annotations__ = getattr(original_func, '__annotations__', {})
        
        # 5. Сохраняем ссылку на саму оригинальную функцию 
        # (полезно, если кто-то захочет "развернуть" декоратор и добраться до оригинала)
        wrapper_func.__wrapped__ = original_func
        
        return wrapper_func
    
    return decorator
```

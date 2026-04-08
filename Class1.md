пример простого класса
```Python
class Counter:
    def __init__(self, initial_count=0):
        self.count = initial_count

    def get(self):
        return self.count
    
    def increment(self):
        self.count += 1

c = Counter(initial_count=0)
c.increment()
print(c.get())
>>> 1
```
на что надо обратить внимание:
- `__init__` - не совсем конструктор, это просто метод, который вызывается после инициализации
- в Python нет this, поэтому мы используем `self` . То есть `self` - это конкретный экземпляр класса.
```Python
class Counter:
    all_counters = [] # <- class attribute

    def __init__(self, initial_count=0):
        Counter.all_counters.append(self)
        self.count = initial_count

c1 = Counter(312)
c2 = Counter(76)
assert len(Counter.all_counters) == 2
assert c1.all_counters is c2.all_counters
```
в данном случае `all_counters` это атрибут объекта класс Коунтер

как хранятся поля класса:
```Python
>>> c = Counter(92)
>>> c.__class__
<class 'class1.Counter'>
>>> c.__dict__
{'count': 92}
>>> c.__dict__["foo"] = 62:
>>> c.foo
62
>>> del c.foo
```

так как Counter это тоже объект, то у него есть функции:
```Python
>>> Counter.__name__
'Counter'
>>> Counter.__doc__
>>> Counter.__module__
'class1'
>>> Counter.__bases__
(<class 'object'>,)
>>> Counter.__dict__
mappingproxy({'__module__': 'class1', 'all_counters': [<class1.Counter object at 0x105272830>, <class1.Counter object at 0x1052727d0>, <class1.Counter object at 0x10501a830>], '__init__': <function Counter.__init__ at 0x10528a320>, '__dict__': <attribute '__dict__' of 'Counter' objects>, '__weakref__': <attribute '__weakref__' of 'Counter' objects>, '__doc__': None})
```


**Что же там внутри?**
на самом деле класс это просто обертка над частью кода. Например:
```Python
>>> class Weird:
...     f1, f2 = 0, 1
...     for i in range(100):
...             f1, f2 = f2, f1 + f2
...
>>> Weird.f1
354224848179261915075
```
то есть мы просто исполнили код, который лежит внутри класса
```Python
>>> Weird.__dict__
mappingproxy({'__module__': '__main__', 'f1': 354224848179261915075, 'f2': 573147844013817084101, 'i': 99, '__dict__': <attribute '__dict__' of 'Weird' objects>, '__weakref__': <attribute '__weakref__' of 'Weird' objects>, '__doc__': None})
```



**Поиск атрибутов**
```Python
>>> class A:
...     x = 92
...
>>> a = A()
>>> a.x
92
>>> vars(a)
{}
>>> a.x = 62
>>> vars(a)
{'x': 62}
>>> a.x
62
>>> A.x
92
```
 поиск атрибутов похож на поиск переменных в областях видимости


**вызов функции**
```Python
>>> class B:
...     def foo(self):
...             pass
...
>>> b = B()
>>> b.foo()
>>> B.foo(b)
```
то есть два таких вывода эквивалентны

**Properties**
В питоне можно сделать метод, который будет работать как атрибут
```Python
class Counter:
    def __init__(self, initial_count=0) -> None:
        self.count = initial_count

    def increment(self):
        self.count += 1

    @property
    def is_zero(self):
        return self.count == 0

c = Counter(92)
print(c.is_zero)
```

**Оптимизация через `__slots__`**
По умолчанию каждый объект в Python хранит свои атрибуты в словаре `__dict__`. Словарь — это хэш-таблица, она гибкая, но занимает много места (даже если там всего две переменные).
когда мы добавляем `__slots__`, то мы выделяем фиксированный объем памяти, который можно тратить
```Python
class PointWithoutSlots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointWithSlots:
    __slots__ = ('x', 'y') # Резервируем место только под x и y
    def __init__(self, x, y):
        self.x = x
        self.y = y
```


**Управление доступом**
все поля всем доступны, но есть соглашение
- с буквы - публичное
- с `_` - приватные
- с `__` прикрепляется имя класса

```Python
class A:
    def __init__(self) -> None:
        self.pub = 92
        self._priv = 62
        self.__mang = 42

a = A()
print(a.pub, a._priv, a._A__mang)
```

## Наследование
пример:
```Python
class Animal:
    def speak(self):
        print("Издает какой-то звук")

class Dog(Animal):  # В скобках указываем родителя
    def speak(self):
        print("Гав-гав!")

my_dog = Dog()
my_dog.speak()  # Выведет: Гав-гав!
```
перечисляем родителей через запятую

`super()` - позволяет вызвать метод родительского класса
```Python
class Counter:
    def __init__(self, initial_count=0):
        self.count = initial_count

    def get(self):
        return self.count

class Sqcounter(Counter):
    def get(self):
        return super().get() ** 2

c = Sqcounter(10)
print(c.get())
```
вывело 100
**важен порядок родителей!!!**
```Python
class A:
    def f(self):
        print('A')

class B:
    def f(self):
        print('B')

class C(A, B):
    pass

C().f()
>>> A
```
при поиске атрибутов мы смотрим на родителей в определенном порядке

**`super()`**
как на самом деле работает super()?
```Python
class Base:
    def f(self):
        print('Base')

class A(Base):
    def f(self):
        print('A')
        super().f()

class B(Base):
    def f(self):
        print('B')
        super().f()

class C(A, B):
    pass

C().f()
>>>A
>>>B
>>>Base
```
`mro()` - возвращает порядок классов по которым происходит поиск атрибутов
```Python
>>> C.mro()
[<class 'class1.C'>, <class 'class1.A'>, <class 'class1.B'>, <class 'class1.Base'>, <class 'object'>]
```
на самом деле super() берет следующий класс из mro()
то есть из A мы переходим в B, а не в Base и там уже вызываем f()

## Декораторы для классов
декораторы для классов работают похоже как и для функций
```Python
import functools

class Counter():
    def __init__(self, initial_value=0):
        self.count = initial_value

    def increment(self):
        self.count += 1

    def get(self):
        return self.count

def doubling(cls):
    orig_f = cls.increment
    @functools.wraps(orig_f)
    def increment(self):
        orig_f(self)
        orig_f(self)

    cls.increment = increment
    return cls

@doubling
class DoubleCounter(Counter):
    pass

c = DoubleCounter()
c.increment()
print(c.get())
>>> 2
```
создаем класс, который два раза вызывается функция

## Магические методы
методы, которые переопределяют дефолтные операции с экземплярами класса
```Python
class Counter:
    def __init__(self, inital_count=0):
        self.count = inital_count

    def __lt__(self, other):
        return self.count < other.count

    def __eq__(self, other):
        return self.count == other.count

c1 = Counter(92)
c2 = Counter(62)
print(c1 == c2, c1 < c2)
>>> False False
```
но при том 
- >=, <= не сработает, надо определять
- через functools можно через два метода дать классу все
вот еще магические методы
```Python
class Counter:
    def __init__(self, inital_count=0):
        self.count = inital_count

    def __lt__(self, other):
        return self.count < other.count

    def __eq__(self, other):
        return self.count == other.count

    def __repr__(self):
        return f"Countrt({self.count})"

    def __str__(self):
        return f"Counted to {self.count}"

    def __hash__(self): # <- лучше не писать для и изменяемы объектов
        return hash(self.count)

    def __bool__(self): # определяет truethy семантику
        return self.count != 0

    # арифметика
    def __add__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return Counter(self.count + other)
    
    # для прибовления самого себя к себе
    def __radd__(self, other):
        return self + other

    def __call__(self, x): # вызов функции
        return x
```
- `__getattr__`  получает атрибут
- `__setattr__` задать атрибут
- `__delattr__` удалить атрибут

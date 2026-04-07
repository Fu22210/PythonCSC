в питоне уже есть много реализованных структур

### Списки
- внутри - расширающийся массив
- O(1) - индексация
- Добавление/удаление с конца - O(1)
- Копирование - O(N)
- Лучше их не копировать!

### Стэк
можно использовать список как стек
```Python
>>> xs = [1, 2, 3]
>>> xs.append(4)
>>> xs.pop()
4
```

### Связный список
- всегда хуже расширяющегося массива
- удаление их середны (O(N) - поиск середины, O(1) - удаление, так что мы не очень выигрываем)
- нет в питоне

#### Важные методы
**reverse/reversed**
```Python
>>> xs = [1, 2, 3]
>>> xs.reverse()
>>> xs
[3, 2, 1]
```
тут мы разворачиваем его inplace
```Python
>>> reversed(xs)
<list_reverseiterator object at 0x100744340>
>>> xs
[3, 2, 1]
>>> list(reversed(xs))
[1, 2, 3]
```
тут мы возвращаем итератор. то есть мы тратим O(1) памяти если мы хотим проитерировать по нему
**главное не вызвать list()**

**sort/sorted**
```Python
>>> xs = [92, 23, 54]
>>> xs
[92, 23, 54]
>>> xs.sort()
>>> xs
[23, 54, 92]
```
```Python
>>> xs = [92, 23, 54]
>>> sorted(xs)
[23, 54, 92]
```
аналогично мы можем сортить наш лист inplace, ну или же возвращать отсортированную версию
```Python
>>> type(sorted(xs))
<class 'list'>
```
в сорт есть аргумент key, для сравнения двух объектов (не компоратор!)
есть функция `functools.cmp_to_key`
также можно использовать tuple для составного ключа
```Python
>>> people = ['Tima', 'Sofia', 'Sashka']
>>> sorted(people, key = lambda s: (len(s), s[0]))
['Tima', 'Sofia', 'Sashka']
>>> sorted(people, key = lambda s: (len(s), s[-1]))
['Tima', 'Sofia', 'Sashka']
>>> sorted(people, key = lambda s: (len(s), s[-2]))
['Tima', 'Sofia', 'Sashka']
>>> sorted(people, key = lambda s: (s[-2], len(s)))
['Sofia', 'Sashka', 'Tima']
```
tuple имеет лексиграфическое сравнение

- сортировка в питоне стабильна, то есть не меняет местами, если key одинаковые
### очередь
лучше использовать deque from collections
есть методы:
- pop()
- append()
- appendleft()
внутри deque() лежит linked list of chunks
- индексация работает за O(N)
то есть у нас блоки по 64 элемента и блоки связаны между собой

### очередь с приоритетом
под капотом - это куча
```Python
>>> xs = [1, 43, 12, 100, 5]
>>> import heapq
>>> heapq.heapify(xs)
>>> xs
[1, 5, 12, 100, 43]
>>> heapq.heappush(xs, 1000)
>>> xs
[1, 5, 12, 100, 43, 1000]
>>> heapq.heappop(xs)
1
>>> heapq.heappop(xs)
5
>>> heapq.heappop(xs)
12
```

### defaultdict
```Python
>>> from collections import defaultdict
>>> g = defaultdict(list)
>>> g[0].append(1)
>>> g[3]
[]
>>> g[0]
[3]
```

в конструктор передаем функцию, которая возвращает что должно быть по умолчанию
нужно, например, для графов)

часто нам нужен `defaultdict(int)`, например, для подсчета количеств
для этого есть специальный класс Counter

```Python
>>> from collections import Counter
>>> c = Counter('aaabbbbbbcc')
>>> c
Counter({'b': 6, 'a': 3, 'c': 2})
>>> c['a']
3
```

**В Python все словари это хэш-мапа**


### ChainMap
мапа, которая состоит из нескольких мап. сначала смотри значения в первой мапе,  потом во второй и тд
```Python
>>> from collections import ChainMap
>>> locals = {}
>>> globals = {'foo': 23}
>>> buildin = {'baa': 321}
>>> c = ChainMap(locals, globals, buildin)
>>> c['foo']
23
>>> c['baa']
321
>>> locals['baa'] = 11111
>>> c['baa']
11111
```

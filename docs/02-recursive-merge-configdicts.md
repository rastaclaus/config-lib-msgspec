## Наиисать функцию для обьединения двух словарей.

### Типы и сигнатуры:

```python
ConfigScalar =  str | int | float | datetime.datetime | datetime.date | None
ConfigSequence = Sequence[ConfigScalar]
ConfigMapping = MutableMapping[str, "ConfigDict | ConfigScalar | ConfigSequence"]

def update_recursive(target: ConfigDict, source: ConfigDict) -> ConfigDict:
    # Implementation penging
```
### Правила объединения значений:
#### Определения
 -  Соответствующими считаются значения в обоих словарях на любом уровне вложенности, с одинаковой последовательностью ключей для извлечения.
 -  Классы значений определяются по соответствию типу `ConfigScalar`, `ConfigSequence` или `ConfigMapping`

1. Если соответствующие значения в обоих словарях имеют тип `ConfigScalar` - результатом будет значение из `source`
2. Если соответствующие значения в обоих словарях имеют тип `ConfigSequence`- результатом будет объединение
   последовательностей.
3. Если соответствующие значения в обоих словарях имеют тип `ConfigMapping` - результатом будет их рекурсивное
   объединение.
4. Если соответствующие значения в обоих словарях разных классов - выбрасывается `ValueError`.
5. Если в `source` соответствующего значения нет, или оно `is None` - результатом будет значение из `target`
6. Если в `target` соответствующего значения нет, или оно `is None` - результатом будет значение из `source`


### Примеры

```python
target = {"a": 1}, source = {"a": 2} => {"a": 2}
target = {"a": 1}, source = {"a": [1, 2]} => ValueError
target = {"a":  1}, source = {"a": {"c": 2, "d": 3}} => ValueError

target = {"a": {"b": 1}}, source = {"a": {"c": 2, "d": 3}} => {"a": {"b": 1, "c": 2, "d": 3}}
target = {"a": [1, 2, 3]}, source = {"a": [3, 4, 5]} => {"a": [1, 2, 3, 4, 5]}
```

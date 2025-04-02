## Получить из плоского словаря с разделителями в ключах вложенный словарь.

### Пример
```python
NEST_DELIMITER = "__"

source = {"a": 1} => {"a": 1}
source = {"s_d": 1} => {"s_d": 1}
source = {"__s": 1} => {"__s": 1}
source = {"a__b": 1} => {"a": {"b": 1}}
source = {"a__": 1} => {"a": 1}
source = {"a__b": 1, "a": 1} => ValueError
source = {"a____b": 1} => {"a__": {"b": 1}
source = {"__": 1} => ValueError
```

Implementation:
File : ./src/

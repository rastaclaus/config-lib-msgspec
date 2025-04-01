# Архитектура библиотеки конфигурации `config-lib`

## 1. Основные модули

```text
src/
├── config_lib/
│   ├── base.py       - Базовый класс и ядро
│   ├── sources/      - Источники конфигурации
│   │   ├── env.py
│   │   ├── yaml.py
│   │   └── cli.py
│   ├── validation/   - Валидация и обработка ошибок
│   └── utils/        - Вспомогательные функции
```

## 2. Базовый класс

```python:src/config_lib/base.py
from msgspec import Struct, ValidationError

class BaseConfig(Struct, frozen=True):
    """
    Base class for configuration with validation via msgspec
    Features:
    - Immutable structure (frozen)
    - Static typing
    - Serialization/deserialization from common formats
    """
    
    @classmethod
    def auto_load(cls, config_path: str | None = None) -> Self:
        """Новый алгоритм загрузки с поддержкой вложенности"""
        merged = deep_merged(
            cls.from_base(),
            deep_merged(
                cls.from_file(config_path),
                deep_merged(
                    cls.from_env(),
                    cls.from_cli()
                    )
                )
            )
        )
        return msgspec.convert(merged, cls, strict=False)
```

## 3. Механизм загрузки конфигурации

**Приоритет источников:**
1. CLI аргументы
2. Переменные окружения
3. YAML-файл
4. Значения по умолчанию

**Особенности:**
- Автоматическое приведение типов
- Поддержка вложенных структур через `Struct`
- Комбинирование данных из нескольких источников

## 3.1 Стратегия слияния данных

Добавлен новый механизм объединения с глубоким слиянием:
```python
def deep_merge(base: dict, update: dict) -> dict:
    """Recursively merge dictionaries while preserving nesting."""
    for k, v in update.items():
        if isinstance(v, dict) and k in base:
            base[k] = deep_merge(base.get(k, {}), v)
        else:
            base[k] = v
    return base
```

## 3.2 Обновленный механизм загрузки
```python:src/config_lib/base.py
```

## 4. Валидация и обработка ошибок

```python:src/config_lib/validation.py
class ConfigValidationError(ValidationError):
    """Кастомное исключение для ошибок конфигурации"""
    def __str__(self):
        return f"Configuration validation failed: {super().__str__()}"
```

## 4.1 Расширенная валидация
- Добавлена поддержка валидации вложенных структур через `msgspec.Struct`
- Автоматическое преобразование псевдонимов полей через `rename="camel"`
- Валидация типов с сохранением иммутабельности frozen-структур

## 5. Безопасность
- Автоматическое маскирование полей с `secret` в названии
- Валидация чувствительных данных
- Интеграция с logging.config для защиты секретов


## 6 Пример с вложенной конфигурацией
```python
class AppConfig(BaseConfig):
    database: DatabaseConfig
    logging: dict
    debug_mode: bool = False

config = AppConfig.auto_load(
    cli={'debug_mode': True},
    env={'database': {'pool_size': 20}},
    yaml={'logging': {'level': 'debug'}}
)
```

## Преимущества архитектуры:
1. **Производительность**: Использование msgspec вместо pydantic дает до 5x прирост скорости
2. **Статическая типизация**: Поддержка Python 3.11+ с современным синтаксисом
3. **Безопасность**: Встроенная защита чувствительных данных
4. **Легковесность**: Нет внешних зависимостей кроме msgspec

## Пример использования
```python
from config_lib import BaseConfig

class DatabaseConfig(BaseConfig):
    host: str
    port: int = 5432
    user: str
    password: str

# Автоматическая загрузка из всех источников
config = DatabaseConfig.auto_load()

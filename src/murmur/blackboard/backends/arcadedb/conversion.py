from __future__ import annotations

from datetime import date, datetime
from typing import Any

from ...errors import TypeConversionError
from ...models import PropertyValue


class TypeConverter:
    @staticmethod
    def to_java(value: PropertyValue) -> Any:
        if isinstance(value, (str, int, float, bool, datetime)) or value is None:
            return value
        if isinstance(value, list):
            return [TypeConverter.to_java(item) for item in value]
        msg = f"Unsupported Python value for ArcadeDB conversion: {type(value)!r}"
        raise TypeConversionError(msg)

    @staticmethod
    def from_java(value: Any) -> PropertyValue:
        if isinstance(value, date) and not isinstance(value, datetime):
            return datetime.combine(value, datetime.min.time())
        if isinstance(value, (str, int, float, bool, datetime)) or value is None:
            return value
        if isinstance(value, list):
            return [TypeConverter.from_java(item) for item in value]
        if isinstance(value, tuple):
            return [TypeConverter.from_java(item) for item in value]
        msg = f"Unrecognized ArcadeDB value type: {type(value)!r}"
        raise TypeConversionError(msg)

    @staticmethod
    def row_to_dict(result_row: Any) -> dict[str, PropertyValue]:
        if isinstance(result_row, dict):
            return {str(k): TypeConverter.from_java(v) for k, v in result_row.items()}
        if hasattr(result_row, "items"):
            return {
                str(k): TypeConverter.from_java(v)
                for k, v in result_row.items()  # type: ignore[call-arg]
            }
        msg = "ArcadeDB row cannot be converted into dictionary"
        raise TypeConversionError(msg)

    @staticmethod
    def params_to_java(params: dict) -> Any:
        return {str(k): TypeConverter.to_java(v) for k, v in params.items()}

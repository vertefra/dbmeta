from abc import ABC, abstractmethod
from typing import Any, Literal, List, Dict
from enum import Enum


class IDatabase(ABC):
    exclude_tables: List[str] = []
    exclude_schema: List[str] = []

    @abstractmethod
    def inspect_database() -> "Metadata":
        ...


class Metadata:
    schema: List["Schema"]
    tables: List["Table"]
    columns: List["Column"]

    def __init__(
        self, schema: List["Schema"], tables: List["Table"], columns: List["Column"]
    ) -> None:
        self.schema = schema
        self.tables = tables
        self.columns = columns


class DatabaseItem:
    def __init__(self, record: dict) -> None:
        for key, value in record.items():
            if self._has_attr_annotation(key):
                setattr(self, key, value)

    def _has_attr_annotation(self, att_name: str) -> bool:
        return att_name in self.__annotations__


class Column(DatabaseItem):
    udt_name: str
    table_catalog: str
    table_schema: str
    table_name: str
    column_name: str
    ordinal_position: int
    column_default: str | None
    is_nullable: Literal["YES"] | Literal["NO"]
    data_type: str
    character_maximum_length: int | None
    is_updatable: bool

    def __init__(self, record: dict) -> None:
        super().__init__(record)

    def __repr__(self) -> str:
        return f"<{self.column_name}: {self.udt_name} : NULLABLE: {self.is_nullable} : DEFAULT: {self.column_default}>"


class Schema(DatabaseItem):
    catalog_name: str
    schema_name: str
    schema_owner: str
    tables: List["Table"]

    def __init__(self, record: dict) -> None:
        super().__init__(record)
        self.tables = []

    def __repr__(self) -> str:
        return f"<{self.schema_name}>"


class Table(DatabaseItem):
    table_catalog: str
    table_schema: str
    table_name: str
    table_type: str
    columns: List[Column]

    def __init__(self, record: dict) -> None:
        super().__init__(record)
        self.columns = []

    def __repr__(self) -> str:
        return f"<{self.table_name}>"

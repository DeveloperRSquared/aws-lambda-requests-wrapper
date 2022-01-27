from __future__ import annotations

from collections import abc
from typing import Any
from typing import Dict
from typing import Iterator
from typing import Mapping
from typing import Optional
from typing import Tuple


class CaseInsensitiveDict(abc.MutableMapping):
    def __init__(self, data: Optional[Mapping[str, Any]] = None) -> None:
        # Mapping from lowercased key to tuple of (actual key, value)
        self._data: Dict[str, Any] = {}
        if data is None:
            data = {}
        self.update(data)

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key.lower()] = (key, value)

    def __getitem__(self, key: str) -> Any:
        return self._data[key.lower()][1]

    def __delitem__(self, key: str) -> None:
        del self._data[key.lower()]

    def __iter__(self) -> Iterator[str]:
        return (key for key, _ in self._data.values())

    def __len__(self) -> int:
        return len(self._data)

    def lower_items(self) -> Iterator[Tuple[str, Any]]:
        return ((key, val[1]) for key, val in self._data.items())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, abc.Mapping):
            # TODO(rikhil): check the correct behaviour here.
            return NotImplemented
        other = CaseInsensitiveDict(other)
        return dict(self.lower_items()) == dict(other.lower_items())

    def copy(self) -> CaseInsensitiveDict:
        return CaseInsensitiveDict(dict(self._data.values()))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({dict(self.items())!r})'

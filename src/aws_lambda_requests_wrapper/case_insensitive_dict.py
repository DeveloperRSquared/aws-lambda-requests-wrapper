from collections import abc
from json import JSONEncoder
from typing import Any
from typing import Dict
from typing import Iterator
from typing import Mapping
from typing import Optional
from typing import Tuple


class CaseInsensitiveDict(abc.MutableMapping):
    def __init__(self, data: Optional[Mapping[str, Any]] = None) -> None:
        # Mapping from lowercased key to tuple of (actual key, value)
        self._store: Dict[str, Any] = {}
        if data is None:
            data = {}
        self.update(data)

    def __setitem__(self, key: str, value: Any) -> None:
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key: str) -> None:
        return self._store[key.lower()][1]

    def __delitem__(self, key: str) -> None:
        del self._store[key.lower()]

    def __iter__(self) -> Iterator[str]:
        return (casedkey for casedkey, _ in self._store.values())

    def __len__(self) -> int:
        return len(self._store)

    def lower_items(self) -> Iterator[Tuple[str, Any]]:
        return ((lowerkey, keyval[1]) for (lowerkey, keyval) in self._store.items())

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, abc.Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    def copy(self):
        return CaseInsensitiveDict(self._store.values())

    def __repr__(self):
        return f'{self.__class__.__name__}({dict(self.items())!r})'


class CaseInsensitiveDictEncoder(JSONEncoder):
    def default(self, o: CaseInsensitiveDict) -> Dict[str, Any]:
        return dict(o.items())

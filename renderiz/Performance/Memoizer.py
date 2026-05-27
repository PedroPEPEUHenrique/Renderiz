from __future__ import annotations

import hashlib
import json
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple


class Memoizer:
    def __init__(self, MaxSize: int = 256) -> None:
        self._Cache: Dict[str, Any] = {}
        self._AccessOrder: List[str] = []
        self._MaxSize = MaxSize
        self._Hits = 0
        self._Misses = 0

    def _MakeKey(self, *Args: Any, **Kwargs: Any) -> str:
        try:
            Serialized = json.dumps(
                {"args": list(Args), "kwargs": Kwargs},
                sort_keys=True,
                default=str,
            )
        except Exception:
            Serialized = str((Args, Kwargs))
        return hashlib.md5(Serialized.encode()).hexdigest()

    def Get(self, Key: str) -> Tuple[bool, Any]:
        if Key in self._Cache:
            self._AccessOrder.remove(Key)
            self._AccessOrder.append(Key)
            self._Hits += 1
            return True, self._Cache[Key]
        self._Misses += 1
        return False, None

    def Set(self, Key: str, Value: Any) -> None:
        if Key in self._Cache:
            self._AccessOrder.remove(Key)
        elif len(self._Cache) >= self._MaxSize:
            Oldest = self._AccessOrder.pop(0)
            del self._Cache[Oldest]
        self._Cache[Key] = Value
        self._AccessOrder.append(Key)

    def Memoize(self, Fn: Callable) -> Callable:
        @wraps(Fn)
        def Wrapper(*Args: Any, **Kwargs: Any) -> Any:
            Key = self._MakeKey(*Args, **Kwargs)
            Hit, Cached = self.Get(Key)
            if Hit:
                return Cached
            Result = Fn(*Args, **Kwargs)
            self.Set(Key, Result)
            return Result
        return Wrapper

    def Invalidate(self, Key: Optional[str] = None) -> None:
        if Key is None:
            self._Cache.clear()
            self._AccessOrder.clear()
        elif Key in self._Cache:
            del self._Cache[Key]
            self._AccessOrder.remove(Key)

    @property
    def Size(self) -> int:
        return len(self._Cache)

    @property
    def HitRate(self) -> float:
        Total = self._Hits + self._Misses
        return self._Hits / Total if Total else 0.0

    def Stats(self) -> Dict[str, Any]:
        return {
            "Size": self.Size,
            "MaxSize": self._MaxSize,
            "Hits": self._Hits,
            "Misses": self._Misses,
            "HitRate": f"{self.HitRate:.1%}",
        }

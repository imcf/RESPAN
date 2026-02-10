"""
Compatibility wrapper for `tifffile.imwrite` that accepts either the old
`compression=("name", arg)` tuple form or the newer
`compression="name", compressionargs=arg` form. This keeps behaviour
consistent across tifffile versions and for frozen Windows .exe builds.
"""

from __future__ import annotations

import inspect
from typing import Any

import tifffile

__all__ = ["imwrite"]


def _backend_supports_compressionargs() -> bool:
    try:
        sig = inspect.signature(tifffile.imwrite)
        return "compressionargs" in sig.parameters
    except Exception:
        # Be conservative: assume modern API if we can't inspect
        return True


_SUPPORTS_COMPRESSIONARGS = _backend_supports_compressionargs()


def _normalize_compressionargs(name, arg):
    """Normalize compression argument into a kwargs mapping expected by
    imagecodecs-style compressors when necessary.

    Examples:
    - ("zlib", 1) -> {"level": 1}
    - {"level": 1} -> {"level": 1}
    - integer -> {"level": integer} (default fallback)
    """
    # Already a mapping/dict-like object
    if isinstance(arg, dict):
        return arg
    # Integer -> interpret as compression level
    if isinstance(arg, int):
        return {"level": arg}
    # If None or unknown type, return as-is
    return arg


def imwrite(filename: str, data: Any, *args, **kwargs) -> Any:
    """Write TIFF while handling compression API differences.

    Behaviour:
    - If caller passes ``compression=("zlib", 1)`` it will be converted to
      ``compression="zlib", compressionargs={'level': 1}`` when supported.
    - If caller passes ``compression="zlib", compressionargs=1`` and the
      backend does not support ``compressionargs``, it will be converted to
      the older tuple form ``compression=("zlib", 1)`` where possible.

    All other kwargs are forwarded as-is to ``tifffile.imwrite``.
    """
    comp = kwargs.get("compression", None)
    compargs = kwargs.get("compressionargs", None)

    # Handle tuple form: compression=(name, arg)
    if isinstance(comp, (tuple, list)) and len(comp) >= 1:
        name = comp[0]
        arg = comp[1] if len(comp) > 1 else None
        if _SUPPORTS_COMPRESSIONARGS:
            kwargs["compression"] = name
            if arg is not None:
                kwargs["compressionargs"] = _normalize_compressionargs(name, arg)
            elif "compressionargs" in kwargs:
                kwargs.pop("compressionargs")
        else:
            # Keep tuple form for old backends
            kwargs["compression"] = (name, arg) if arg is not None else (name,)
            kwargs.pop("compressionargs", None)
    else:
        # If new form is used but backend doesn't accept compressionargs,
        # convert to tuple form (try to extract level if mapping provided)
        if compargs is not None and not _SUPPORTS_COMPRESSIONARGS:
            if isinstance(compargs, dict) and "level" in compargs:
                kwargs["compression"] = (comp, compargs["level"])
            else:
                kwargs["compression"] = (comp, compargs)
            kwargs.pop("compressionargs", None)
        else:
            # If compargs is provided and backend supports compressionargs,
            # ensure integer args become mappings to avoid **int errors
            if compargs is not None and _SUPPORTS_COMPRESSIONARGS:
                kwargs["compressionargs"] = _normalize_compressionargs(comp, compargs)

    return tifffile.imwrite(filename, data, *args, **kwargs)

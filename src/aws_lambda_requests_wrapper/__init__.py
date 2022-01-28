try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # type: ignore[import,no-redef]

__version__: str = version(__name__)

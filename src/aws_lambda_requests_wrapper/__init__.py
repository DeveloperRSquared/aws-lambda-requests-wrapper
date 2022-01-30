# isort: skip_file
# pylint: disable=wrong-import-position
try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import PackageNotFoundError  # type: ignore[no-redef,misc]
    from importlib_metadata import version  # type: ignore[no-redef]

try:
    __version__: str = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

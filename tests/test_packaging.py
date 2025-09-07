import importlib.metadata
import pytest

def test_package_is_installed():
    """
    A simple test to check that the `ludo-game` package metadata can be found
    after installation.
    """
    try:
        # This will succeed if the package was installed (e.g., with `pip install .`)
        version = importlib.metadata.version('ludo-game')
        assert version == "1.0.0"
    except importlib.metadata.PackageNotFoundError:
        pytest.fail("The 'ludo-game' package does not appear to be installed.")

def test_can_import_main_modules():
    """
    Tests that the main packages `ludo` and `apps` can be imported.
    """
    try:
        import ludo
        import apps
        assert ludo is not None
        assert apps is not None
    except ImportError as e:
        pytest.fail(f"Failed to import a core module: {e}")

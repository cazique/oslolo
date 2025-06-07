
# scripts/test.py
import pytest
import sys

def run_tests():
    """Runs the full test suite using pytest."""
    print("--- Running OSLolo Test Suite ---")
    # Add '--gui-tests' to run GUI tests
    args = sys.argv[1:]
    exit_code = pytest.main(args)
    sys.exit(exit_code)

if __name__ == "__main__":
    run_tests()

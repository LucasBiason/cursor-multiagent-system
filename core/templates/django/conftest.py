"""
Configuration file for pytest tests.

This module sets up Django settings and test environment for all test modules.
"""

import os
import sys
import django
from django.conf import settings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.test_settings')

django.setup()

def pytest_configure():
    """Configure pytest with Django settings."""
    if not settings.configured:
        django.setup()



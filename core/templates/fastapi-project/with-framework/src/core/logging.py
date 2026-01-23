"""
Logging Configuration (DEPRECATED)

⚠️ DEPRECATED: Logging is now configured automatically by MicroserviceBuilder.

This file is kept for backward compatibility but should not be used.
The builder automatically sets up structured logging via with_observability().

For custom logging configuration, extend the builder's _setup_structured_logging() method.
"""
import warnings

warnings.warn(
    "setup_logging() is deprecated. "
    "Logging is now automatically configured by MicroserviceBuilder.with_observability(). "
    "Remove manual setup_logging() calls from your code.",
    DeprecationWarning,
    stacklevel=2
)


def setup_logging():
    """
    DEPRECATED: Logging is now configured automatically by MicroserviceBuilder.
    
    This function does nothing and is kept only for backward compatibility.
    Remove all calls to setup_logging() from your code.
    """
    pass

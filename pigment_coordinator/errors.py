class CoordinatorError(Exception):
    """Base error for deterministic coordinator failures."""


class ConfigurationError(CoordinatorError):
    """Raised when required runtime configuration is missing or unsafe."""


class GateError(CoordinatorError):
    """Raised when a workflow gate prevents advancement."""


class MessageValidationError(CoordinatorError):
    """Raised when a provider message violates the shared contract."""


class ProviderError(CoordinatorError):
    """Raised when a provider call cannot produce a usable response."""


class TransitionError(CoordinatorError):
    """Raised when a requested state transition is not allowed."""

"""AniBridge list provider base classes package."""

from anibridge.list.base import (
    ListEntity,
    ListEntry,
    ListMedia,
    ListMediaType,
    ListProvider,
    ListProviderT,
    ListStatus,
    ListTarget,
    ListUser,
    MappingDescriptor,
    ProviderLogger,
)
from anibridge.list.registry import (
    ListProviderRegistry,
    list_provider,
    provider_registry,
)

__all__ = [
    "ListEntity",
    "ListEntry",
    "ListMedia",
    "ListMediaType",
    "ListProvider",
    "ListProviderRegistry",
    "ListProviderT",
    "ListStatus",
    "ListTarget",
    "ListUser",
    "MappingDescriptor",
    "ProviderLogger",
    "list_provider",
    "provider_registry",
]

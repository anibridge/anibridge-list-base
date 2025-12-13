"""Anibridge list provider interfaces package."""

from anibridge.list.interfaces import (
    ListEntry,
    ListMedia,
    ListMediaType,
    ListProvider,
    ListStatus,
    ListUser,
    MappingDescriptor,
    MappingEdge,
    MappingGraph,
)
from anibridge.list.registry import (
    ListProviderRegistry,
    list_provider,
    provider_registry,
)

__all__ = [
    "ListEntry",
    "ListMedia",
    "ListMediaType",
    "ListProvider",
    "ListProviderRegistry",
    "ListStatus",
    "ListUser",
    "MappingDescriptor",
    "MappingEdge",
    "MappingGraph",
    "list_provider",
    "provider_registry",
]

"""Anibridge list provider interfaces package."""

from anibridge.list.interfaces import (
    ListEntity,
    ListEntry,
    ListMedia,
    ListMediaType,
    ListProvider,
    ListProviderT,
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
    "ListEntity",
    "ListEntry",
    "ListMedia",
    "ListMediaType",
    "ListProvider",
    "ListProviderRegistry",
    "ListProviderT",
    "ListStatus",
    "ListUser",
    "MappingDescriptor",
    "MappingEdge",
    "MappingGraph",
    "list_provider",
    "provider_registry",
]

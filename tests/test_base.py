"""Tests for the list provider base classes."""

import asyncio
import logging
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import cast

import pytest
from anibridge.utils.types import MappingDescriptor, ProviderLogger

from anibridge.list import (
    ListEntry,
    ListMedia,
    ListMediaType,
    ListProvider,
    ListStatus,
    ListTarget,
    ListUser,
)


class DummyListMedia(ListMedia["DummyListProvider"]):
    """Concrete list media for tests."""

    def __init__(self, provider: "DummyListProvider", key: str) -> None:  # noqa: UP037
        """Create a dummy media object."""
        self._provider = provider
        self._key = key
        self._title = f"Media {key}"

    @property
    def media_type(self) -> ListMediaType:
        """Return the media type."""
        return ListMediaType.TV

    @property
    def total_units(self) -> int | None:
        """Return the total episode count."""
        return 12


class DummyListEntry(ListEntry["DummyListProvider"]):
    """Concrete list entry for tests."""

    def __init__(self, provider: "DummyListProvider", key: str) -> None:  # noqa: UP037
        """Create a dummy entry."""
        self._provider = provider
        self._key = key
        self._title = f"Entry {key}"
        self._media = DummyListMedia(provider, key)
        self._progress: int | None = 1
        self._repeats: int | None = 0
        self._review: str | None = None
        self._status: ListStatus | None = ListStatus.CURRENT
        self._user_rating: int | None = 80
        self._started_at: datetime | None = datetime(2026, 3, 12, tzinfo=UTC)
        self._finished_at: datetime | None = None

    @property
    def progress(self) -> int | None:
        """Return the current progress."""
        return self._progress

    @progress.setter
    def progress(self, value: int | None) -> None:
        """Update the current progress."""
        self._progress = value

    @property
    def repeats(self) -> int | None:
        """Return the repeat count."""
        return self._repeats

    @repeats.setter
    def repeats(self, value: int | None) -> None:
        """Update the repeat count."""
        self._repeats = value

    @property
    def review(self) -> str | None:
        """Return the review text."""
        return self._review

    @review.setter
    def review(self, value: str | None) -> None:
        """Update the review text."""
        self._review = value

    @property
    def status(self) -> ListStatus | None:
        """Return the list status."""
        return self._status

    @status.setter
    def status(self, value: ListStatus | None) -> None:
        """Update the list status."""
        self._status = value

    @property
    def user_rating(self) -> int | None:
        """Return the user rating."""
        return self._user_rating

    @user_rating.setter
    def user_rating(self, value: int | None) -> None:
        """Update the user rating."""
        self._user_rating = value

    @property
    def started_at(self) -> datetime | None:
        """Return the start timestamp."""
        return self._started_at

    @started_at.setter
    def started_at(self, value: datetime | None) -> None:
        """Update the start timestamp."""
        self._started_at = value

    @property
    def finished_at(self) -> datetime | None:
        """Return the finish timestamp."""
        return self._finished_at

    @finished_at.setter
    def finished_at(self, value: datetime | None) -> None:
        """Update the finish timestamp."""
        self._finished_at = value

    def media(self) -> DummyListMedia:
        """Return the associated media object."""
        return self._media


class DummyListProvider(ListProvider):
    """Concrete provider used to exercise batch helpers."""

    NAMESPACE = "dummy"
    MAPPING_PROVIDERS = frozenset({"anilist"})

    def __init__(self) -> None:
        """Initialize the provider with a test logger."""
        super().__init__(logger=cast(ProviderLogger, logging.getLogger("tests.list")))

    async def delete_entry(self, key: str) -> None:
        """Delete a list entry."""
        return None

    async def resolve_mapping_descriptors(
        self, descriptors: Sequence[MappingDescriptor]
    ) -> Sequence[ListTarget]:
        """Resolve descriptors into list targets."""
        return tuple(
            ListTarget(descriptor=descriptor, media_key=descriptor[1])
            for descriptor in descriptors
        )

    async def get_entry(self, key: str) -> DummyListEntry | None:
        """Return a dummy entry or raise for a sentinel key."""
        if key == "boom":
            raise RuntimeError("boom")
        if key == "missing":
            return None
        return DummyListEntry(self, key)

    async def update_entry(self, key: str, entry: ListEntry) -> ListEntry | None:
        """Return the updated entry."""
        if key == "boom":
            raise RuntimeError("boom")
        return entry

    def user(self) -> ListUser | None:
        """Return a stable dummy user."""
        return ListUser(key="user-1", title="Test User")


def test_list_provider_default_hooks() -> None:
    """The default optional hooks should remain safe."""
    provider = DummyListProvider()

    assert asyncio.run(provider.initialize()) is None
    assert asyncio.run(provider.clear_cache()) is None
    assert asyncio.run(provider.close()) is None
    assert asyncio.run(provider.restore_list("backup")) is None
    assert asyncio.run(provider.search("query")) == []
    assert provider.user() == ListUser(key="user-1", title="Test User")

    with pytest.raises(NotImplementedError):
        asyncio.run(provider.backup_list())


def test_list_provider_batch_helpers_and_status_ordering() -> None:
    """Batch helpers should preserve order and tolerate per-item failures."""
    provider = DummyListProvider()
    entry = DummyListEntry(provider, "ok")
    failing_entry = DummyListEntry(provider, "boom")

    assert [
        item.key if item else None
        for item in asyncio.run(provider.get_entries_batch(("ok", "missing", "boom")))
    ] == [
        "ok",
        None,
        None,
    ]
    assert asyncio.run(provider.update_entries_batch((entry, failing_entry))) == [
        entry,
        None,
    ]
    assert ListStatus.COMPLETED > ListStatus.PLANNING

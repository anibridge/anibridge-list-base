# anibridge-list-base

anibridge-list-base provides base classes and utilities to implement and register media list providers for the [AniBridge](https://github.com/anibridge/anibridge) project.

> [!IMPORTANT]
> This package is intended for developers building AniBridge list providers. If you're looking to use AniBridge as an end user, please refer to the [AniBridge documentation](https://anibridge.eliasbenb.dev/).

## Installation

```shell
pip install anibridge-list-base
# pip install git+https://github.com/anibridge/anibridge-list-base.git
```

## API reference

The package exposes its public API from `anibridge.list` and the core definitions in `anibridge.list.base`.

To get more context, explore the `anibridge.list.base` module's source code and docstrings.

- `ListProvider` (base class)
  - Key methods and hooks:
    - `__init__(*, logger: ProviderLogger, config: dict | None = None) -> None`: Construct a provider with an injected logger and optional configuration.
    - `async backup_list() -> str`: Optional backup hook returning a string representation of the user's list. The base implementation raises `NotImplementedError`.
    - `async clear_cache() -> None`: Optional cache clearing hook that AniBridge will occasionally run to free up memory and prevent stale data.
    - `async close() -> None`: Optional cleanup hook called when the provider is shut down or reloaded.
    - `async delete_entry(key: str) -> None`: Delete a list entry.
    - `async resolve_mapping_descriptors(descriptors: Sequence[MappingDescriptor]) -> Sequence[ListTarget]`: Resolve mapping descriptors into provider media keys.
    - `async get_entries_batch(keys: Sequence[str]) -> Sequence[ListEntry | None]`: Optional batch helper to fetch multiple entries at once.
    - `async get_entry(key: str) -> ListEntry | None`: Fetch a user's list entry; return `None` if not present.
    - `async initialize() -> None`: Optional async initialization called once after construction. Perform network I/O, authentication, or pre-fetching here.
    - `async restore_list(backup: str) -> None`: Optional backup restore hook. The base implementation is a no-op.
    - `async search(query: str) -> Sequence[ListEntry]`: Optional search helper returning matching entries.
    - `async update_entries_batch(entries: Sequence[ListEntry]) -> Sequence[ListEntry | None]`: Optional batch helper to update multiple entries at once.
    - `async update_entry(key: str, entry: ListEntry) -> ListEntry | None`: Update an entry; return the updated entry or `None` on failure.
    - `user() -> ListUser | None`: Return the associated user object, if any.

- `ListEntry`, `ListMedia`, `ListUser` (base classes)
  - `ListEntry` stores and exposes properties and setters for `progress`, `repeats`, `review`, `status` (`ListStatus`), `user_rating`, `started_at`, `finished_at`, and `total_units`, plus a `media()` method returning the associated `ListMedia`.
  - `ListMedia` stores `media_type` (`ListMediaType`), optional `labels`, `poster_image`, `external_url`, and `total_units`.
  - `ListUser` is an immutable dataclass with `key` and `title`.
  - `ListTarget` pairs a resolved `MappingDescriptor` with a provider media key.
  - `user_rating` is a 0-100 integer scale (providers may document their own mapping).

- `ListStatus` (StrEnum)
  - Enum of common list statuses: `COMPLETED`, `CURRENT`, `DROPPED`, `PAUSED`, `PLANNING`, `REPEATING`.
  - Includes ordering semantics via `priority` for comparison.

## Examples

You can view the following built-in provider implementations as examples of how to implement the base classes:

- [anibridge-provider-template](https://github.com/anibridge/anibridge-provider-template)
- [anibridge-anilist-provider](https://github.com/anibridge/anibridge-anilist-provider)
- [anibridge-mal-provider](https://github.com/anibridge/anibridge-mal-provider)

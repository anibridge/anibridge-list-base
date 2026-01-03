# anibridge-list-interface

anibridge-list-interface provides a set of protocols and utilities to implement and register media list providers for the [AniBridge](https://github.com/anibridge/anibridge) project.

> [!IMPORTANT]
> This package is a definition-only interface library. It does not include any concrete provider implementations. Provider implementations should be created in separate packages that depend on this interface library.

## Installation

```shell
pip install anibridge-list-interface
# pip install git+https://github.com/anibridge/anibridge-list-interface.git
```

## API reference

The library exposes two major surfaces: the `anibridge.list.interfaces` set of protocols and the `anibridge.list.registry` registration helpers.

To get some more context, explore the `anibridge.list.interfaces` module's source code and docstrings.

- `ListProvider` (Protocol)

  - The core interface provider implementations must follow.
  - Key methods:
    - `async initialize() -> None`: Optional async initialization to prepare the provider. It's called once after instantiation. It's recommended to perform any network I/O or setup here such as authentication or pre-fetching list data.
    - `async get_entry(key: str) -> ListEntry | None`: Fetch a user's list entry; return `None` if it doesn't exist in the user's list yet.
    - `async build_entry(key: str) -> ListEntry`: Prepare an entry for a media item not yet in the user's list.
    - `async update_entry(key: str, entry: ListEntry) -> ListEntry | None`: Update a list entry; return the updated entry or `None` on failure.
    - `async delete_entry(key: str) -> None`: Delete a list entry.
    - `async backup_list() -> str` / `async restore_list(backup: str) -> None`: Optional backup/restore. Providers may choose to implement these to allow users to export/import their list data; it is up to the provider how the backup string is formatted.
    - `resolve_mappings(mapping: MappingGraph, *, scope: str | None) -> MappingDescriptor | None`: This method matches media identifiers from a mapping graph to the provider's own identifiers. It is used to help resolve media across different providers. The mapping graph can contain identifiers from different sources; the default upstream mappings contain `anidb`, `anilist`, `imdb`, `mal`, `tmdb_movie`, `tmdb_show`, `tvdb_movie`, and `tvdb_show` namespaces. However, users can extend this with custom namespaces as needed.

- `ListEntry`, `ListMedia`, `ListUser` (Protocols)

  - `ListEntry` exposes properties and setters for `progress`, `repeats`, `review`, `status` (`ListStatus`), `user_rating`, `started_at`, `finished_at`, and `total_units`, and a `media()` method returning the associated `ListMedia`.
  - `ListMedia` exposes `media_type` (`ListMediaType`), `poster_image`, and `total_units`.
  - `ListUser` is a simple dataclass-like structure with `key` and `title`.

- `ListStatus` (StrEnum)

  - Enum of common list statuses: `COMPLETED`, `CURRENT`, `DROPPED`,
    `PAUSED`, `PLANNING`, `REPEATING`.
  - Includes ordering semantics via `priority` for comparison.

- Mapping protocols

  - `MappingDescriptor`, `MappingEdge`, `MappingGraph` describe how media identifiers can be related and provide a hook for providers to resolve identifiers from a graph of mappings.

- `ListProviderRegistry` and `list_provider` decorator
  - `ListProviderRegistry` is a simple registry that maps namespace strings to provider classes. Use `create(namespace, *, config=None)` to instantiate a provider or `get(namespace)` to access the class.
  - `list_provider` is a decorator helper that registers a provider with the module-level `provider_registry` by default.

## Examples

You can view the following built-in provider implementations as examples of how to implement the interface:

- [anibridge-provider-template](https://github.com/anibridge/anibridge-provider-template)
- [anibridge-anilist-provider](https://github.com/anibridge/anibridge-anilist-provider)
- [anibridge-mal-provider](https://github.com/anibridge/anibridge-mal-provider)

# LOCAL_OVERRIDES

This file records local rules for this repository.

## Repository-Specific Layout

This repository is the source project for AI Project OS.

```text
template/project-os/
```

is the distributable OS package source.

```text
project-os/
```

is the installed OS instance used to manage this repository itself.

## Local Audit Location

This repository's own audit output belongs in:

```text
project-os/audit/
```

Do not write repository-specific audit output into:

```text
template/project-os/audit/
```

because those files are part of the distributable template.

## GitHub Rule

The GitHub repository for this project must be private.

Public repository creation is not allowed.

## Linear Rule

The first Linear import must follow `project-os/LINEAR_POLICY.md`:

- Generate import plan first.
- Confirm team/project.
- Check duplicates.
- Wait for explicit human approval before bulk write.

## Release Artifact Rule

Zip artifacts are generated from:

```text
template/project-os/
```

Generated release zip files are not the source of truth.


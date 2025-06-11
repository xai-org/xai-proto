# Contributing to xAI API Protobuf Definitions

Thank you for your interest in contributing to the xAI API Protobuf Definitions repository! This repository hosts the public Protocol Buffer (protobuf) definitions for xAI's gRPC-based APIs, and we appreciate efforts to improve its quality and clarity.

## Contribution Guidelines

### Accepted Contributions
We welcome contributions that enhance the clarity and maintainability of the repository without altering the functionality of the protobuf definitions. Examples of accepted contributions include:
- Improving comments or documentation within the `.proto` files to make them clearer or more accurate.
- Fixing typos or grammatical errors in the `.proto` files, README, or other documentation.
- Enhancing the README or other supporting files (e.g., `buf.yaml`, `buf.gen.yaml`) with better explanations or examples, provided they do not change the repository's behavior.

### Non-Accepted Contributions
Functional changes to the protobuf definitions themselves are not accepted, as these files are maintained by xAI to ensure compatibility with our gRPC API services. Examples of non-accepted changes include:
- Adding, removing, or modifying services, messages, fields, or options in the `.proto` files.
- Altering the structure or behavior of the API definitions in any way that impacts their functionality.

## For xAI Contributors

The following sections are intended for xAI employees and contributors who are maintaining or updating the protobuf definitions. External users do not need to follow these steps since they will not be making functional changes to the `.proto` files.

### Making Changes to Proto Files

1. **Create a Branch**: Start by creating a new branch for your changes. Use a descriptive name that reflects the purpose of the change, such as `feature/add-new-service` or `bugfix/correct-field-type`.
   ```bash
   git checkout -b <branch-name>
   ```

2. **Modify Proto Files**: Make the necessary changes to the `.proto` files in the `proto` directory. Ensure that your changes align with the intended API design and follow the style guidelines enforced by Buf linting rules.

3. **Update Documentation**: If your changes introduce new services, messages, or fields, update the relevant documentation within the `.proto` files and, if applicable, in the `README.md` to reflect these changes.

### Linting and Formatting

Buf is configured to enforce consistent protobuf definitions through linting and breaking change detection.

#### Linting

The `buf.yaml` file specifies linting rules under the `lint` section. The `MINIMAL` rule set is used to enforce basic style and correctness. To run linting:

```bash
buf lint
```

This checks all `.proto` files in the `proto` directory for compliance with the configured rules.

#### Formatting

To ensure consistent formatting across `.proto` files:

```bash
buf format -w
```

This command reformats all `.proto` files in place according to Buf's formatting standards.

### Checking for Successful Compilation

To ensure the proto files themselves have no issues, run:

```bash
buf build
```

This should run with no output if there are no issues.

### Breaking Change Detection

The `buf.yaml` file also configures breaking change detection under the `breaking` section. The `FILE` rule ensures that changes to `.proto` files do not break compatibility with existing generated code. To check for breaking changes:

```bash
buf breaking --against <previous-commit-or-reference>
```

For example, to compare against the previous commit:

```bash
buf breaking --against .git#branch=main
```

This ensures that updates to the protobuf definitions remain backward-compatible unless explicitly intended.

All of the above checks are enforced on pull requests via a GitHub Action. They are all required to pass for the pull request to be eligible for merging.

### Committing and Pushing Changes

1. **Commit Changes**: Once you've made and tested your changes locally, commit them with a clear and descriptive commit message following the project's commit message guidelines.
   ```bash
   git add .
   git commit -m "feat: add new service to API definition"
   ```

2. **Update CHANGELOG.md**: Add your changes to the `Unreleased` section of `CHANGELOG.md` under the appropriate subsection (`Added`, `Changed`, `Fixed`, or `Removed`). Follow the existing format and provide a brief description of the change.
   - For example, if you added a new feature, update the `Added` subsection under `Unreleased` with a line like:
     ```
     - Added new `UserService` for managing user data.
     ```
   - Commit this update with your changes.

3. **Push to Remote**: Push your branch to the remote repository and create a pull request for review.
   ```bash
   git push origin <branch-name>
   ```

4. **Code Review**: Collaborate with your team to review the changes. Address any feedback by making additional commits to the same branch.

### Merging to Main

Once your pull request is approved and all checks pass, it can be merged into the `main` branch.

### Versioning and Tagging Releases

After merging changes to `main`, if the update warrants a new release (e.g., it introduces new features or breaking changes), create a new git tag to mark the release version. Follow semantic versioning (`MAJOR.MINOR.PATCH`) to determine the appropriate version bump:

- **Patch** (`0.0.X`): For backward-compatible bug fixes or minor documentation updates.
- **Minor** (`0.X.0`): For backward-compatible new features or enhancements.
- **Major** (`X.0.0`): For breaking changes that are not backward-compatible.

To create and push a new tag:

1. **Determine the New Version**: Based on the nature of the changes, decide the new version number.
2. **Create a Tag**: Tag the latest commit on `main` with the new version.
   ```bash
   git checkout main
   git pull origin main
   git tag -a v1.0.0 -m "Release version 1.0.0 with new API service"
   ```
3. **Push the Tag**: Push the tag to the remote repository.
   ```bash
   git push origin v1.0.0
   ```

This tag will serve as a reference point for downstream consumers of the protobuf definitions, ensuring they can depend on a specific version of the API.

### Triggering a GitHub Release

Pushing a git tag with the format `vX.Y.Z` (e.g., `v1.0.0`) to the repository triggers the `release.yaml` GitHub workflow defined in `.github/workflows/release.yaml`. This automated workflow creates a new GitHub Release associated with the tagged commit. The release will include:

- A title matching the tag name (e.g., `v1.0.0`).
- Automatically generated release notes based on the commit history.

This process ensures that each versioned release is properly documented and accessible to users via the GitHub Releases page, providing a clear changelog and download links for any associated artifacts if configured.

### Updating CHANGELOG.md After Release

Once the GitHub Release is created, update the `CHANGELOG.md` to reflect the released version by moving the changes from the `Unreleased` section to a new versioned section. Follow these steps:

1. **Create a New Branch**: After the tag is pushed and the release is created, create a new branch for updating the changelog.
   ```bash
   git checkout main
   git pull origin main
   git checkout -b chore/update-changelog-v1.0.0
   ```

2. **Update CHANGELOG.md**: Move the contents of the `Unreleased` section to a new heading with the version number and release date. Include a link to the GitHub Release.
   - Replace the `[Unreleased]` section contents with empty placeholders (as shown in the current `CHANGELOG.md` template).
   - Add a new section below `[Unreleased]` with the version number and current date in the format `YYYY-MM-DD`. For example:
     ```
     ## [v1.0.0] - 2023-10-15
     ### Added
     - Added new `UserService` for managing user data.
     ### Changed
     - None.
     ### Fixed
     - None.
     ### Removed
     - None.
     ```
   - Link the version number to the GitHub Release by formatting it as `[v1.0.0]: https://github.com/xai-org/xai-proto/releases/tag/v1.0.0` at the bottom of the file (adjust the repository URL as necessary).

3. **Commit and Push**: Commit the changelog update and push the branch for review.
   ```bash
   git add CHANGELOG.md
   git commit -m "chore: update changelog for v1.0.0 release"
   git push origin chore/update-changelog-v1.0.0
   ```

4. **Create a Pull Request**: Open a pull request for this update. Once reviewed and approved, merge it into `main`.

This ensures that the changelog remains up-to-date and provides users with a clear history of changes linked to specific releases.
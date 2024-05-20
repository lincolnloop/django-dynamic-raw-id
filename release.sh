#!/bin/bash
set -o errexit
set -o pipefail

# Run tests before release
./tests.sh

# Bump up major version number
poetry version minor
VERSION="v$(poetry version -s)"

# Commit new version number and create a tag and Github release
git add pyproject.toml && git commit -am "Bump up version number to v$(poetry version -s)"
git tag $VERSION
git push
git push --tags
gh release create --generate-notes --latest --title=$VERSION $VERSION

# Publish to Pypi
poetry publish --build

# pyproject-bump-version
A GitHub Action to bump pyproject.toml version numbers during pull requests

This action will bump the version number of `pyproject.toml` file with respect to the main branch.

For instance, say the version numbers in `branch1` and `main` are both `1.0.0` and a pull request is being made from `branch1` into `main`, then this action will bump the version number to `2.0.0` (if you specify `major` as the `bump_type` input).

Note, that this action will only bump the version if the version number in main is less than or equal to the compare branch version.

You can control whether you want the bump to happen before merging or after by checking the variable `github.event.pull_request.merged`.


## Example Usage:

The following example will do the following:
1. Only runs on a pull request into main and when any files in the directory `python_project/` have changed or the `pyproject.toml` file has changed.
2. The job only runs if the pull request is not being merged. This is useful for when a repository is set up to not allow writing directly to main.
3. It will do a minor version bump to the `pyproject.toml` and commit the changes to the compare branch.

```yaml
name: "Version bumper"
on:
  pull_request:
    branches:
      - main
    paths:
      - 'python_project/**'
      - './pyproject.toml'

jobs:
  bump-version:
    if: github.event.pull_request.merged == false
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          repository: ${{ github.event.pull_request.head.repo.full_name }}
          ref: ${{ github.event.pull_request.head.ref }}
          fetch-depth: "0"

      - name: Version bumper
        uses: apowis/pyproject-bump-version@v0.0.1
        with:
          file_to_bump: "./pyproject.toml"
          bump_type: "minor"
          main_branch: "main"
          python_version: "3.10"
```


# TODO List
- Work out more about the fetch depth and potentially using different branches
- Document `version_compare.py` more and add some tests.
- Add more options to EndBug/add-and-commit@v9 inputs
- Add option to not merge or not depending on pull request merge status
- Implement more file types than pyproject.toml?
- Long term, think about using npm stuff instead of Python scripts. Probably will never get to doing this.

import argparse
from pathlib import Path
from subprocess import check_output
from typing import Literal, Optional, Tuple

from packaging.version import parse, Version
import toml


def get_main_version(project_file: Path, main_branch: Optional[str] = None) -> Version:
    """
    Uses git cat-file to toml load the pyproject file and returns the verison number
    """
    main_branch = main_branch if main_branch else "main"
    pyproject = check_output(["git", "cat-file", "blob", f"origin/{main_branch}:./{project_file}"])
    version_string = toml.loads(pyproject.decode())["project"]["version"]
    return parse(version_string)


def get_current_version(pyproject: str) -> Version:
    """
    Toml loads the pyproject file and returns the verison number.
    """
    with open(pyproject, "r") as fh:
        pyproject_dict = toml.load(fh)
        version_string = pyproject_dict["project"]["version"]
        return parse(version_string)


def get_next_version(
    version_number: Version, bump_type: Literal["major", "minor", "micro"]
) -> str:
    """Bumps the provided version_number by one"""
    major, minor, micro = version_number.release
    if bump_type == "major":
        return f"{major + 1}.0.0"
    if bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{micro + 1}"


def bump_pyproject(pyproject: Path, new_version_number: str) -> None:
    """Bumps the version number in the pyproject file"""
    with pyproject.open("r") as fh:
        d = toml.load(pyproject)
        d["project"]["version"] = new_version_number
    with pyproject.open("w") as fh:
        toml.dump(d, fh)


def parse_args() -> Tuple[str, str, str, Path]:
    """get argparse values"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--main", help="Main branch name", required=True)
    parser.add_argument(
        "--bump_type",
        help="Bump type",
        choices=["major", "minor", "micro"],
        required=True,
    )
    parser.add_argument("--pyproject", help="Path to pyproject.toml", required=True)
    parser.add_argument(
        "--bump_commit_file",
        help="Path to file containing git commit message",
        required=True,
    )
    args = parser.parse_args()
    pyproject = Path(args.pyproject)
    if not Path(pyproject).is_file():
        raise FileNotFoundError(f"{pyproject} does not exist")

    return (
        args.main,
        args.bump_type,
        args.bump_commit_file,
        pyproject,
    )


def main():
    main_branch, bump_type, bump_commit_file, pyproject = parse_args()

    main_version = get_main_version(pyproject, main_branch)
    current_version = get_current_version(pyproject)

    print(f"{main_branch} branch version: {main_version}")
    print(f"Current branch version: {current_version}")
    if current_version <= main_version:
        new_version = get_next_version(main_version, bump_type)
        bump_pyproject(pyproject, new_version)
        bump_message = (
            f"Bumped version from {current_version} to {new_version}"
        )
        print(bump_message)
        with open(bump_commit_file, "w") as fh:
            fh.write(bump_message)
    else:
        print('No need to bump the version this time.')


if __name__ == "__main__":
    main()

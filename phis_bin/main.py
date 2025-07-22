from pathlib import Path
import argparse
import shutil

CR = Path(__file__).parent


def get_version(bindir: Path) -> str:
    dir_names = [i for i in bindir.iterdir() if i.is_dir() and i.name.startswith('1')]
    if len(dir_names) == 0:
        return 'unknown'
    else:
        dir_names.sort()
        return dir_names[-1].name


def main():
    BIN_DIR = CR / 'BIN'

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--init-from',
        type=str,
        help='Initialize the binary directory with existing binaries.',
    )

    parser.add_argument(
        '--init',
        help='copy BIN and config files to the current directory',
        action='store_true',
    )

    args = parser.parse_args()

    if args.init:
        if not BIN_DIR.exists() and not BIN_DIR.is_dir():
            print('please init from existing binaries first.')
            return
        else:
            shutil.copytree(BIN_DIR, Path.cwd() / 'BIN')

    original_bin: str = args.init_from
    if original_bin is None:
        # print help
        parser.print_help()
        return

    if not Path(original_bin).is_absolute():
        original_bin = Path.cwd() / original_bin
    else:
        original_bin = Path(original_bin)

    bindir = original_bin / 'BIN'
    if not bindir.exists() or not bindir.is_dir():
        print(f'BIN directory {bindir} does not exist.')
        return
    else:
        if BIN_DIR.exists():
            print(f"removing existing version {get_version(BIN_DIR)}")
            shutil.rmtree(BIN_DIR)
        print(f"initing from verison {get_version(bindir)}")
        shutil.copytree(bindir, BIN_DIR)

"""Remove all __pycache__ directories under the folder containing this script."""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {'.venv', '.git', 'node_modules'}


def clear_pycache(root: Path = ROOT) -> int:
    removed = 0
    for path in root.rglob('__pycache__'):
        if not path.is_dir() or SKIP_DIRS & set(path.relative_to(root).parts):
            continue
        shutil.rmtree(path, ignore_errors=True)
        print(f'Removed {path}')
        removed += 1
    return removed


if __name__ == '__main__':
    print(f'Done. Removed {clear_pycache()} __pycache__ folder(s).')

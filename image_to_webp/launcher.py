import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from version import APP_EXE_NAME, APP_VERSION, CACHE_DIR_NAME


def _bundle_path():
    if getattr(sys, 'frozen', False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent / 'build'
    return base / 'bundle.zip'


def _cache_dir():
    local_app_data = os.environ.get('LOCALAPPDATA')
    if not local_app_data:
        local_app_data = str(Path.home() / 'AppData' / 'Local')
    return Path(local_app_data) / 'IJoySoft' / CACHE_DIR_NAME


def _is_cache_ready(cache_dir):
    version_file = cache_dir / 'version.txt'
    app_exe = cache_dir / f'{APP_EXE_NAME}.exe'
    return (
        version_file.exists()
        and version_file.read_text(encoding='utf-8').strip() == APP_VERSION
        and app_exe.exists()
    )


def _extract_bundle(cache_dir):
    bundle = _bundle_path()
    if not bundle.exists():
        raise FileNotFoundError(f'未找到内置资源包: {bundle}')

    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(bundle) as archive:
        archive.extractall(cache_dir)

    (cache_dir / 'version.txt').write_text(APP_VERSION, encoding='utf-8')


def _launch_app(app_exe):
    result = subprocess.run([str(app_exe)], cwd=str(app_exe.parent))
    return result.returncode


def main():
    cache_dir = _cache_dir()
    if not _is_cache_ready(cache_dir):
        _extract_bundle(cache_dir)

    app_exe = cache_dir / f'{APP_EXE_NAME}.exe'
    if not app_exe.exists():
        raise FileNotFoundError(f'未找到程序入口: {app_exe}')

    sys.exit(_launch_app(app_exe))


if __name__ == '__main__':
    main()

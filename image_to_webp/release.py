import os
import shutil
import subprocess
import sys

from version import APP_EXE_NAME, RELEASE_EXE_NAME


def _pyinstaller_base(script_dir):
    assets_dir = os.path.join(script_dir, 'assets')
    ico_dir = os.path.join(script_dir, 'ico')
    return [
        sys.executable, '-m', 'PyInstaller',
        '--clean', '--noupx', '-w',
        '--paths', os.path.join(script_dir, '..'),
        '-i', os.path.join(ico_dir, 'logo.ico'),
        '--add-data', f'{assets_dir}{os.pathsep}assets',
        '--add-data', f'{ico_dir}{os.pathsep}ico',
        '--hidden-import', 'PIL',
        '--hidden-import', 'pylnk3',
        '--exclude-module', 'tkinter',
        '--exclude-module', 'matplotlib',
        '--exclude-module', 'numpy',
        '--exclude-module', 'scipy',
        '--exclude-module', 'pandas',
    ]


def _build_app_onedir(script_dir):
    dist_dir = os.path.join(script_dir, 'dist')
    app_dir = os.path.join(dist_dir, APP_EXE_NAME)
    if os.path.isdir(app_dir):
        shutil.rmtree(app_dir)

    cmd = _pyinstaller_base(script_dir) + [
        '-D', '-n', APP_EXE_NAME,
        os.path.join(script_dir, 'run.py'),
    ]
    subprocess.check_call(cmd, cwd=script_dir)
    return app_dir


def _create_bundle_zip(script_dir, app_dir):
    build_dir = os.path.join(script_dir, 'build')
    os.makedirs(build_dir, exist_ok=True)
    bundle_base = os.path.join(build_dir, 'bundle')
    bundle_zip = f'{bundle_base}.zip'
    if os.path.exists(bundle_zip):
        os.remove(bundle_zip)

    shutil.make_archive(bundle_base, 'zip', app_dir)
    return bundle_zip


def _build_launcher_onefile(script_dir, bundle_zip):
    ico_dir = os.path.join(script_dir, 'ico')
    launcher_script = os.path.join(script_dir, 'launcher.py')
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '-F', '--clean', '--noupx', '-w',
        '--paths', os.path.join(script_dir, '..'),
        '--paths', script_dir,
        '-n', RELEASE_EXE_NAME,
        '-i', os.path.join(ico_dir, 'logo.ico'),
        '--add-data', f'{bundle_zip}{os.pathsep}.',
        '--hidden-import', 'version',
        launcher_script,
    ]
    subprocess.check_call(cmd, cwd=script_dir)


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = _build_app_onedir(script_dir)
    bundle_zip = _create_bundle_zip(script_dir, app_dir)
    _build_launcher_onefile(script_dir, bundle_zip)
    shutil.rmtree(app_dir, ignore_errors=True)
    print(f'打包完成: dist/{RELEASE_EXE_NAME}.exe')
    print('分发单个 exe 即可；首次运行会解压到本地缓存，之后启动会更快')

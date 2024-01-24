# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

datas = [("../../Anaconda/envs/deadlock/Lib/site-packages/streamlit/runtime","./streamlit/runtime"),
("../../Anaconda/envs/deadlock/Lib/site-packages/streamlit/static", "./streamlit/static"),
("../../Anaconda/envs/deadlock/Lib/site-packages/streamlit_agraph","./streamlit_agraph")]
datas += collect_data_files("streamlit")
datas += copy_metadata("streamlit")


block_cipher = None

#修改下面a里面的datas为=datas
a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='run_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

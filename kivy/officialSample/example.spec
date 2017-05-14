# -*- mode: python -*-

block_cipher = None


a = Analysis(['example.py'],
             pathex=['C:\\work\\PythonCode\\kivy\\officialSample'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='example',
          debug=False,
          strip=False,
          upx=True,
          console=False )

from kivy.deps import sdl2, glew
coll = COLLECT(exe, Tree('.'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='example')
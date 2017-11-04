# -*- mode: python -*-
from kivy.deps import sdl2, glew

block_cipher = None


a = Analysis(['sudoku.py'],
             pathex=['D:\\work\\pythonCode\\kivy\\numberPlace\\beta'],
             binaries=[],
             datas=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             hiddenimports=[])

a.datas+=[('sudoku.kv','D:\\work\\pythonCode\\kivy\\numberPlace\\beta\\sudoku.kv',"DATA"),
          ('libz3.dll','D:\\work\\pythonCode\\kivy\\numberPlace\\beta\\libz3.dll',"DATA")]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='sudoku',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )

coll = COLLECT(exe, Tree('.'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='sudoku')
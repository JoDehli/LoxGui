import sys
from cx_Freeze import setup, Executable

product_name = 'PyLoxoneGui'

bdist_msi_options = {
    'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s' % product_name,
}

build_exe_options = {
    "excludes": ["tkinter"]}

# , "include_files": ["Main.ui"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="PyLoxGui",
      version="0.1",
      description="PyLoxone Qt Gui",
      options={"build_exe": build_exe_options, 'bdist_msi': bdist_msi_options},
      executables=[Executable("main.py", base=base)])

import sys

from cx_Freeze import setup, Executable

from Version import server_version

# python setup.py build
# python setup.py bdist_msi

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

includeFiles = [
    "./images/",
    "./lang/",
]

includes = ["pyDes", "web", "requests"]  # 'SerialMonitor'
excludes = ['tkinter']
packages = ["time", "sys", "datetime", "traceback", "os", "io", "atexit", "inspect", "getopt", "socket", "wmi",
            "threading", "json", "subprocess", "pyDes", "web", "requests", "getmac", "platform"]
requires = ['pyDes', 'requests', 'web.py', 'pyserial', 'wmi', 'getmac']  # RPi.GPIO

build_exe_options = {
    'includes': includes,
    'excludes': excludes,
    'packages': packages,
    'include_files': includeFiles
}

shortcut_table = [
    ("DesktopShortcut",  # Shortcut
     "DesktopFolder",  # Directory_
     "DMS",  # Name
     "TARGETDIR",  # Component_
     "[TARGETDIR]DMS.exe",  # Target
     None,  # Arguments
     None,  # Description
     None,  # Hotkey
     None,  # Icon
     None,  # IconIndex
     None,  # ShowCmd
     'TARGETDIR'  # WkDir
     )
]

msi_data = {
    "Shortcut": shortcut_table
}

bdist_msi_options = {
    'data': msi_data
}

options = {
    "build_exe": build_exe_options,
    "bdist_msi": bdist_msi_options
}

executables = [
    Executable('Server.py',
               base=base,
               targetName='DMS',
               icon="icon.ico",
               shortcutName="DMS",
               shortcutDir="DesktopFolder")
]

setup(name='Deutschtec DMS',
      version=server_version,
      description='Deutschtec application to control remote doors',
      options=options,
      executables=executables,
      requires=requires
      )

# tabs/__init__.py
import os
import importlib
from .base_tab import BaseTab

def get_tab_modules():
    tab_modules = []
    tabs_folder = os.path.dirname(__file__)
    for filename in os.listdir(tabs_folder):
        if filename.endswith('_tab.py') and filename != 'base_tab.py':
            module_name = f'tabs.{filename[:-3]}'
            module = importlib.import_module(module_name)
            # Check if module has required attributes
            if hasattr(module, 'tab_id') and hasattr(module, 'tab_label') and hasattr(module, 'get_layout'):
                tab_modules.append(module)
    # Sort tab_modules based on a priority or alphabetically if needed
    return tab_modules

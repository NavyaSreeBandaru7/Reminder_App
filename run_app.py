#!/usr/bin/env python3
"""
Custom Streamlit runner that completely disables metrics and configuration system
"""

import os
import sys
import types

# Create fake modules to prevent Streamlit from loading its metrics system
class FakeModule(types.ModuleType):
    def __init__(self, name):
        super().__init__(name)
        self.__path__ = []
    
    def __getattr__(self, name):
        return None

# Replace critical Streamlit modules with dummies
sys.modules['streamlit.runtime.metrics_util'] = FakeModule('metrics_util')
sys.modules['streamlit.runtime.installation'] = FakeModule('installation')
sys.modules['streamlit.config'] = FakeModule('config')

# Set environment variables to prevent any file writes
os.environ['STREAMLIT_GLOBAL_METRICS'] = '0'
os.environ['STREAMLIT_SERVER_ENABLE_STATIC_SERVE'] = '1'
os.environ['STREAMLIT_GLOBAL_DEVELOPMENT_MODE'] = '0'
os.environ['HOME'] = '/tmp'

# Import and run Streamlit with our app
from streamlit.web.cli import main

if __name__ == '__main__':
    sys.argv = [
        "streamlit", "run", "app.py",
        "--global.developmentMode=false",
        "--logger.level=error",
        "--browser.gatherUsageStats=false"
    ]
    sys.exit(main())

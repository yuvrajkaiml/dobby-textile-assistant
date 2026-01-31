import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web import app

# Vercel requires the variable to be named 'app'
# It is already named 'app' in the import

import sys
import os

# Insert the parent directory of the current file into the system path
# This allows importing modules from the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

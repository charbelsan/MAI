import sys
import os
current_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(current_file_path)
sys.path.append(current_file_path)
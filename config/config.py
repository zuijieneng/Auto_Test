import os
from pathlib import Path

# BASE_FILE_DIR = os.path.dirname(os.path.abspath(__file__)) + "\\test_data\\"  # F:\Python\Python基础\PythonProject\
BASE_FILE_DIR = Path(__file__).parent / "test_data//"  # F:\Python\Python基础\PythonProject\

BASE_LOG_DIR = os.path.dirname(os.path.abspath(__file__)) + "\\result\\" + "\\log\\"  # F:\Python\Python基础\PythonProject\result\log\
LOG_DIR = Path(__file__).parent / "result/log/"  # F:\Python\Python基础\PythonProject\result\log
LOG_ROOT_DIR = Path(__file__).parent.parent  # F:\Python\Python基础

if __name__ == '__main__':
    print(BASE_FILE_DIR.joinpath("jjj"))

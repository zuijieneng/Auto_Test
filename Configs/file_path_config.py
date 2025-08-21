from pathlib import Path

# BASE_FILE_DIR = os.path.dirname(os.path.abspath(__file__)) + "\\Data\\"  # F:\Python\Python基础\PythonProject\
BASE_FILE_DIR = Path(__file__).parent.parent  # F:\Python\Python基础\PythonProject\
FILE_PATH = {
    "logs": BASE_FILE_DIR / "Log/",  # D:\TestEngineer\Auto_UnitTest_Project\PythonProject\Result\log
    "datas": BASE_FILE_DIR / "Data/",
    "config.ini": BASE_FILE_DIR / "Configs/config.ini",
}


def get_file_path(name):
    return FILE_PATH.get(name)

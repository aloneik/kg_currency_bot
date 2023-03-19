@echo off

rmdir /q /s venv

echo Create virual environment
python -m venv venv

echo Activate virtual environment
call .\venv\Scripts\activate

echo Install required python modules
python -m pip install -r requirements.txt

echo Virtual environment succesfully initialized

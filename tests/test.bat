@echo off

echo The current user is: %USERNAME%

echo "Booting up Makehuman Daemon"
call C:\Users\%USERNAME%\mambaforge\Scripts\activate.bat C:\Users\%USERNAME%\mambaforge
call conda activate makehuman
cd ..
cd makehuman-docker\custom_makehuman\makehuman
start "Makehuman Daemon" cmd /c "python makehuman.py > NUL 2>&1"

timeout /T 15 /NOBREAK > NUL
echo "Makehuman Daemon is ready"

cd ..
cd ..
cd ..
cd pythonServices\3Dify-sliderModule
call python -m pytest -v --disable-warnings test_main.py::test_scanFace_noImage test_main.py::test_scanFace_correctImage test_main.py::test_scanFace_noFace test_main.py::test_extractFeatures_noImage test_main.py::test_extractFeatures_correctImage test_main.py::test_extractFeatures_noFace test_main.py::test_extractFeatures_lowRes test_main.py::test_customSkin_noImage test_main.py::test_applyAndDownload

taskkill /FI "WindowTitle eq makehuman*" /T /F
echo "Makehuman Daemon is down"

call python -m pytest -v --disable-warnings test_main.py::test_applyAndDownload_noMakehuman

call conda deactivate

cd ..
cd ..
echo "Installing npm packages"
call npm install --silent
call npm test --silent
#!/bin/bash
username=$(whoami)
echo Current User is $username

npm test --silent

echo "Booting up Makehuman Daemon"
# source "C:\\Users\\$username\\mambaforge\\etc\\profile.d\\conda.sh"
source /home/$username/mambaforge/etc/profile.d/conda.sh
conda activate makehuman
cd ../makehuman-docker/custom_makehuman/makehuman
python makehuman.py > /dev/null 2>&1 &
MAKEHUMAN_PID=$!

# Attendi 15 secondi per assicurarti che il processo sia avviato
sleep 15
echo "Makehuman Daemon is ready"

cd ../../../pythonServices/3Dify-sliderModule

# Esegui più funzioni di test con pytest
pytest -v --disable-warnings test_main.py::test_scanFace_noImage test_main.py::test_scanFace_correctImage test_main.py::test_scanFace_noFace test_main.py::test_extractFeatures_noImage test_main.py::test_extractFeatures_correctImage test_main.py::test_extractFeatures_noFace test_main.py::test_extractFeatures_lowRes test_main.py::test_customSkin_noImage test_main.py::test_applyAndDownload
sleep 10

# Termina il processo makehuman.py
kill $MAKEHUMAN_PID
echo "Makehuman Daemon is down"

# Esegui un altro test con pytest
pytest -v --disable-warnings test_main.py::test_applyAndDownload_noMakehuman


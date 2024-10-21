# 3Dify Test Suite
## Prerequisites
In order to proceed with the execution of the tests suite, it is necessary to:
1. Install miniforge(https://github.com/conda-forge/miniforge) (install for single user)
2. Add the /condabin folder from the installation path to the system variables by following this [guide](https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)#to-add-a-path-to-the-path-environment-variable) (ONLY WINDOWS)
3. Create a new environment named "makehuman" and activate it by typing **"conda create -n makehuman && conda activate makehuman && conda install python=3.12"**
4. Install in the environment all the packages inside "requirements.txt" by using **"python -m pip install -r requirements.txt"**
5. Execute the test.bat or test.bash script inside the root of the project
brew install --cask miniconda
conda init
conda env create -f environment.yml --prefix ./env -y
conda activate ./env

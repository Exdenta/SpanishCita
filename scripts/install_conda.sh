brew install --cask miniconda
conda init
conda env create -f scripts/environment.yml --prefix ./env -y
conda activate ./env

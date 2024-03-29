# IST-data-science-33

__Important:__

This repository was created in the course Data-Science of the IST Lisbon. The util functions are inspired by the scripts, given by the professor! The DS_chart.py is taken out of the sources. The sources of the course free are aviable under: [Link](http://web.ist.utl.pt/~claudia.antunes/DSLabs/). 

## Setup

From lecture its recommend to use python3.10!

Run `pip install -r requirements.txt` to install dependencies

Or run with conda: 

```bash
conda env create -f environment.yml
conda activate data-science
```

## Datasets

### SET 1: [Health](https://www.kaggle.com/datasets/brandao/diabetes)

### SET 2: [Climate](https://www.kaggle.com/datasets/cdminix/us-drought-meteorological-data)

## Don't rewrite functions, use modules

For using modules, which can be imported in the task, please use the `src/utils` folder.

Then we can include these files by the following commands on top of the python file:

```python
import sys, os

# Add  relative path to the directory
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '..','utils') )
from <Your_Library> import <Your_Function>
```

## Docker application

First create container: 

```bash 
docker build -t anaconda_ds_image .
```

Then run container:

```bash 
sudo chmod +x start-docker.sh
./start-docker.sh
```

Inside of the container, create you env
```bash 
conda env create --file environment.yml
```

__Important: This work directory is mounted into the container! If you run and save plots, they get directly saved here and could overwrite old results!__

## Copy remote files

```bash 
scp username@b:/path/to/file /path/to/destination
```

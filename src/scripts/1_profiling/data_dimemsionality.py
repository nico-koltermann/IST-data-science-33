#!/usr/bin/env python3

import sys, os

# dirty but works for now 
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'utils'))

from general_utils import get_plot_folder_path
from load_data import load_diabetic_data, load_drought_data

from ds_charts import bar_chart
import pandas as pd
import matplotlib.pyplot as plt

def read_data():
    return load_diabetic_data(), load_drought_data()

    # plot(data)

def plot(data):
    plt.figure(figsize=(4,2))
    values = {'nr records': data.shape[0], 'nr variables': data.shape[1]}
    bar_chart(list(values.keys()), list(values.values()), title='Nr of records vs nr variables')
    plt.savefig('%s/%s'  % (get_plot_folder_path(), 'dimensionality')  )
    plt.show()

if __name__ == "__main__":
    data_diabetic, data_drought = read_data()
    plot(data_diabetic)
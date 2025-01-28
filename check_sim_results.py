import os
import csv
import pandas as pd
from pathlib import Path

from simulation_parameters import get_sim_params


# path
base_dir = Path(__file__).parent.absolute()
sim_dir = base_dir.joinpath('Sim_model')
csv_dir = sim_dir.joinpath('csv')
kpi_dir = sim_dir.joinpath('kpi')


def check_results():
    df_res = pd.read_pickle('sim_year_results.pkl')
    list_params = get_sim_params([])
    list_name_new = set(df_res.index)
    list_name_default = set([x[0]['name'] for x in list_params])
    list_name_miss = list_name_default - list_name_new

    with open('list_name_miss.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for item in list_name_miss:
            writer.writerow([item])

    return None



if __name__ == '__main__':
    check_results()

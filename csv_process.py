import os

import pandas as pd
from pathlib import Path


# path
base_dir = Path(__file__).parent.absolute()
sim_dir = base_dir.joinpath('Sim_model')
csv_dir = sim_dir.joinpath('csv')
kpi_dir = sim_dir.joinpath('kpi')


def process_csv():
    all_files = list(os.listdir(csv_dir))
    idx = [x.split('.csv')[0] for x in all_files if x.endswith('.csv')]
    df_cols = pd.read_excel('test_process_data.xlsx', sheet_name='cols', index_col=0)
    df_res = pd.DataFrame(index=idx, columns=list(df_cols.index), dtype=float)
    for fn in all_files:
        if not fn.endswith('.csv'):
            continue
        sim_name = fn.split('.csv')[0]
        with open(csv_dir.joinpath(fn), mode='r') as file:
            res_list = file.read().split(',')
        try:
            csv_data = [float(x) for x in res_list]
        except:
            df_res.loc[sim_name, :] = 0.0
            continue

        df_res.loc[sim_name, :] = csv_data
    df_res.to_pickle('sim_year_results.pkl')
    df_res.to_excel('sim_year_results.xlsx')
    return None


def process_csv_kpi():
    all_files = list(os.listdir(kpi_dir))
    idx = [x.split('.csv')[0] for x in all_files if x.endswith('.csv')]
    df_cols = pd.read_excel('test_process_data.xlsx', sheet_name='cols_kpi', index_col=0)
    df_res = pd.DataFrame(index=idx, columns=list(df_cols.index), dtype=float)
    for fn in all_files:
        if not fn.endswith('.csv'):
            continue
        sim_name = fn.split('.csv')[0]
        with open(kpi_dir.joinpath(fn), mode='r') as file:
            res_list = file.read().split(',')
        try:
            csv_data = [float(x) for x in res_list]
        except:
            df_res.loc[sim_name, :] = 0.0
            continue

        df_res.loc[sim_name, :] = csv_data
    df_res.to_pickle('kpi.pkl')
    df_res.to_excel('kpi.xlsx')
    return None


if __name__ == '__main__':
    process_csv()
    process_csv_kpi()

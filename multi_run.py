from typing import List

import pandas as pd
from pathlib import Path
from multiprocessing import Pool, cpu_count
import subprocess           # to run the TRNSYS simulation
import csv
import datetime
from simulation_parameters import get_sim_params
from data_process import df_process, df_process_kpi

# path
base_dir = Path(__file__).parent.absolute()
sim_dir = base_dir.joinpath('Sim_model')
temp_dir = sim_dir.joinpath('Templates')
csv_dir = sim_dir.joinpath('csv')
kpi_dir = sim_dir.joinpath('kpi')
proc = cpu_count() - 1




def run_simulation():
    pool = Pool(processes=proc)
    existing_files = get_existing_files(csv_dir)
    list_params = get_sim_params(existing_files)
    #one_sim(list_params[0][0],list_params[0][1])

    pool.starmap(one_sim, list_params)
    return None


def trnsys_input(sim_params: dict):
    # Read dck template
    with open(temp_dir.joinpath('CZTtemplate.dck'), 'r') as file_in:
        filedata = file_in.read()
        # replace parameters of template
        for placeholder, value in sim_params.items():
            if placeholder not in ['name', 'folder']:  # Skip 'name' and 'folder'
                filedata = filedata.replace(placeholder, value)

    # save template of simulation
    sim_name = sim_params['name']
    output_filename = f'{sim_name}.dck'
    # Write the modified filedata to the new file
    with open(sim_dir.joinpath(output_filename), 'w') as dckfile_out:
        dckfile_out.write(filedata)
    return None


def trnsys_run_sim(file_name: str):
    subprocess.run(
        [r"C:\TRNSYS18\Exe\TrnEXE64.exe",
         sim_dir.joinpath(f'{file_name}.dck'),
         '/h']
    )
    return None


def create_csv_file(folder_dir: Path, res_list: List, file_name):
    res_list = [str(x) for x in res_list]
    with open(folder_dir.joinpath(f'{file_name}.csv'), mode="w") as file:
        file.write(','.join(res_list))
    return None


def process_data(file_name: str):
    df = pd.read_csv(sim_dir.joinpath(f'{file_name}.out'), sep='\t', header=0)
    # label editing
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    #df.columns = df.columns.str.strip().lower().replace(' ', '_')
    df.drop(0, inplace=True)
    df.index = pd.date_range(start='1/1/2023', periods=df.shape[0], freq='1H')
    res_list = df_process(df)
    return res_list


def process_data_kpi(file_name: str):
    df = pd.read_csv(sim_dir.joinpath(f'{file_name}.out'), delim_whitespace=True)
    res_list = df_process_kpi(df)
    return res_list


def remove_files(file_name: str):
    sim_dir.joinpath(f'{file_name}.out').unlink(missing_ok=True)
    sim_dir.joinpath(f'{file_name}.log').unlink(missing_ok=True)
    sim_dir.joinpath(f'{file_name}.lst').unlink(missing_ok=True)
    sim_dir.joinpath(f'{file_name}.dck').unlink(missing_ok=True)
    sim_dir.joinpath(f'{file_name}.PTI').unlink(missing_ok=True)
    return None


def one_sim(sim_input: dict, sim_name: str):
    remove_sim_data = True  # TODO
    kpi_data = True  # TODO

    start_time = datetime.datetime.now()
    print(f'Start: {sim_name} - Time: {start_time} ')

    trnsys_input(sim_input)
    # run TRNSYS simulation
    trnsys_run_sim(sim_name)
    sim_time = datetime.datetime.now() - start_time  # Measuring time (end point)
    print(f'End: {sim_name} - Sim time: {sim_time}')

    # process data
    results_list = process_data(sim_name)
    # create csv file
    create_csv_file(csv_dir, results_list, sim_name)
    if kpi_data:
        results_list_kpi = process_data_kpi(sim_name)
        create_csv_file(kpi_dir, results_list_kpi, sim_name)
    # remove data
    if remove_sim_data:
        remove_files(sim_name)
    return None

def get_existing_files(csv_dir: Path):
    existing_files = [f.stem for f in csv_dir.glob('*.csv')]
    return existing_files


if __name__ == '__main__':
    # file_name = 'sim000001SIZE50LOSS0LTYPE0REF0Twin120dt30Tsum80Moff0.1E2G1.0N0.11CTRL3'

    # results_list = process_data(file_name)
    # create_csv_file(csv_dir, results_list, file_name)

    # results_list = process_data_kpi(file_name)
    # create_csv_file(kpi_dir, results_list, file_name)

    # remove_files(file_name)

    run_simulation()



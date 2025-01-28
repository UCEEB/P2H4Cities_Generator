import pandas as pd


def df_process(df_raw: pd.DataFrame) -> list:
    df = df_raw.copy()
    df['q_load'] = df['qload_mw']
    df['q_el'] = df['q_el_mw']
    df['q_fuel'] = df['q_peak_source_mw']
    df['q_all'] = df['q_el'] + df['q_fuel']
    df['q_loss'] = df['q_loss_pipe_mw']
    df['el_p2h_load'] = df['p_p2h_mw']

    q_load = round(df['q_load'].sum(), 4)
    q_all = round(df['q_all'].sum(), 4)
    q_el = round(df['q_el'].sum(), 4)
    q_fuel = round(df['q_fuel'].sum(), 4)
    q_loss = round(df['q_loss'].sum(), 4)
    cop = round(df['q_el'].sum() / df['el_p2h_load'].sum(), 4)
    p2h_hours = (df['q_el_mw'] > 0).sum()
    t_czt_in_p2h = round(df.loc[df['q_el_mw'] > 0, 't_prim_ret_c'].mean(), 4)
    t_czt_out_p2h = round(df.loc[df['q_el_mw'] > 0, 't_prim_p2h_sup_c'].mean(), 4)
    el_regulated_price = round(df['pee_reg'].mean(), 4)  # 1000 CZK/MWh  TODO
    gas_regulated_price = round(df['pgas_reg'].mean(), 4)  # 1000 CZK/MWh  TODO
    spot = round(df['price_el_spot_czkpermwh_i'].mean(), 4)
    s_spot_el = df['price_el_spot_czkpermwh_i'] * df['el_p2h_load']
    spot_weighted = s_spot_el.sum() / df['el_p2h_load'].sum()
    spot_specific = 1
    spot_weighted_specific = spot_weighted / spot
    fuel_price_specific = df['price_el_spot_czkpermwh_i'].mean() / df['price_gas_fixed_czkpermwh'].mean()  # TODO

    q_price = round(s_spot_el.sum() / q_el, 4) / spot
    co2_p2h = round((df['ico2_el_kgco2permwh_in'] * df['el_p2h_load']).sum() / df['q_el'].sum(), 4)
    p2h_q_max = round(df['q_el_mw'].max(), 4)
    p2h_el_max = round(df['el_p2h_load'].max(), 4)

    res_list = [q_load, q_all, q_el, q_fuel, q_loss, cop, p2h_hours, t_czt_in_p2h, t_czt_out_p2h,
                spot_specific, spot_weighted_specific, fuel_price_specific, q_price, co2_p2h, p2h_q_max, p2h_el_max,]
    q_all_sum = df['q_all'].sum()
    q_all_per = []
    q_p2h_per = []
    q_fuel_per = []
    t_czt_in_per = []
    t_czt_out_per = []
    t_p2h_out_per = []
    cop_per = []
    for m in range(1, 13):
        q_all_per.append(df.loc[df.index.month == m, 'q_all'].sum() / q_all_sum)
        q_p2h_per.append(df.loc[df.index.month == m, 'q_el'].sum() / q_all_sum)
        q_fuel_per.append(df.loc[df.index.month == m, 'q_fuel'].sum() / q_all_sum)
        t_czt_in_per.append(df.loc[df.index.month == m, 't_prim_sup_c'].mean())
        t_czt_out_per.append(df.loc[df.index.month == m, 't_prim_ret_c'].mean())
        t_p2h_out_per.append(df.loc[df.index.month == m, 't_prim_p2h_sup_c'].mean())
        cop_per.append(df.loc[df.index.month == m, 'q_el'].sum() / df.loc[df.index.month == m, 'el_p2h_load'].sum())

    return res_list + q_all_per + q_p2h_per + q_fuel_per + t_czt_in_per + t_czt_out_per + t_p2h_out_per + cop_per


def df_process_kpi(df_raw: pd.DataFrame) -> list:
    df = df_raw.copy()
    kpi = {
        "Qload": df['Qload_MW'].sum() * 0.0036,
        "Qsource": df['Qsource_MW'].sum() * 0.0036,
        "Qfuel": df['Q_fuel_MW'].sum() * 0.0036,
        "Qel": df['Q_el_MW'].sum() * 0.0036,
        "Qloss": df['Q_loss_pipe_MW'].sum() * 0.0036,
        "P_P2H": df['P_P2H_MW'].sum() * 0.0036,
        "COP": df['Q_el_MW'].sum() / df['P_P2H_MW'].sum(),
        "ratioP2H": df['Q_el_MW'].sum() / df['Qsource_MW'].sum(),
        "ratioLosses": df['Q_loss_pipe_MW'].sum() / df['Qsource_MW'].sum(),
        "Qtotmax": df['Qsource_MW'].max(),
        "Qp2hmax": df['Q_el_MW'].max(),
    }

    time_filter_winter = (df['TIME'] < 3120) | (df['TIME'] > 6168)
    time_filter_summer = (df['TIME'] > 3120) & (df['TIME'] < 6168)

    kpi.update(
        {
        "TsupWMax": df.loc[time_filter_winter, 'T_prim_sup_C'].max(),
        "TsupWMin": df.loc[time_filter_winter, 'T_prim_sup_C'].min(),
        "TsupWAvg": df.loc[time_filter_winter, 'T_prim_sup_C'].mean(),
        "TsupSMax": df.loc[time_filter_summer, 'T_prim_sup_C'].max(),
        "TsupSMin": df.loc[time_filter_summer, 'T_prim_sup_C'].min(),
        "TsupSAvg": df.loc[time_filter_summer, 'T_prim_sup_C'].mean(),
        "TsupSUnc": df.loc[time_filter_summer, 'T_prim_sup_C'].max() - df.loc[
            time_filter_summer, 'T_prim_sup_C'].min(),
        "TretWMax": df.loc[time_filter_winter, 'T_prim_ret_C'].max(),
        "TretWMin": df.loc[time_filter_winter, 'T_prim_ret_C'].min(),
        "TretWAvg": df.loc[time_filter_winter, 'T_prim_ret_C'].mean(),
        "TretSMax": df.loc[time_filter_summer, 'T_prim_ret_C'].max(),
        "TretSMin": df.loc[time_filter_summer, 'T_prim_ret_C'].min(),
        "TretSAvg": df.loc[time_filter_summer, 'T_prim_ret_C'].mean(),
        "TretSUnc": df.loc[time_filter_summer, 'T_prim_ret_C'].max() - df.loc[
            time_filter_summer, 'T_prim_ret_C'].min(),
        "dTW": (df.loc[time_filter_winter, 'T_prim_sup_C'] - df.loc[time_filter_winter, 'T_prim_ret_C']).mean(),
        "dTWstd": (df.loc[time_filter_winter, 'T_prim_sup_C'] - df.loc[time_filter_winter, 'T_prim_ret_C']).std(),
        "dTS": (df.loc[time_filter_summer, 'T_prim_sup_C'] - df.loc[time_filter_summer, 'T_prim_ret_C']).mean(),
        "dTSstd": (df.loc[time_filter_summer, 'T_prim_sup_C'] - df.loc[time_filter_summer, 'T_prim_ret_C']).std(),
        }
    )

    return list(kpi.values())

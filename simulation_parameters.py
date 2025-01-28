from typing import Tuple

import numpy as np
import time


def get_sim_params(existing_files):
	list_params = []  # dict of all simulation
	#network typology settings
	list_size = np.array([50, 150 , 300])  # [TJ] size of the system

	list_L_primPipe = [[1500, 3000,7500],[3000, 6000,15000]]  # primary pipe lenght per typology
	list_L_sec1Pipe = [[500, 1000, 1500],[1000, 2000, 3000]] # sec 1 pipe lenght per typology
	list_L_sec2Pipe = [[500, 1000, 1500],[1000, 2000, 3000]]  # sec 2 pipe lenght per typology
	list_L_sec3Pipe = [[500, 1000, 1500],[1000, 2000, 3000]]  # sec 3 pipe lenght per typology

	list_k_primPipe = [0.4,0.7]  # primary pipe loss coef per network quality
	list_k_sec1Pipe = [0.4,0.7]  # sec 1 pipe loss coef per network quality y
	list_k_sec2Pipe = [0.4,0.7]   # sec 2 pipe loss coef per network quality
	list_k_sec3Pipe = [0.4,0.7]   # sec 3 pipe loss coef per network quality

	#load settings
	list_load_profiles=['ExampleLoad\Rezidence_0%_Komerce_100%_TV_30%_VYT_70%.csv',
	                    'ExampleLoad\Rezidence_0%_Komerce_100%_TV_40%_VYT_60%.csv',
	                    'ExampleLoad\Rezidence_0%_Komerce_100%_TV_50%_VYT_50%.csv',
	                    'ExampleLoad\Rezidence_0%_Komerce_100%_TV_60%_VYT_40%.csv',
	                    'ExampleLoad\Rezidence_0%_Komerce_100%_TV_70%_VYT_30%.csv',
	                    'ExampleLoad\Rezidence_50%_Komerce_50%_TV_30%_VYT_70%.csv',
	                    'ExampleLoad\Rezidence_50%_Komerce_50%_TV_40%_VYT_60%.csv',
	                    'ExampleLoad\Rezidence_50%_Komerce_50%_TV_50%_VYT_50%.csv',
	                    'ExampleLoad\Rezidence_50%_Komerce_50%_TV_60%_VYT_40%.csv',
	                    'ExampleLoad\Rezidence_50%_Komerce_50%_TV_70%_VYT_30%.csv',
	                    'ExampleLoad\Rezidence_100%_Komerce_0%_TV_30%_VYT_70%.csv',
	                    'ExampleLoad\Rezidence_100%_Komerce_0%_TV_40%_VYT_60%.csv',
	                    'ExampleLoad\Rezidence_100%_Komerce_0%_TV_50%_VYT_50%.csv',
	                    'ExampleLoad\Rezidence_100%_Komerce_0%_TV_60%_VYT_40%.csv',
	                    'ExampleLoad\Rezidence_100%_Komerce_0%_TV_70%_VYT_30%.csv']

	list_peak2load = [
		0.134407587, 0.122401526, 0.110395466, 0.098389405, 0.086383345,
		0.111079279, 0.101522661, 0.091966044, 0.082409427, 0.073013349,
		0.113740401, 0.104389121, 0.095037842, 0.085686562, 0.076335283
	]

	list_n_HP = [
		[
			0.11, 0.15, 0.22, 0.29, 0.39,
			0.12, 0.17, 0.23, 0.31, 0.41,
			0.12, 0.18, 0.24, 0.32, 0.42
		],
		[
			1, 1, 1, 1, 1,
			1, 1, 1, 1, 1,
			1, 1, 1, 1, 1
		]
	]
	list_n_HP = [
		[
			0.11, 0.15, 0.22, 0.29, 0.39,
			0.12, 0.17, 0.23, 0.31, 0.41,
			0.12, 0.18, 0.24, 0.32, 0.42
		],
		[
			1, 1, 1, 1, 1,
			1, 1, 1, 1, 1,
			1, 1, 1, 1, 1
		]
	]


	#Temperature settings
	list_Ts_peak = [120,105,90,70,65]
	list_dT_Prim = [30, 25, 20, 20, 25]
	list_dT_Sec = [30, 25,20,20,20,20]

	list_Tsp_offseas = [80, 70, 60]
	list_Msp_cutoff = [0.1, 0.07,0.05]

	#integration scenario settings
	list_P2H_scenario = [2,3]
	# 0 -no P2H,
	# 1- electric boiler,
	# 2 - AWHP,
	# 3 - WWHP
	list_Tsp_biv = [0,5,5]


	list_P2H_Tariff = [3, 3]  # selection of tariff #1 single tarrif, #2 ToU tarrif #3 spot tarrif
	list_P2H_CtrTariff = [1,3]  # selection of control #1 control based on temp, # ctrl based on ToU tarrif, #ctrl based  on #3 spot tarrif


	list_perf_map_AWHP = ['PerformanceMaps\AWHP\Trane_Qk0.823_Pe0.324.dat',
						  'PerformanceMaps\AWHP\Trane_Qk0.823_Pe0.324.dat',
						  'PerformanceMaps\AWHP\Trane_Qk0.823_Pe0.324.dat']
	list_perf_map_WWHP = ['PerformanceMaps\WWHP\Qk1.1_Pe1.04_85C_60C.txt',
						  'PerformanceMaps\WWHP\Qk1.1_Pe1.04_85C_60C.txt',
						  'PerformanceMaps\WWHP\Qk1.1_Pe1.04_85C_60C.txt']
	list_Tw = [10, 20]
	list_Tamp = [12, 0]


	list_Qml_WWHP = [1.1, 1.1, 1.1]  # [1,1.1,1.21] TO BE CHECKED WITH NIKOLE IF STILL NEEDED
	list_Pml_WWHP = [1.04, 1.04, 1.04]  # [1,1.04,1.07] TO BE CHECKED WITH NIKOLE IF STILL NEEDED



	list_weather = ['Weather\CZE_PM_Praha-Karlov-Klementinum.115190_TMYx.2007-2021.epw',
					'Weather\CZE_BK_Brno.Turany.117230_TMYx.2007-2021.epw',
					'Weather\CZE_UK_Usti.nad.Labem.115020_TMYx.2007-2021.epw',
					'Weather\CZE_VK_Dolni.Benesov.117250_TMYx.2007-2021.epw']

	list_gas_price_ml = [3500, 2333.33333, 1750,1400,1000]
	list_el_price_ml = [3500, 3500, 3500,3500,3500]
	list_coal_price_ml = [1400, 1400]
	list_el_CO2int_ml = [1, 0.8]
	list_PV_area = [0, 8000, 16000]






	# initial values (maybe unused/rewriting during model/scenario definition)
	size = list_size[1]
	P2H_scenario = list_P2H_scenario[0]
	P2H_Tariff = list_P2H_Tariff[1]  #
	P2H_CtrTariff = list_P2H_CtrTariff[1]  #
	Ts_peak = list_Ts_peak[0]  #
	Tsp_offseas = list_Tsp_offseas[0]  #
	Tsp_biv = list_Tsp_biv[0]  #

	dT_Prim = list_dT_Prim[0]

	dT_Sec = list_dT_Sec[0]
	n_HP = list_n_HP[0]


	weather = list_weather[0]
	perf_map_AWHP = list_perf_map_AWHP[0]
	perf_map_WWHP = list_perf_map_WWHP[0]

	PV_area = list_PV_area[0]
	Tw = list_Tw[1]
	Tamp = list_Tamp[1]
	Qml = list_Qml_WWHP[0]
	Pml = list_Pml_WWHP[0]
	Msp_cutoff = list_Msp_cutoff[0]

	# regulated price CZK/MWh
	el_price_ml = list_el_price_ml[0]
	elfix_price_ml = 4000
	gas_price_ml = list_gas_price_ml[0]
	coal_price_ml = 1  # not in use in this case
	biomass_price_ml = 1  # not in use in this case
	el_CO2int_ml = list_el_CO2int_ml[0]

	Pee_reg = 1000
	Pgas_reg = 1000
	Pcoal_reg = 0
	Pbiomass_reg = 0

	sim_nb = 0
	sim_nb_finished = 0
	folderlimit = 100
	# Looping through Each of Combinations (List of Parameters)
	start_time_tot = time.time()
	# Measuring time (start point)

	# for PV_area in list_PV_area:
	# for weather in list_weather:
	# for gas_price_ml in list_gas_price_ml:
	#
	for Typ, size in enumerate(list_size): #typology 50 150 300
		for Loss, k_primPipe in enumerate(list_k_primPipe): # high low losses
			for Load, load_profile in enumerate(list_load_profiles): #15 loads types
				for S, P2H_scenario in enumerate(list_P2H_scenario): #scenarios
					for Tseas, Ts_peak in enumerate(list_Ts_peak):
						for Tofseas, Tsp_offseas in enumerate(list_Tsp_offseas):
							for P2H_CtrTariff in list_P2H_CtrTariff:
								for n_HP_index in range(len(list_n_HP)):
									for E2G, el_price_ml in enumerate(list_el_price_ml):
										for Tw in list_Tw:
												load2peak = list_peak2load[Load]
												# excluding scenarios if conditions are not satisfied

												# if P2H_scenario==0 and P2H_Tariff>1: #baseline without spot calculation
												#     continue

												if P2H_scenario < 3 and Tw > list_Tw[0]:
													continue
												if S == 0 and n_HP_index == 1: #no sizing for baseline
													continue
												if (Tsp_offseas+10)>Ts_peak: #avoiding nonsense temperature settings
													continue
												# if typology==0 and PV_area>0: #do not calculate PV for mid-town typology
												#     continue

												# if typology>0 and P2H_scenario == 3: #do not calculate WWHP for the small-town and campus typology
												#     continue

												# condition for interupted simulations. If you want to start again, set sim_nb_finished = 0
												sim_nb = sim_nb + 1
												if sim_nb <= sim_nb_finished:
													continue

												# typology definition

												L_primPipe = list_L_primPipe[Loss][Typ]
												L_sec1Pipe = list_L_sec1Pipe[Loss][Typ]
												L_sec2Pipe = list_L_sec2Pipe[Loss][Typ]
												L_sec3Pipe = list_L_sec3Pipe[Loss][Typ]

												k_primPipe = list_k_primPipe[Loss]
												k_sec1Pipe = list_k_sec1Pipe[Loss]
												k_sec2Pipe = list_k_sec2Pipe[Loss]
												k_sec3Pipe = list_k_sec3Pipe[Loss]


												#     #Global baseline
												# else: #baseline
												Ts_peak = list_Ts_peak[Tseas]
												dT_Prim = list_dT_Prim[Tseas]
												dT_Sec = list_dT_Sec[Tseas] #

												Tsp_offseas = list_Tsp_offseas[Tofseas]  #
												Msp_cutoff=list_Msp_cutoff[Tofseas]

												n_HP=list_n_HP[n_HP_index][Load]
												# turn off the bivalent setpoint when WHPP scenario is applied
												Tsp_biv = list_Tsp_biv[1] if (P2H_scenario == 3) else list_Tsp_biv[0]
												Tamp = list_Tamp[0] if (Tw == list_Tw[0]) else list_Tamp[1]
												E2Gratio= list_el_price_ml[E2G] / list_gas_price_ml[E2G]
												gas_price_ml = list_gas_price_ml[E2G]
												# scenario ID generator
												if P2H_scenario == 1:
													P2HLab = 'ELBO'
												elif P2H_scenario == 2:
													P2HLab = 'AWHP'
												elif P2H_scenario == 3:
													P2HLab = 'WWHP'
												else:
													P2HLab = 'REF'

												outid = str(sim_nb)
												outid = outid.rjust(6, '0')

												scenarioID = 'sim' + str(outid) + 'SIZE' + str(size) +'LOSS' + str(Loss) +'LTYPE' + str(Load)  + P2HLab + str(P2H_scenario) + 'Twin' + str(
													Ts_peak) + 'dt' + str(dT_Prim) + 'Tsum' + str(Tsp_offseas)+'Moff' + str(
													Msp_cutoff)+ 'E2G' + str(E2Gratio) + 'N' + str(n_HP) + 'CTRL' + str(
													P2H_Tariff)

												scenarioID = scenarioID + 'Ta' + 'Prague' if (
															P2H_scenario == 2) else scenarioID
												scenarioID = scenarioID + 'Tw' + str(Tw) if (P2H_scenario == 3) else scenarioID

												if scenarioID in existing_files:
													continue

												
												filename_out = 'Outputs\sim' + outid + 'model' + str(size) + str(
													scenarioID) + '.txt'

												foldername = 'Outputs' + str(folderlimit)
												if sim_nb >= folderlimit:
													folderlimit = folderlimit + 100

												one_param = {
													'name': str(scenarioID),
													'folder': str(foldername),
													'py_load': str(size),
													'py_profile': str(load_profile),
													'py_peak': str(load2peak),
													'py_P2H_scenario': str(P2H_scenario),
													'py_P2H_Tariff': str(P2H_Tariff),
													'py_P2H_CtrTariff': str(P2H_CtrTariff),
													'py_Ts_peak': str(Ts_peak),
													'py_Tsp_offseas': str(Tsp_offseas),
													'py_Tsp_biv': str(Tsp_biv),
													'py_dT_Prim': str(dT_Prim),
													'py_dT_Sec': str(dT_Sec),
													'py_n_HP': str(n_HP),
													'py_L_primPipe': str(L_primPipe),
													'py_L_sec1Pipe': str(L_sec1Pipe),
													'py_L_sec2Pipe': str(L_sec2Pipe),
													'py_L_sec3Pipe': str(L_sec3Pipe),
													'py_k_primPipe': str(k_primPipe),
													'py_k_sec1Pipe': str(k_sec1Pipe),
													'py_k_sec2Pipe': str(k_sec2Pipe),
													'py_k_sec3Pipe': str(k_sec3Pipe),
													'py_weather': str(weather),
													'py_perf_map_AWHP': str(perf_map_AWHP),
													'py_perf_map_WWHP': str(perf_map_WWHP),
													'py_el_CO2int_ml': str(el_CO2int_ml),
													'py_PV_area': str(PV_area),
													'py_Twater_source': str(Tw),
													'py_Qml': str(Qml),
													'py_Pml': str(Pml),
													'py_gas_price_ml': str(gas_price_ml),
													'py_coal_price_ml': str(coal_price_ml),
													'py_biomass_price_ml': str(biomass_price_ml),
													'py_el_price_ml': str(el_price_ml),
													'py_elfix_price_ml': str(elfix_price_ml),
													'py_Pee_reg': str(Pee_reg),
													'py_Pgas_reg': str(Pgas_reg),
													'py_Pcoal_reg': str(Pcoal_reg),
													'py_Pbiomass_reg': str(Pbiomass_reg),
													'py_Tamp': str(Tamp),
													'py_Msp_cutoff': str(Msp_cutoff),
												}
												list_params.append((one_param, one_param['name']))  # dict of all simulation
	return list_params


if __name__ == '__main__':
	list_params = get_sim_params()
	print()


import pandas as pd, numpy as np

dataset = pd.read_csv("bweb_1t_AC_101020181938.csv", encoding = 'latin1', sep = ";", low_memory = False)

ds_aptos = pd.pivot_table(dataset,
                          index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                          values = ["QT_APTOS"],
                          columns = ["NR_ZONA", "NR_SECAO"], 
                          fill_value = 0
                          )

ds_abst = pd.pivot_table(dataset,
                          index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                          values = ["QT_ABSTENCOES"],
                          columns = ["NR_ZONA", "NR_SECAO"], 
                          fill_value = 0
                          )

ds_aptos["TOTAL_APTOS"] = round(ds_aptos.sum(axis = 1))
ds_aptos = ds_aptos[["TOTAL_APTOS"]]

ds_abst["TOTAL_ABSTENCOES"] = round(ds_abst.sum(axis = 1))
ds_abst = ds_abst[["TOTAL_ABSTENCOES"]]

ds_aptos_abtencoes = pd.concat([ds_aptos, ds_abst], axis = 1, join = "inner")
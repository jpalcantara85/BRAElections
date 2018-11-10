import pandas as pd, numpy as np, glob

folder_ = glob.glob("/Users/jpalcantara/Desktop/Trade in Elections/Files/2T 2018" + "/*.csv")
list_ = []

frame_pres = []

for file_ in folder_:
    df = pd.read_csv(file_, encoding = 'latin1', sep = ";")
    list_.append(df)
      
for i in list_:  
    ds_pres = i[i.CD_CARGO_PERGUNTA == 1]

    ds_pres_pivot = pd.pivot_table(ds_pres,
                                   index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values = ["QT_VOTOS"], 
                                   columns = ["NR_PARTIDO", "NM_VOTAVEL"],
                                   aggfunc = np.sum,
                                   fill_value = 0
                                   )

    ds_aptos = pd.pivot_table(i,
                              index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                              values = ["QT_APTOS"],
                              columns = ["NR_ZONA", "NR_SECAO"], 
                              fill_value = 0
                              )

    ds_abst = pd.pivot_table(i,
                             index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                             values = ["QT_ABSTENCOES"],
                             columns = ["NR_ZONA", "NR_SECAO"], 
                             fill_value = 0
                             )

    ds_aptos["TOTAL_APTOS"] = round(ds_aptos.sum(axis = 1))
    ds_aptos = ds_aptos[["TOTAL_APTOS"]]

    ds_abst["TOTAL_ABSTENCOES"] = round(ds_abst.sum(axis = 1))
    ds_abst = ds_abst[["TOTAL_ABSTENCOES"]]

    ds_aptos_abstencoes = pd.concat([ds_aptos, ds_abst], axis = 1, join = "inner")

    ds_pres_final = pd.concat([ds_pres_pivot, ds_aptos_abstencoes], axis = 1, join = "inner")
    
    frame_pres.append(ds_pres_final)

ds_pres_2018 = pd.concat(frame_pres)

ds_pres_2018.to_csv('2T_pres_2018.csv')
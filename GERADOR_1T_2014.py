import pandas as pd, numpy as np, glob

folder_ = glob.glob("/Users/jpalcantara/Desktop/Trade in Elections/Files/1T 2014" + "/*.txt")
list_ = []

frame_pres = []
frame_sen = []
frame_gov = []
frame_depfed = []
frame_depest = []

for file_ in folder_:
    df = pd.read_csv(file_, encoding = 'latin1', sep = ";")
    list_.append(df)
 
#dataset1 = pd.read_csv("bweb_1t_AC_14102014131600.txt", encoding = 'latin1', sep = ";", low_memory = False)
#dataset2 = pd.read_csv("bweb_1t_AL_14102014131724.txt", encoding = 'latin1', sep = ";", low_memory = False)
#list_ = [dataset1, dataset2]
      
for i in list_:
    i.columns = ["DT_GERACAO", "HH_GERACAO", "CD_PLEITO", "CD_ELEICAO", "SG_ UF", "CD_CARGO_PERGUNTA", "DS_CARGO_PERGUNTA", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "NR_PARTIDO", "NM_PARTIDO", "CD_MUNICIPIO", "NM_MUNICIPIO", "X", "QT_APTOS", "QT_ABSTENCOES", "QT_COMPARECIMENTO", "CD_PLEITO", "CD_TIPO_URNA", "DS_TIPO_URNA", "NR_VOTAVEL", "NM_VOTAVEL", "QT_VOTOS", "CD_TIPO_VOTAVEL", "NR_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA", "CD_FLASHCARD_URNA_EFETIVADA", "DS_CARGO_PERGUNTA_SECAO"]
    ds_pres = i[i.CD_CARGO_PERGUNTA == 1]
    ds_gov = i[i.CD_CARGO_PERGUNTA == 3]
    ds_sen = i[i.CD_CARGO_PERGUNTA == 5]
    ds_depfed = i[i.CD_CARGO_PERGUNTA == 6]
    ds_depest = i[i.CD_CARGO_PERGUNTA == 7]

    ds_pres_pivot = pd.pivot_table(ds_pres,
                                   index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values = ["QT_VOTOS"], 
                                   columns = ["NR_PARTIDO", "NM_VOTAVEL"],
                                   aggfunc = np.sum,
                                   fill_value = 0
                                   )

    ds_gov_pivot = pd.pivot_table(ds_gov,
                                   index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values = ["QT_VOTOS"], 
                                   columns = ["NR_PARTIDO", "NM_PARTIDO"],
                                   aggfunc = np.sum,
                                   fill_value = 0
                                   )

    ds_sen_pivot = pd.pivot_table(ds_sen,
                                   index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values = ["QT_VOTOS"], 
                                   columns = ["NR_PARTIDO", "NM_PARTIDO"],
                                   aggfunc = np.sum,
                                   fill_value = 0
                                   )

    ds_depfed_pivot = pd.pivot_table(ds_depfed,
                                   index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values = ["QT_VOTOS"], 
                                   columns = ["NR_PARTIDO", "NM_PARTIDO"],
                                   aggfunc = np.sum,
                                   fill_value = 0
                                   )

    ds_depest_pivot = pd.pivot_table(ds_depest,
                                   index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values = ["QT_VOTOS"], 
                                   columns = ["NR_PARTIDO", "NM_PARTIDO"],
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
    ds_gov_final = pd.concat([ds_gov_pivot, ds_aptos_abstencoes], axis = 1, join = "inner")
    ds_sen_final = pd.concat([ds_sen_pivot, ds_aptos_abstencoes], axis = 1, join = "inner")
    ds_depfed_final = pd.concat([ds_depfed_pivot, ds_aptos_abstencoes], axis = 1, join = "inner")
    ds_depest_final = pd.concat([ds_depest_pivot, ds_aptos_abstencoes], axis = 1, join = "inner")

    frame_pres.append(ds_pres_final)
    frame_gov.append(ds_gov_final)
    frame_sen.append(ds_sen_final)
    frame_depfed.append(ds_depfed_final)
    frame_depest.append(ds_depest_final)

ds_pres_2014 = pd.concat(frame_pres)
ds_gov_2014 = pd.concat(frame_gov)
ds_sen_2014 = pd.concat(frame_sen)
ds_depfed_2014 = pd.concat(frame_depfed)
ds_depest_2014 = pd.concat(frame_depest)

ds_pres_2014.to_csv("1T_pres_2014.csv")
ds_gov_2014.to_csv("1T_gov_2014.csv")
ds_sen_2014.to_csv("1T_sen_2014.csv")
ds_depfed_2014.to_csv("1T_depest_2014.csv")
ds_depest_2014.to_csv("1T_depfed_2014.csv")
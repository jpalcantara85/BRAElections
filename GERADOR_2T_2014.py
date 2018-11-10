import pandas as pd, numpy as np, glob

folder_ = glob.glob("/Users/jpalcantara/Desktop/Trade in Elections/Files/2T 2014" + "/*.txt")
list_ = []

frame_pres = []

for file_ in folder_:
    df = pd.read_csv(file_, encoding = 'latin1', sep = ";")
    list_.append(df)
 
for i in list_:
    i.columns = ["DT_GERACAO", "HH_GERACAO", "CD_PLEITO", "CD_ELEICAO", "SG_ UF", "CD_CARGO_PERGUNTA", "DS_CARGO_PERGUNTA", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "NR_PARTIDO", "NM_PARTIDO", "CD_MUNICIPIO", "NM_MUNICIPIO", "X", "QT_APTOS", "QT_ABSTENCOES", "QT_COMPARECIMENTO", "CD_PLEITO", "CD_TIPO_URNA", "DS_TIPO_URNA", "NR_VOTAVEL", "NM_VOTAVEL", "QT_VOTOS", "CD_TIPO_VOTAVEL", "NR_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA", "CD_FLASHCARD_URNA_EFETIVADA", "DS_CARGO_PERGUNTA_SECAO"]
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

ds_pres_2014 = pd.concat(frame_pres)

ds_pres_2014.to_csv("2T_pres_2014.csv")
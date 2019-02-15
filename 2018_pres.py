import pandas as pd, numpy as np, glob

df = pd.read_csv("/Users/jpalcantara/Downloads/votacao_secao_2018_BR/votacao_secao_2018_BR.csv", encoding = 'latin1', sep = ";")

df_1T = df[df["NR_TURNO"] == 1]
df_2T = df[df["NR_TURNO"] == 2]

df_pres_1T_votos = pd.pivot_table(df_1T,
                                  index      =   ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                  values     =   ["QT_VOTOS"], 
                                  columns    =   ["NR_VOTAVEL"],
                                  aggfunc    =   np.sum,
                                  fill_value =   0
                                  )

df_pres_2T_votos = pd.pivot_table(df_2T,
                                  index      =   ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                  values     =   ["QT_VOTOS"], 
                                  columns    =   ["NR_VOTAVEL"],
                                  aggfunc    =   np.sum,
                                  fill_value =   0
                                  )

###############################################################################

ds = pd.read_csv("/Users/jpalcantara/Downloads/detalhe_votacao_munzona_2018/detalhe_votacao_munzona_2018_BR.csv", encoding = 'latin1', sep = ";", index_col = False)
ds = ds[ds["SG_UF"] != "ZZ"]

ds_1T = ds[ds["NR_TURNO"] == 1]
ds_2T = ds[ds["NR_TURNO"] == 2]

ds_pres_1T_brancos_nulos_abstencoes = pd.pivot_table(ds_1T,
                                                     index        =   ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                                     values       =   ["QT_VOTOS_NULOS", "QT_VOTOS_BRANCOS", "QT_APTOS_TOT", "QT_COMPARECIMENTO", "QT_ABSTENCOES"], 
                                                     aggfunc      =   np.sum,
                                                     fill_value   =   0
                                                     )

ds_pres_2T_brancos_nulos_abstencoes = pd.pivot_table(ds_2T,
                                                     index        =   ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                                     values       =   ["QT_VOTOS_NULOS", "QT_VOTOS_BRANCOS", "QT_APTOS_TOT", "QT_COMPARECIMENTO", "QT_ABSTENCOES"], 
                                                     aggfunc      =   np.sum,
                                                     fill_value   =   0
                                                     )

###############################################################################

ds_pres_1T = pd.concat([df_pres_1T_votos, ds_pres_1T_brancos_nulos_abstencoes], axis = 1, join = "inner")
ds_pres_2T = pd.concat([df_pres_2T_votos, ds_pres_2T_brancos_nulos_abstencoes], axis = 1, join = "inner")

ds_pres_1T.to_csv("/Users/jpalcantara/Desktop/2018_pres_1T.csv")
ds_pres_2T.to_csv("/Users/jpalcantara/Desktop/2018_pres_2T.csv")
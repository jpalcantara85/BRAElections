import pandas as pd, numpy as np, glob

header1 = ["DT_GERACAO", "HR_GERACAO", "ANO_ELEICAO", "NUM_TURNO", "DESCR_ELEICAO", "SG_UF", "SIGLA_UE", "CD_MUNICIPIO", "NM_MUNICIPIO", "NUM_ZONA", "NUM_SECAO", "CD_CARGO", "DESCR_CARGO", "NUM_VOTAVEL", "QT_VOTOS"]

df = pd.read_csv("/Users/jpalcantara/Downloads/votacao_secao_2014_BR/votacao_secao_2014_BR.txt", encoding = 'latin1', sep = ";", names = header1)

df_1T = df[df["NUM_TURNO"] == 1]
df_2T = df[df["NUM_TURNO"] == 2]

df_pres_1T_votos = pd.pivot_table(df_1T,
                                  index      =   ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                  values     =   ["QT_VOTOS"], 
                                  columns    =   ["NUM_VOTAVEL"],
                                  aggfunc    =   np.sum,
                                  fill_value =   0
                                  )

df_pres_2T_votos = pd.pivot_table(df_2T,
                                  index      =   ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                  values     =   ["QT_VOTOS"], 
                                  columns    =   ["NUM_VOTAVEL"],
                                  aggfunc    =   np.sum,
                                  fill_value =   0
                                  )

###############################################################################

header2 = ["DATA_GERACAO", "HORA_GERACAO", "ANO_ELEICAO", "NUM_TURNO", "DESCRICAO_ELEICAO", "SIGLA_UF", "SIGLA_UE", "CD_MUNICIPIO", "NM_MUNICIPIO", "NUMERO_ZONA", "CODIGO_CARGO", "DESCRICAO_CARGO", "QTD_APTOS", "QTD_SECOES", "QTD_SECOES_AGREGADAS", "QTD_APTOS_TOT", "QTD_SECOES_TOT", "QTD_COMPARECIMENTO", "QTD_ABSTENCOES", "QTD_VOTOS_NOMINAIS", "QTD_VOTOS_BRANCOS", "QTD_VOTOS_NULOS", "QTD_VOTOS_LEGENDA", "QTD_VOTOS_ANULADOS_APU_SEP", "DATA_ULT_TOTALIZACAO", "HORA_ULT_TOTALIZACAO", "X.1" , "X.2"]

ds = pd.read_csv("/Users/jpalcantara/Downloads/detalhe_votacao_munzona_2014/detalhe_votacao_munzona_2014_BR.txt", encoding = 'latin1', sep = ";", names = header2, index_col = False)
ds = ds[ds["SIGLA_UF"] != "ZZ"]

ds_1T = ds[ds["NUM_TURNO"] == 1]
ds_2T = ds[ds["NUM_TURNO"] == 2]

ds_pres_1T_brancos_nulos_abstencoes = pd.pivot_table(ds_1T,
                                                     index        =   ["SIGLA_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                                     values       =   ["QTD_VOTOS_NULOS", "QTD_VOTOS_BRANCOS", "QTD_APTOS_TOT", "QTD_COMPARECIMENTO", "QTD_ABSTENCOES"], 
                                                     aggfunc      =   np.sum,
                                                     fill_value   =   0
                                                     )

ds_pres_2T_brancos_nulos_abstencoes = pd.pivot_table(ds_2T,
                                                     index        =   ["SIGLA_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                                     values       =   ["QTD_VOTOS_NULOS", "QTD_VOTOS_BRANCOS", "QTD_APTOS_TOT", "QTD_COMPARECIMENTO", "QTD_ABSTENCOES"], 
                                                     aggfunc      =   np.sum,
                                                     fill_value   =   0
                                                     )

###############################################################################

ds_pres_1T = pd.concat([df_pres_1T_votos, ds_pres_1T_brancos_nulos_abstencoes], axis = 1, join = "inner")
ds_pres_2T = pd.concat([df_pres_2T_votos, ds_pres_2T_brancos_nulos_abstencoes], axis = 1, join = "inner")

ds_pres_1T.to_csv("/Users/jpalcantara/Desktop/2014_pres_1T.csv")
ds_pres_2T.to_csv("/Users/jpalcantara/Desktop/2014_pres_2T.csv")
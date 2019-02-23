import pandas as pd, numpy as np, glob

folder0 = glob.glob("/Users/jpalcantara/Downloads/votacao_candidato_munzona_2002" + "/*.txt")
list0 = []

for file in folder0:
    df0 = pd.read_csv(file, encoding = 'latin1', sep = ";", header = None)
    list0.append(df0)
    
df0 = pd.concat(list0, ignore_index = True) 
df0.columns = ["DT", "HR", "ANO", "NR_TURNO", "X4", "SG_UF", "X6", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "CD_CARGO", "NR_CAND", "CD_CAND", "NM_CAND", "NM_URNA", "DS_CARGO", "X16", "X17", "X18", "DS_CAND", "CD_RESULT", "DS_RESULT", "NR_PARTIDO", "SG_PARTIDO", "NM_PARTIDO", "X25", "NM_COLIG", "PART_COLIG", "QT_VOTOS"]

ds_pres0    = df0[df0["CD_CARGO"] == 1]
ds_gov0     = df0[df0["CD_CARGO"] == 3]
ds_sen0     = df0[df0["CD_CARGO"] == 5]
ds_depfed0  = df0[df0["CD_CARGO"] == 6]
ds_depest0  = df0[df0["CD_CARGO"] == 7]
ds_depdis0  = df0[df0["CD_CARGO"] == 8]

ds_pres_1T0 = ds_pres0[ds_pres0["NR_TURNO"] == 1]
ds_pres_2T0 = ds_pres0[ds_pres0["NR_TURNO"] == 2]
ds_depfed0 = pd.concat([ds_depfed0, ds_depdis0]) 

ds_pres_1T_pivot0    =   pd.pivot_table(ds_pres_1T0,
                                   index = ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values = ["QT_VOTOS"], 
                                   columns = ["NR_PARTIDO", "NM_PARTIDO"],
                                   aggfunc = np.sum,
                                   fill_value = 0
                                   )

ds_pres_2T_pivot0    =   pd.pivot_table(ds_pres_2T0,
                                   index = ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values = ["QT_VOTOS"], 
                                   columns = ["NR_PARTIDO", "NM_PARTIDO"],
                                   aggfunc = np.sum,
                                   fill_value = 0
                                   )

ds_gov_pivot0         =   pd.pivot_table(ds_gov0,
                                   index = ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values = ["QT_VOTOS"], 
                                   columns = ["NR_PARTIDO", "NM_PARTIDO"],
                                   aggfunc = np.sum,
                                   fill_value = 0
                                   )

ds_sen_pivot0         =   pd.pivot_table(ds_sen0,
                                   index = ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values = ["QT_VOTOS"], 
                                   columns = ["NR_PARTIDO", "NM_PARTIDO"],
                                   aggfunc = np.sum,
                                   fill_value = 0
                                   )

ds_depfed_pivot0      =   pd.pivot_table(ds_depfed0,
                                   index = ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values = ["QT_VOTOS"], 
                                   columns = ["NR_PARTIDO", "NM_PARTIDO"],
                                   aggfunc = np.sum,
                                   fill_value = 0
                                   )

ds_depest_pivot0      =   pd.pivot_table(ds_depest0,
                                   index = ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values = ["QT_VOTOS"], 
                                   columns = ["NR_PARTIDO", "NM_PARTIDO"],
                                   aggfunc = np.sum,
                                   fill_value = 0
                                   )

###############################################################################

folder1 = glob.glob("/Users/jpalcantara/Downloads/detalhe_votacao_munzona_2002" + "/*.txt")
list1 = []

for file in folder1:
    df1 = pd.read_csv(file, encoding = 'latin1', sep = ";", header = None)
    list1.append(df1)
    
df1 = pd.concat(list1, ignore_index = True) 
df1.columns = ["DT", "HR", "ANO", "NR_TURNO", "X4", "SG_UF", "X6", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "CD_CARGO", "DS_CARGO", "X12", "QT_SECOES", "X14", "QT_APTOS", "X16", "QT_COMPARECIMENTOS", "QT_ABST", "QT_VOTOS", "QT_BRANCOS", "QT_NULOS", "QT_LEGEND", "X23", "X24", "X25"]

ds_pres1    = df1[df1["CD_CARGO"] == 1]
ds_gov1     = df1[df1["CD_CARGO"] == 3]
ds_sen1     = df1[df1["CD_CARGO"] == 5]
ds_depfed1  = df1[df1["CD_CARGO"] == 6]
ds_depest1  = df1[df1["CD_CARGO"] == 7]
ds_depdis1  = df1[df1["CD_CARGO"] == 8]

ds_pres_1T1 = ds_pres1[ds_pres1["NR_TURNO"] == 1]
ds_pres_2T1 = ds_pres1[ds_pres1["NR_TURNO"] == 2]
ds_depfed1  = pd.concat([ds_depfed1, ds_depdis1])

ds_pres_1T_pivot1   = pd.pivot_table(ds_pres_1T1,
                                   index        =   ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values       =   ["QT_NULOS", "QT_BRANCOS", "QT_APTOS", "QT_COMPARECIMENTOS", "QT_ABST"], 
                                   aggfunc      =   np.sum,
                                   fill_value   =   0
                                   )

ds_pres_2T_pivot1   = pd.pivot_table(ds_pres_2T1,
                                   index        =   ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values       =   ["QT_NULOS", "QT_BRANCOS", "QT_APTOS", "QT_COMPARECIMENTOS", "QT_ABST"], 
                                   aggfunc      =   np.sum,
                                   fill_value   =   0
                                   )

ds_gov_pivot1       = pd.pivot_table(ds_gov1,
                                   index        =   ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values       =   ["QT_NULOS", "QT_BRANCOS", "QT_APTOS", "QT_COMPARECIMENTOS", "QT_ABST"], 
                                   aggfunc      =   np.sum,
                                   fill_value   =   0
                                   )

ds_sen_pivot1       = pd.pivot_table(ds_sen1,
                                   index        =   ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values       =   ["QT_NULOS", "QT_BRANCOS", "QT_APTOS", "QT_COMPARECIMENTOS", "QT_ABST"], 
                                   aggfunc      =   np.sum,
                                   fill_value   =   0
                                   )

ds_depfed_pivot1    = pd.pivot_table(ds_depfed1,
                                   index        =   ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values       =   ["QT_NULOS", "QT_BRANCOS", "QT_APTOS", "QT_COMPARECIMENTOS", "QT_ABST"], 
                                   aggfunc      =   np.sum,
                                   fill_value   =   0
                                   )

ds_depest_pivot1    = pd.pivot_table(ds_depest1,
                                   index        =   ["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                   values       =   ["QT_NULOS", "QT_BRANCOS", "QT_APTOS", "QT_COMPARECIMENTOS", "QT_ABST"], 
                                   aggfunc      =   np.sum,
                                   fill_value   =   0
                                   )

###############################################################################

ds_pres_1T_final    = pd.concat([ds_pres_1T_pivot0, ds_pres_1T_pivot1], axis = 1, join = "inner")
ds_pres_2T_final    = pd.concat([ds_pres_2T_pivot0, ds_pres_2T_pivot1], axis = 1, join = "inner")
ds_gov_final        = pd.concat([ds_gov_pivot0, ds_gov_pivot1]        , axis = 1, join = "inner")
ds_sen_final        = pd.concat([ds_sen_pivot0, ds_sen_pivot1]        , axis = 1, join = "inner")
ds_depfed_final     = pd.concat([ds_depfed_pivot0, ds_depfed_pivot1]  , axis = 1, join = "inner")
ds_depest_final     = pd.concat([ds_depest_pivot0, ds_depest_pivot1]  , axis = 1, join = "inner")

###############################################################################

ds_pres_1T_final.to_csv("/Users/jpalcantara/Desktop/2002_pres_1T.csv")
ds_pres_2T_final.to_csv("/Users/jpalcantara/Desktop/2002_pres_2T.csv")
ds_gov_final.to_csv("/Users/jpalcantara/Desktop/2002_gov.csv")
ds_sen_final.to_csv("/Users/jpalcantara/Desktop/2002_sen.csv")
ds_depfed_final.to_csv("/Users/jpalcantara/Desktop/2002_depfed.csv")
ds_depest_final.to_csv("/Users/jpalcantara/Desktop/2002_depest.csv")

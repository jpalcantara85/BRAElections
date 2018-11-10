import pandas as pd, numpy as np, glob

####
#
#dataset1 = pd.read_csv("/Users/jpalcantara/Desktop/Trade in Elections/Files/1T 2T 2010/Presidente VOTOS/votacao_candidato_munzona_2010_BR.txt", encoding = 'latin1', sep = ";", header = None)
#dataset1.columns = ["X0", "X1", "X2", "NUM_TURNO", "X4", "SG_ UF", "CD_MUNICIPIO", "X7", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO", "X11", "X12", "X13", "NM_VOTAVEL", "DS_CARGO", "X16", "X17", "X18", "X19", "X20", "X21", "NR_PARTIDO", "SG_PARTIDO", "X24", "X25", "X26", "X27", "QT_VOTOS"]
#
#ds_pres = dataset1[dataset1.DS_CARGO == "PRESIDENTE"]
#ds_pres = ds_pres[ds_pres["SG_ UF"] != "VT"]
#ds_pres = ds_pres[ds_pres["SG_ UF"] != "ZZ"]
#
#ds_pres_1T = ds_pres[ds_pres["NUM_TURNO"] == 1]
#ds_pres_2T = ds_pres[ds_pres["NUM_TURNO"] == 2]
#
#ds_pres_pivot1 = pd.pivot_table(ds_pres_1T,
#                                   index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
#                                   values = ["QT_VOTOS"], 
#                                   columns = ["NR_PARTIDO", "NM_VOTAVEL"],
#                                   aggfunc = np.sum,
#                                   fill_value = 0
#                                   )
#
#ds_pres_pivot2 = pd.pivot_table(ds_pres_2T,
#                                   index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
#                                   values = ["QT_VOTOS"], 
#                                   columns = ["NR_PARTIDO", "NM_VOTAVEL"],
#                                   aggfunc = np.sum,
#                                   fill_value = 0
#                                   )
#
####
#
#dataset2 = pd.read_csv("/Users/jpalcantara/Desktop/Trade in Elections/Files/1T 2T 2010/Presidente APTOS/detalhe_votacao_secao_2010_BR.txt", encoding = 'latin1', sep = ";", header = None)
#dataset2.columns = ["X0", "X1", "X2", "NUM_TURNO", "X4", "SG_ UF", "X6", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_CARGO_PERGUNTA", "DS_CARGO", "QT_APTOS", "X14", "QT_ABSTENCOES", "X16", "X17", "X18", "X19", "X20"]
#
#ds_aptos_abst1 = dataset2[dataset2["NUM_TURNO"] == 1]
#ds_aptos_abst2 = dataset2[dataset2["NUM_TURNO"] == 2]
#
#ds_aptos1 = pd.pivot_table(ds_aptos_abst1,
#                          index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
#                          values = ["QT_APTOS"],
#                          columns = ["NR_ZONA", "NR_SECAO"],
#                          fill_value = 0
#                          )
#
#ds_aptos1["TOTAL_APTOS"] = round(ds_aptos1.sum(axis = 1))
#ds_aptos1 = ds_aptos1[["TOTAL_APTOS"]]
#
#ds_abst1 = pd.pivot_table(ds_aptos_abst1,
#                          index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
#                          values = ["QT_ABSTENCOES"],
#                          columns = ["NR_ZONA", "NR_SECAO"], 
#                          fill_value = 0
#                          )
#
#ds_abst1["TOTAL_ABSTENCOES"] = round(ds_abst1.sum(axis = 1))
#ds_abst1 = ds_abst1[["TOTAL_ABSTENCOES"]]
#
#ds_aptos_abstencoes_1T = pd.concat([ds_aptos1, ds_abst1], axis = 1, join = "inner")
#
#ds_aptos2 = pd.pivot_table(ds_aptos_abst2,
#                          index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
#                          values = ["QT_APTOS"],
#                          columns = ["NR_ZONA", "NR_SECAO"], 
#                          fill_value = 0
#                          )
#
#ds_abst2 = pd.pivot_table(ds_aptos_abst2,
#                          index = ["SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
#                          values = ["QT_ABSTENCOES"],
#                          columns = ["NR_ZONA", "NR_SECAO"], 
#                          fill_value = 0
#                          )
#
#ds_aptos2["TOTAL_APTOS"] = round(ds_aptos2.sum(axis = 1))
#ds_aptos2 = ds_aptos2[["TOTAL_APTOS"]]
#
#ds_abst2["TOTAL_ABSTENCOES"] = round(ds_abst2.sum(axis = 1))
#ds_abst2 = ds_abst2[["TOTAL_ABSTENCOES"]]
#
#ds_aptos_abstencoes_2T = pd.concat([ds_aptos2, ds_abst2], axis = 1, join = "inner")
#
####
#
#ds_pres_final1 = pd.concat([ds_pres_pivot1, ds_aptos_abstencoes_1T], axis = 1, join = "inner")
#ds_pres_final2 = pd.concat([ds_pres_pivot2, ds_aptos_abstencoes_2T], axis = 1, join = "inner")
#
#ds_pres_final1.to_csv("1T_pres_2010.csv")
#ds_pres_final2.to_csv("2T_pres_2010.csv")

######

folder_1 = glob.glob("/Users/jpalcantara/Desktop/Trade in Elections/Files/1T 2T 2010/Candidatos VOTOS/" + "/*.txt")
list_1 = []
frame_1 = []

for file_ in folder_1:
    df = pd.read_csv(file_, encoding = 'latin1', sep = ";", header = None)
    df.columns = ["X0", "X1", "X2", "NUM_TURNO", "X4", "SG_ UF", "X6", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "CD_CARGO", "DS_CARGO", "X12", "X13", "X14", "SG_PARTIDO", "NR_PARTIDO", "NM_PARTIDO", "QT_VOTOS", "X19", "X20"]
    list_1.append(df)

#datasetA = pd.read_csv("/Users/jpalcantara/Desktop/Trade in Elections/Files/1T 2T 2010/Candidatos VOTOS/votacao_partido_munzona_2010_AC.txt", encoding = 'latin1', sep = ";", header = None)
#datasetA.columns = ["X0", "X1", "X2", "NUM_TURNO", "X4", "SG_ UF", "X6", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "CD_CARGO", "DS_CARGO", "X12", "X13", "X14", "SG_PARTIDO", "NR_PARTIDO", "NM_PARTIDO", "QT_VOTOS", "X19", "X20"]
#
#datasetB = pd.read_csv("/Users/jpalcantara/Desktop/Trade in Elections/Files/1T 2T 2010/Candidatos VOTOS/votacao_partido_munzona_2010_AL.txt", encoding = 'latin1', sep = ";", header = None)
#datasetB.columns = ["X0", "X1", "X2", "NUM_TURNO", "X4", "SG_ UF", "X6", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "CD_CARGO", "DS_CARGO", "X12", "X13", "X14", "SG_PARTIDO", "NR_PARTIDO", "NM_PARTIDO", "QT_VOTOS", "X19", "X20"]
#
#list_1 = [datasetA, datasetB]
      
for i in list_1:  
    ds_partidos = pd.pivot_table(i,
                                 index = ["CD_CARGO", "SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                                 values = ["QT_VOTOS"], 
                                 columns = ["NR_PARTIDO", "NM_PARTIDO"],
                                 aggfunc = np.sum,
                                 fill_value = 0
                                 )
  
    frame_1.append(ds_partidos)

ds_partidos_final = pd.concat(frame_1)

###

folder_2 = glob.glob("/Users/jpalcantara/Desktop/Trade in Elections/Files/1T 2T 2010/Candidatos APTOS/" + "/*.txt")
list_2 = []
frame_2 = []

for file_ in folder_2:
    df = pd.read_csv(file_, encoding = 'latin1', sep = ";", header = None)
    df.columns = ["X0", "X1", "X2", "NUM_TURNO", "X4", "SG_ UF", "X6", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_CARGO_PERGUNTA", "DS_CARGO", "QT_APTOS", "X14", "QT_ABSTENCOES", "X16", "X17", "X18", "X19", "X20"]
    list_2.append(df)

#datasetC = pd.read_csv("/Users/jpalcantara/Desktop/Trade in Elections/Files/1T 2T 2010/Candidatos APTOS/detalhe_votacao_secao_2010_AC.txt", encoding = 'latin1', sep = ";", header = None)
#datasetC.columns = ["X0", "X1", "X2", "NUM_TURNO", "X4", "SG_ UF", "X6", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_CARGO_PERGUNTA", "DS_CARGO", "QT_APTOS", "X14", "QT_ABSTENCOES", "X16", "X17", "X18", "X19", "X20"]
#
#datasetD = pd.read_csv("/Users/jpalcantara/Desktop/Trade in Elections/Files/1T 2T 2010/Candidatos APTOS/detalhe_votacao_secao_2010_AL.txt", encoding = 'latin1', sep = ";", header = None)
#datasetD.columns = ["X0", "X1", "X2", "NUM_TURNO", "X4", "SG_ UF", "X6", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_CARGO_PERGUNTA", "DS_CARGO", "QT_APTOS", "X14", "QT_ABSTENCOES", "X16", "X17", "X18", "X19", "X20"]
#
#list_2 = [datasetC, datasetD]

for i in list_2:  
    ds_aptos = pd.pivot_table(i,
                              index = ["CD_CARGO_PERGUNTA", "SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                              values = ["QT_APTOS"],
                              columns = ["NR_ZONA", "NR_SECAO"], 
                              fill_value = 0
                              )

    ds_abst = pd.pivot_table(i,
                             index = ["CD_CARGO_PERGUNTA", "SG_ UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], 
                             values = ["QT_ABSTENCOES"],
                             columns = ["NR_ZONA", "NR_SECAO"], 
                             fill_value = 0
                             )

    ds_aptos["TOTAL_APTOS"] = round(ds_aptos.sum(axis = 1))
    ds_aptos = ds_aptos[["TOTAL_APTOS"]]

    ds_abst["TOTAL_ABSTENCOES"] = round(ds_abst.sum(axis = 1))
    ds_abst = ds_abst[["TOTAL_ABSTENCOES"]]

    ds_aptos_abstencoes = pd.concat([ds_aptos, ds_abst], axis = 1, join = "inner")

    frame_2.append(ds_aptos_abstencoes)

ds_aptos_abst_final = pd.concat(frame_2)

###

#ds_final = pd.concat([ds_partidos_final, ds_aptos_abst_final], axis = 1, join = "inner")
#ds_final = ds_final.fillna(0)
#
####
#
#x = ds_final.reset_index(level = 0)
#y = x.rename(columns = {"level_0": "CD_CARGO"}, inplace = True)
#
#ds_gov_2010 = x[x.CD_CARGO == 3]
#ds_gov_2010 = ds_gov_2010.drop("CD_CARGO", 1)
#
#ds_sen_2010 = x[x.CD_CARGO == 5]
#ds_sen_2010 = ds_sen_2010.drop("CD_CARGO", 1)
#
#ds_depfed_2010 = x[x.CD_CARGO == 6]
#ds_depfed_2010 = ds_depfed_2010.drop("CD_CARGO", 1)
#
#ds_depest_2010 = x[x.CD_CARGO == 7]
#ds_depest_2010 = ds_depest_2010.drop("CD_CARGO", 1)
#
####
#
#ds_gov_2010.to_csv("1T_gov_2010.csv")
#ds_sen_2010.to_csv("1T_sen_2010.csv")
#ds_depfed_2010.to_csv("1T_depest_2010.csv")
#ds_depest_2010.to_csv("1T_depfed_2010.csv")

###

folder_3 = glob.glob("/Users/jpalcantara/Desktop/Trade in Elections/Files/1T 2T 2010/Partidos/" + "/*.txt")
list_3 = []

for file_ in folder_3:
    df = pd.read_csv(file_, encoding = 'latin1', sep = ";", header = None)
    df.columns = ["X0", "X1", "X2", "X3", "X4", "SG_ UF", "X6", "X7", "X8", "X9", "X10", "NR_CANDIDATO", "X12", "X13", "NM_CANDIDATO", "CARGO", "X16", "X17", "X18", "X19", "X20", "X21", "NR_PARTIDO", "SG_PARTIDO", "NM_PARTIDO", "X25", "X26", "X27", "X28"]
    list_3.append(df)
    
ds_nomes_candidatos = pd.concat(list_3)
ds_nomes_candidatos = ds_nomes_candidatos[["SG_ UF", "NR_CANDIDATO", "NM_CANDIDATO", "CARGO", "NR_PARTIDO", "SG_PARTIDO", "NM_PARTIDO"]]
ds_nomes_candidatos = ds_nomes_candidatos.drop_duplicates()

ds_nomes_candidatos.to_csv("candidatos_2010.csv")
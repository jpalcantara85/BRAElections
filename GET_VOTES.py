import pandas as pd, numpy as np, glob

#folder = glob.glob("/Users/jpalcantara/Downloads/2003-2007" + "/*.txt")
#folder = glob.glob("/Users/jpalcantara/Downloads/2007-2011" + "/*.txt")
#folder = glob.glob("/Users/jpalcantara/Downloads/2011-2015" + "/*.txt")
#folder = glob.glob("/Users/jpalcantara/Downloads/2015-2019" + "/*.txt")

list = []

for file in folder:
        df_temp = pd.read_fwf(file, widths = [16, 40, 10, 11, 25, 5], encoding = 'latin1', names = ["HEADER", "NM_PARLA", "VOTE", "PARTY", "STATE", "COD_PARLA"])
        list.append(df_temp)

df = pd.concat(list, axis = 0, ignore_index = True)

df_pivot = pd.pivot_table(df,
                          index      =   ["NM_PARLA", "PARTY", "STATE", "COD_PARLA"], 
                          values     =   ["VOTE"], 
                          columns    =   ["HEADER"],
                          aggfunc    =   np.sum,
                          fill_value =   0
                          )

df_pivot[df_pivot == "Não"]       = "N"     # No
df_pivot[df_pivot == "Sim"]       = "Y"     # Yes
df_pivot[df_pivot == "Abstenção"] = "A"     # Abstention
df_pivot[df_pivot == "Obstrução"] = "O"     # Obstruction
df_pivot[df_pivot == "Branco"]    = "B"     # Blank
df_pivot[df_pivot == "Presente"]  = "P"     # Secret ballot
df_pivot[df_pivot == "<------->"] = "X"     # Not present
                                            # If 0 then congressman changed parties

#df_pivot.to_csv("/Users/jpalcantara/Desktop/2003_2007.csv", encoding = "utf-8")
#df_pivot.to_csv("/Users/jpalcantara/Desktop/2007_2011.csv", encoding = "utf-8")
#df_pivot.to_csv("/Users/jpalcantara/Desktop/2011_2015.csv", encoding = "utf-8")
#df_pivot.to_csv("/Users/jpalcantara/Desktop/2015_2019.csv", encoding = "utf-8")

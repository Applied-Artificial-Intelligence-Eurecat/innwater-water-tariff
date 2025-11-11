import pandas as pd
from gini_decomp import *
from pandas_ods_reader import read_ods

population_df = read_ods("gini_test.ods")
print(population_df)

print("GINI")
print("##############################")
from gini_decomp import * 
result = gini_decomp(population_df['car_excess'], population_df['sanitation_status'])
for x in result:
    print (x)
    for y in result[x]:
        print (y,':',result[x][y])
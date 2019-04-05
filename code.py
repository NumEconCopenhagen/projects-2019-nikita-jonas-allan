# Import relevent packages: Panda, numpy, matplotlib and pydst
# Note: Sometimes you need to run code 2 times, before yoour packages will be uploaded

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydst
dst = pydst.Dst(lang = 'da') # Lang = Danish

# Get columns dictionary from DST
columns_dict = {}
columns_dict['TRANSAKT'] = 'variable'
columns_dict['PRISENHED'] = 'unit'
columns_dict['TID'] = 'year'
columns_dict['INDHOLD'] = 'value'


var_dict = {} # var is for variable

# Get variable dictionary from DST
var_dict['B.1*g Bruttpmationalprodukt, BNP'] = 'Y'
var_dict['P.31 Privatforbrug'] = 'C'
var_dict['P.3 Offentlige forbrugsudgifter'] = 'G'
var_dict['P.5g Bruttoinvesteringer'] = 'I'
var_dict['P.6 Eksport af varer og tjenester'] = 'X'
var_dict['P.7 Import af varer og tjenester'] = 'M'


# UNITS
unit_dict = {}
unit_dict['2010-priser, kædede værdier'] = 'realle'
unit_dict['løbende priser'] = 'nominelle'

# CODE. There is a bug in the code, where you get the desired year + start year.
nan1 = dst.get_data(table_id = 'NAN1', variables={'TRANSAKT':['*'], 'PRISENHED':['*'], 'TID':['*']})
nan1.rename(columns = columns_dict, inplace = True)

# Following loops get items from our variable and value list, defined on lines 21 to 26
# and 30 to 32
for key,value in var_dict.items():
    nan1.variable.replace(key,value,inplace=True)

for key,value in unit_dict.items():
    nan1.unit.replace(key,value, inplace=True)

I = False
for key,value in var_dict.items():
    I = I | (nan1.variable == value)
nan1 = nan1[I]


# Basic discriptive stats
nan1.groupby(['variable','unit']).describe()

# We create a new variable 'X', where we select data from year 2001 and onwards
X = nan1["year"]>2000  
nan1 = nan1[X]

# We define which unit we will work with.
K=nan1["unit"]=="Pr. indbygger, løbende priser, (1000 kr.)"
nan1 = nan1[K]

# At last we recreate our data from dst to be a DataFrame
df=pd.DataFrame(data=nan1)

# Sort values first by year and then by variable type
df.sort_values(by=["year","variable"])

# Replace old index with our new index. We use year as index in our case
df.set_index(['year'], inplace=True)
df.sort_index(inplace=True)

# In our data, all values where strings. As such we need to make value numbers into floats instead of strings
df["value"]=df["value"].str.replace(",",".").astype(float)

# As we do not have data for Net Export, we need to make this variable. Just like before we make it a float
# Note: This new variable is not a dataFrame
NX = pd.to_numeric(df.loc[:,:].value[df.loc[:,:].variable == "X" ]) - pd.to_numeric(df.loc[:,:].value[df.loc[:,:].variable == "M" ])
NX.columns=["year","value"]

# Defining our new variable as a dataFrame var. 
NX=pd.DataFrame(data=NX)
NX["variable"] ="NX"


# Next we use Pandas function 'concat' to add Net Export to our DataFrame. We call this dataset for "dollo"
dollo= pd.concat([df, NX])
# We sort our dollo data set
dollo.sort_index(inplace=True)

# As we have the new variable 'Net Export', we remove import and export
dollo=dollo[dollo.variable !='X']
dollo=dollo[dollo.variable !='M']
# Sort by year and var.
dollo.sort_values(by=["year","variable"])

# We realised that we lack data for GDP in total, we make a new variable 'Y', which is a sum of other variables
Y = pd.to_numeric(dollo.loc[:,:].value[dollo.loc[:,:].variable == 'C']) + pd.to_numeric(dollo.loc[:,:].value[dollo.loc[:,:].variable== 'G']) + pd.to_numeric(dollo.loc[:,:].value[dollo.loc[:,:].variable== 'I'])  + pd.to_numeric(dollo.loc[:,:].value[dollo.loc[:,:].variable== 'NX'])
Y.columns=['year','value']

# Just like with NX, we define the new variable as a dataFrame
Y = pd.DataFrame(data=Y)
Y['variable'] = 'Y'

# An important note: We do not add our 'Y' variable to the complete table.
# The reason why will be clear when we make our graph

# Next lines make our graph
fig, ax = plt.subplots(figsize=(15,7))
dollo.groupby(['year','variable']).sum()['value'].unstack().plot(ax=ax, kind='bar', stacked = True)
ax.set_xlabel('year')
ax.set_ylabel('Mia')
Y.groupby(['year','variable']).sum()['value'].plot(ax=ax)
# Looking at our variable list, we can see that only C G I and NX are part of this group
# As such we have 2 lists: Var list and GDP list. Doing so allows us to make a very simple
# combination of these two lists graphically..
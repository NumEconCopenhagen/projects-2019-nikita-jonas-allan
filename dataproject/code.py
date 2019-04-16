import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydst
dst = pydst.Dst(lang = 'da')

columns_dict = {}
columns_dict['TRANSAKT'] = 'variable'
columns_dict['PRISENHED'] = 'unit'
columns_dict['TID'] = 'year'
columns_dict['INDHOLD'] = 'value'
columns_dict['HOVED'] = 'Type'
columns_dict['PERPCT'] = 'Type'


var_dict = {} # var is for variable
#var_dict['P.1 Output'] = 'Y'
#var_dict['P.3 Final consumption expenditure'] = 'C'
#var_dict['P.3 Government consumption expenditure'] = 'G'
#var_dict['P.5 Gross capital formation'] = 'I'
#var_dict['P.6 Export of goods and services'] = 'X'
#var_dict['P.7 Import of goods and services'] = 'M'

#VARIABLES
var_dict['B.1*g Bruttonationalprodukt, BNP'] = 'Y'
var_dict['P.31 Privatforbrug'] = 'C'
var_dict['P.3 Offentlige forbrugsudgifter'] = 'G'
var_dict['P.5g Bruttoinvesteringer'] = 'I'
var_dict['P.6 Eksport af varer og tjenester'] = 'X'
var_dict['P.7 Import af varer og tjenester'] = 'M'
var_dict['ÅRSSTIGNING'] = 'Inflation'

#UNITS
unit_dict = {}
#unit_dict['2010-prices, chained values'] = 'real'
#unit_dict['Current prices'] = 'nominal'
unit_dict['2010-priser, kædede værdier'] = 'realle'
unit_dict['løbende priser'] = 'nominelle'

#CODE
nan1 = dst.get_data(table_id = 'NAN1', variables={'TRANSAKT':['*'], 'PRISENHED':['*'], 'TID':['*']})
nan1.rename(columns = columns_dict, inplace = True)

for key,value in var_dict.items():
    nan1.variable.replace(key,value,inplace=True)

for key,value in unit_dict.items():
    nan1.unit.replace(key,value, inplace=True)

I = False
for key,value in var_dict.items():
    I = I | (nan1.variable == value)
nan1 = nan1[I]

nan1.groupby(['variable','unit']).describe()

X = nan1["year"]>2000 #laver en ny variabel hvor X inderholder en variabel year som er større end 2000. giver nan1= nan1[x] for at sige at den skal være lig med det. 
nan1 = nan1[X]
nan2=nan1
nan3=nan1

Y=nan1["unit"]=="Pr. indbygger, løbende priser, (1000 kr.)"
#Her laver selectere jeg Faste og løbende priser for variablen Uni
#nan1=nan1.loc[nan1["unit"].isin(["Pr. indbygger, løbende priser, (1000 kr.)" ,"Pr. indbygger, 2010-priser, kædede værdier, (1000 kr.)"])]

nan1 = nan1[Y]
df=pd.DataFrame(data=nan1)
df.sort_values(by=["year","variable"])

#Her laver jeg et nyt dataframe i tilfælde at det er lettere at arbejde med de fastepriser for sig selv. 
X = nan2["year"]>2000
nan2 = nan2[X]
Y=nan2["unit"]=="Pr. indbygger, 2010-priser, kædede værdier, (1000 kr.)"
nan2 = nan2[Y]
df_K=pd.DataFrame(data=nan2)
df_K.sort_values(by=["year","variable"])

#Her laver jeg et nyt dataframe for realvækst. 
X = nan3["year"]>2000
nan3 = nan3[X]
bb=nan3["variable"]=="Y"
nan3 = nan3[bb]
Y=nan3["unit"]=="Realvækst i pct. i forhold til foregående periode"
nan3 = nan3[Y]
df_Y=pd.DataFrame(data=nan3)
df_Y.sort_values(by=["year","variable"])


#df.loc[df.variable=="X", "Eksport"]=df.value
#df.loc[df.variable=="M", "Eksport"]=df.value
df.set_index(['year'], inplace=True)
df.sort_index(inplace=True)

df["value"]=df["value"].str.replace(",",".").astype(float)

# komma til punktum før to numeric 
NX = pd.to_numeric(df.loc[:,:].value[df.loc[:,:].variable == "X" ]) - pd.to_numeric(df.loc[:,:].value[df.loc[:,:].variable == "M" ])
NX.columns=["year","value"]
print(NX)

NX=pd.DataFrame(data=NX)

NX["variable"] ="NX"


dollo= pd.concat([df, NX])

dollo.sort_index(inplace=True)
dollo
#her fjerner vi X og M
dollo=dollo[dollo.variable !='X']
dollo=dollo[dollo.variable !='M']
dollo.sort_values(by=["year","variable"])

#her laver vi en samlet BNP variabel.
Y = pd.to_numeric(dollo.loc[:,:].value[dollo.loc[:,:].variable == 'C']) + pd.to_numeric(dollo.loc[:,:].value[dollo.loc[:,:].variable== 'G']) + pd.to_numeric(dollo.loc[:,:].value[dollo.loc[:,:].variable== 'I'])  + pd.to_numeric(dollo.loc[:,:].value[dollo.loc[:,:].variable== 'NX'])
Y.columns=['year','value']
print(Y)

Y = pd.DataFrame(data=Y)
Y['variable'] = 'Y'
Y

# plot data
fig, ax = plt.subplots(figsize=(15,7))
# use unstack()
#dollo.groupby(['year','variable']).sum()['value'].unstack().plot(ax=ax , kind='bar',stacked=True)
Y.groupby(['year','variable']).sum()['value'].unstack().plot(ax=ax)
ax.set_xlabel('Year')
ax.set_ylabel('Mio')            
print(df)

#HER LAVER JEG DET FOR FASTE PRISER

df_K.set_index(['year'], inplace=True)
df_K.sort_index(inplace=True)

df_K["value"]=df_K["value"].str.replace(",",".").astype(float)
df_K.sort_index(inplace=True)
# komma til punktum før to numeric 
NX_K = pd.to_numeric(df_K.loc[:,:].value[df_K.loc[:,:].variable == "X" ]) - pd.to_numeric(df_K.loc[:,:].value[df_K.loc[:,:].variable == "M" ])
NX_K.columns=["year","value"]

print(NX_K)

NX_K=pd.DataFrame(data=NX_K)

NX_K["variable"] ="NX"


dollo_K= pd.concat([df_K, NX_K])

dollo_K.sort_index(inplace=True)
dollo_K

#her fjerner vi X og M
dollo_K=dollo_K[dollo_K.variable !='X']
dollo_K=dollo_K[dollo_K.variable !='M']
dollo_K=dollo_K[dollo_K.variable !='Y']
dollo_K.sort_values(by=["year","variable"])

#her laver vi en samlet BNP variabel.
Y = pd.to_numeric(dollo_K.loc[:,:].value[dollo_K.loc[:,:].variable == 'C']) + pd.to_numeric(dollo_K.loc[:,:].value[dollo_K.loc[:,:].variable== 'G']) + pd.to_numeric(dollo_K.loc[:,:].value[dollo_K.loc[:,:].variable== 'I'])  + pd.to_numeric(dollo_K.loc[:,:].value[dollo_K.loc[:,:].variable== 'NX'])
Y.columns=['year','value']
print(Y)

Y = pd.DataFrame(data=Y)
Y['variable'] = 'Y'
Y

#her fjerner jeg indekx. 
dollo_K1 = dollo_K.reset_index()
Y1 = Y.reset_index()

nan3.set_index(['year'], inplace=True)
nan3.sort_index(inplace=True)
nan3=nan3.reset_index()
nan3["value"]=nan3["value"].str.replace(",",".").astype(float)


#laver figur
fig, ax = plt.subplots(figsize=(20,7))
dollo_K1.groupby(['year','variable']).sum()['value'].unstack().plot( ax=ax,  kind='bar', stacked = True)
nan3.groupby(['year','variable']).sum()['value'].plot(ax=ax,  secondary_y=True, color="r").set_ylabel("realvækst i BNP")
ax.set_ylabel('Mia ')
plt.show()


#for inflation
pris119 = dst.get_data(table_id = 'PRIS119', variables={'TID':['*'], 'HOVED':['*']})
pris119.rename(columns = columns_dict, inplace = True)
pris119

infl = pd.DataFrame(data=pris119)
infl = infl[infl.Type !='Årsgennemsnit']
infl = infl[infl.value !='..']
infl["value"]=infl["value"].str.replace(",",".").astype(float)
infl
#henter data fra dst
AULAAR = dst.get_data(table_id = 'AULAAR', variables={'TID':['*']})
X = AULAAR["TID"]>1996
AULAAR1 = AULAAR[X]
AULAAR1.rename(columns = columns_dict, inplace = True)


AULAAR1 = pd.DataFrame(data=AULAAR1)
AULAAR1['value']=AULAAR1['value'].str.replace(',','.').astype(float)
AULAAR1


aaar= pd.DataFrame(data=AULAAR1["year"])
aaar.set_index(['year'], inplace=True)
aaar.sort_index(inplace=True)


fig, ax = plt.subplots(figsize=(20,7))
ax.scatter(AULAAR1["value"], infl["value"])
for i, txt in enumerate(aaar):
    ax.annotate(txt, (AULAAR1["value"][i], infl["value"][i]))




#dollo_K.sort_values(by=["year","variable"])

#dollo_K1["year"].astype(float)
#dollo_K1.groupby(['year','variable'])

#dollo_K1.plot(x="year", y=["variable"], stacked=True, kind="bar")
 #ax = Y['variable'].plot(secondary_y=True, color='k', marker='o')
 #ax.set_ylabel('variable')







import sys, os, json, time
import pandas as pd

BOROCODE = {'61' : '1', '05' : '2', '47': '3', '81' : '4', '85': '5'}

if (len(sys.argv) < 2):
    print ("Usage: cfcensus.py census.csv districts.json")
    exit()
    
censusfile = sys.argv[1]
councilfile = sys.argv[2]

def boroCT (id2):
    boro = BOROCODE[str(id2)[3:5]]
    tract = str(id2)[5:]
    return boro + tract

for (f) in ([censusfile, councilfile]):
    if (not os.path.isfile(f)):
        print ("File " + f + " is not readable")
        exit()

try:
    vehDf = pd.read_csv(
         censusfile,
         skiprows=[1]
            )
except Exception as e:
    print ("Unable to read census file " + censusfile + ": {0}".format(e))
    exit()


try:
    with open(councilfile) as councilfo:
        councilData = json.load(councilfo)

except Exception as e:
    print ("Unable to read council file " + councilfile+": {0}".format(e))
    exit()


vehDf['pctNoVeh'] = (vehDf['VD10'].astype('int') + vehDf['VD03'].astype('int')) / vehDf['VD01'].astype('int')
vehDf['BoroCT'] = vehDf['GEO.id2'].apply(boroCT)

# The 2000 census splits households with no vehicle into:
# VD03 (owner-occupied) and VD10 (rental)

vehDf2 = pd.DataFrame(vehDf[['BoroCT', 'VD01', 'VD03', 'VD10', 'pctNoVeh']]).set_index('BoroCT')

k = 0
total = {}
noVeh = {}
councilDistricts = set()
for (t, c) in councilData.items():
    for (d) in c:
        councilDistricts.add(d)
        try:
            total[d] = total.get(d, 0) + c[d] * vehDf2.loc[str(t)]['VD01']
            noVeh[d] = noVeh.get(d, 0) + c[d] * (vehDf2.loc[str(t)]['VD03'] + vehDf2.loc[str(t)]['VD10'])
        except KeyError as e:
            k += 1

for (d) in sorted(councilDistricts, key=int):
    carfree = str(round((noVeh[d] / total[d]), 3))
    print (','.join([
                d,
                str(int(total[d])),
                str(int(noVeh[d])),
                carfree
                ]))


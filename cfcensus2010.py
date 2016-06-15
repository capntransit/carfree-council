import sys, os, json, time
import pandas as pd

BOROCODE = {'61' : '1', '05' : '2', '47': '3', '81' : '4', '85': '5'}

if (len(sys.argv) < 2):
    print ("Usage: cfcensus.py census.csv districts.json")
    exit()
    
censusfile = sys.argv[1]
councilfile = sys.argv[2]
TRACTCOL = 'BoroCT' # rename this for 2000 census

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


vehDf['pctNoVeh'] = vehDf['HD01_VD03'].astype('int') / vehDf['HD01_VD01'].astype('int')
vehDf[TRACTCOL] = vehDf['GEO.id2'].apply(boroCT)

vehDf2 = pd.DataFrame(vehDf[[TRACTCOL, 'HD01_VD01', 'HD01_VD03', 'pctNoVeh']]).set_index(TRACTCOL)


f = 0
total = {}
noVeh = {}
councilDistricts = set()
for (t, c) in councilData.items():
    for (d) in c:
        councilDistricts.add(d)
        try:
            total[d] = total.get(d, 0) + c[d] * vehDf2.loc[str(t)]['HD01_VD01']
            noVeh[d] = noVeh.get(d, 0) + c[d] * vehDf2.loc[str(t)]['HD01_VD03']
        except KeyError as e:
            print("No entry for census tract " + str(t))

for (d) in sorted(councilDistricts, key=int):
    print (','.join([
                d,
                str(int(total[d])),
                str(int(noVeh[d])),
                str(round((noVeh[d] / total[d]), 3))
                ]))

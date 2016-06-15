# carfree-council
What percentage of households in a New York City Council district are car-free?

cfcouncil2000.py takes as input an HCT 32 table from the 2000 US decennial census, specifically the columns GEO.id2 (census tract), VD01 (Total), VD03 (Owner occupied: - No vehicle available) and VD10 (VD10,Renter occupied: - No vehicle available).  

cfcouncil2010.py takes as input a B0141 ("Means of Transportation to Work by Vehicles Available") table from the American Community Survey (2009-), specifically the columns GEO.id2, HD01_VD01 (Estimate; Total) and HD01_VD03 (Estimate; Total: - No vehicle available).

Each script combines the input with a JSON file mapping census tracts to New York City Council districts: tracts2000.json or tracts2010.json, produced from New York City Planning Department files with [tract2council.py](https://github.com/capntransit/tract2council).

The scripts do not check the margin of error to determine whether the output is statistically significant.

The algorithm introduces a potential source of inaccuracy by assigning the households to split census tracts on the basis of area.  This assumes that the households are evenly distributed within each census tract, but that is not always the case.  For example, a tract with 75% of its area in City Council District A and 25% in District B would have 75% of its households assigned to District A, but if there is a large apartment building in the District B part of the tract, it could contain over 50% of the households.

The output is a CSV file with four columns, as in the following example:

Council District | Total Households | Households without a vehicle | Percent
--- | --- | --- | ---
1 | 63808 | 

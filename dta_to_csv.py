
# coding: utf-8

import pandas as pd

df = pd.read_stata('/scratch/sv1239/projects/mlcs/raw/Votelevel_stuffjan2013.dta')
print df.shape
print "saving as csv..."
df.to_csv('/scratch/sv1239/projects/mlcs/raw/Votelevel_stuffjan2013.csv')
print "done!"




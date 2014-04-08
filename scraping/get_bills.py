
# In[13]:

import pandas as pd
from urllib import urlretrieve
import zipfile


# In[4]:

statedf = pd.read_csv('state_table.csv')
stateabbrevs = statedf['abbreviation']
stateabbrevs = [x.lower() for x in stateabbrevs]


# In[5]:

# http://static.openstates.org/downloads/2014-02-25-al-json.zip


# In[24]:

for state in stateabbrevs:
    try:
        url = 'http://static.openstates.org/downloads/2014-02-25-' + state + '-json.zip'
        saveloc = 'data/2014-02-25-' + state + '-json.zip'
        urlretrieve(url, saveloc)
        zippedstate = zipfile.ZipFile(saveloc,'r')
        zippedstate.extractall(path='data/'+state)
        zippedstate.close()
    except:
        url = 'http://static.openstates.org/downloads/2014-02-26-' + state + '-json.zip'
        saveloc = 'data/2014-02-26-' + state + '-json.zip'
        urlretrieve(url, saveloc)
        zippedstate = zipfile.ZipFile(saveloc,'r')
        zippedstate.extractall(path='data/'+state)
        zippedstate.close()
    print state


# Out[24]:

#     al
#     ak
#     az
#     ar
#     ca
#     co
#     ct
#     de
#     fl
#     ga
#     hi
#     id
#     il
#     in
#     ia
#     ks
#     ky
#     la
#     me
#     md
#     ma
#     mi
#     mn
#     ms
#     mo
#     mt
#     ne
#     nv
#     nh
#     nj
#     nm
#     ny
#     nc
#     nd
#     oh
#     ok
#     or
#     pa
#     ri
#     sc
#     sd
#     tn
#     tx
#     ut
#     vt
#     va
#     wa
#     wv
#     wi
#     wy
#     dc
# 

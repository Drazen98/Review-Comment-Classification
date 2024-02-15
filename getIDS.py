import requests as req
import time
import re
import pandas as pd
import numpy as np

# Dražen

def getOwnerMemberIds(itemId):
    URL = "https://www.aliexpress.com/item/" + itemId + ".html"
    page = req.get(URL)
    pageStr = str(page.content)
    pos = pageStr.find("sellerAdminSeq") + 16
    ownerMemberId = ""
    while (pageStr[pos] in "1234567890"):
        ownerMemberId += pageStr[pos]
        pos += 1
    productOwnerIds.append([itemId,ownerMemberId])

productIds = []
productOwnerIds = []

file = pd.read_csv("AliExpressLinks.csv", dtype = {'stars-href' : str}, usecols=['stars', 'stars-href']).to_numpy()

for i in file:
    if i[0] != 5.0:
        productIds.append(re.search("item/(.*?).html", i[1]).group(1))

# Antonio

j = 0
while len(productOwnerIds) != len(productIds):
    try:
        getOwnerMemberIds(productIds[j])
        j += 1
    except:
        print("error")
        time.sleep(600)
    if (j % 10 == 0):
        print(j)
        
poi = np.array(productOwnerIds)
df = pd.DataFrame({'productId' : poi[:,0], 'ownerMemberId': poi[:,1]})
df.to_csv('productSellerIds.csv')

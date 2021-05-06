# -*- coding: utf-8 -*-
##author : oaiskoo
##date : 2006
##goal : 
##
##input
##
##
##process
##
##
##output
##
## 
##history
##-2009
##--task
##
import os
import shutil
import time
import re
import pandas as pd
import numpy as np
import geopandas as gpd
from datetime import date

if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib
start = time.time()
start_day = date.today()
import ps3010_ytb_video_dl
import ps3020_img_db_gen


while 1:
    print('start ps3010')
    ps3010_ytb_video_dl.ps3010(10)
    print('start ps3020')
    ps3020_img_db_gen.ps3020()

end_day = date.today()
print("start day :", start_day)
print("end day :", end_day)
min_v = (time.time() - start)/60
print("time :", min_v, 'min')




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
import time
from datetime import date
start = time.time()
start_day = date.today()

import ps2010_youtube_trend_title
import ps2020_get_yid_by_search
##import ps2030_get_additional_yid
import ps2040_get_metadata
import ps2050_youtube_meta_tbl_gen
import ps2060_upload_y_meta_info_to_db
import ps2070_get_user_regi_youtube_meta


ps2010_youtube_trend_title.ps2010()
ps2020_get_yid_by_search.ps2020()
##ps2030_get_additional_yid.ps2030()
ps2040_get_metadata.ps2040(100)
ps2050_youtube_meta_tbl_gen.ps2050()
ps2060_upload_y_meta_info_to_db.ps2060()
ps2070_get_user_regi_youtube_meta.ps2070()

end_day = date.today()
print("start day :", start_day)
print("end day :", end_day)
min_v = (time.time() - start)/60
print("time :", min_v, 'min')


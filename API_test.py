import os

from utils.backend import BackendManager
from API.building import *
from template.buildings import *


GamePath = r"D:\Steam\steamapps\common\Victoria 3\game"
ModPath = r"mod\test"

BM = BackendManager(GamePath, ModPath)
print(BM.get_part("buildings"))
building_textile_mills ,rc = get_building_detail(BM, "building_textile_mills")


pm_test, rc = get_pm_detail(BM, "pm_patent_stills")

for key in pm_test.keys():
    print(key, pm_test[key])
print(building_textile_mills)


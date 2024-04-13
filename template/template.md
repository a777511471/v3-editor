# template

template文件夹下存放有关V3基本属性与数据部分的结构抽象，以python代码定义或者原始的txt文件形式存储。

为了应对可能的语法修改，建议将不相关的模板存放在不同的文件中，以便于维护。并且，如果不涉及具体的语义，如恒定不变的属性值（如texture）或者特殊的结构定义,而是抽象的一种基类，建议放置在utils文件夹下。

## 目前实现的模板

- [ ] `buildings.py`：有关于building,building_groups, production_method_groups, production_methods的定义
- [ ]  `goods.py`：有关于goods的读取等。
- [ ]  `localization.py`：有关于localization的读取等。

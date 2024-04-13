from utils.template import BaseTemplate
from utils.template import BaseManager

class Goods(BaseTemplate):
    def __init__(self, name ,if_init=False):
        original_file = "template/original/goods.txt"
        super().__init__(name,original_file, if_init)

    def _clone(self,name):
        return Goods(name, self.if_init)
    
    @staticmethod
    #从goods_manager中获取所有的goods与对应的cost
    def goods_dict(goods_manager: BaseManager):
        #检测goods_manager中的prototype是否为Goods
        if not isinstance(goods_manager.prototype, Goods):
            raise Exception("goods_manager中的prototype必须为Goods")
        result = {}
        for key in goods_manager.map:
            goods = goods_manager.map[key]
            cost = goods["cost"][1]
            result[key] = cost

        return result
    
    @staticmethod
    #获取指定key的goods的cost
    def goods(goods_manager: BaseManager, key: str):
        #检测goods_manager中的prototype是否为Goods
        if not isinstance(goods_manager.prototype, Goods):
            raise Exception("goods_manager中的prototype必须为Goods")
        goods = goods_manager.map[key]
        cost = goods["cost"][1]
        return cost
    
    

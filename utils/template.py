#用于添加与控制的模板类
from typing import Literal
from enum import Enum
from abc import ABC, abstractmethod

from utils.utils import output_to_txt
from utils.folder import parser_folder


class BaseTemplate:
    def __init__(self, name ,original_file,if_init=False):
        self.if_init = if_init
        self.original_file = original_file
        self.get_name = name
        #self.Localizations = Localization()
        self.data = {
            name: 
                [
                    "=",
                    None
                ]
            
        }
        if if_init:
            self.init_from_file()

    @abstractmethod
    def _clone(self, name):
        pass

    def clone_from(self, prototype: "BaseTemplate", new_name: str):
        '''
            从原型中克隆一个新的对象
        '''
        result:"BaseTemplate" = prototype._clone(new_name)
        result.data[new_name] = prototype.data[prototype.get_name]
        return result
    
    def rename(self, new_name: str):
        '''
            重命名
        '''
        self.data[new_name] = self.data.pop(self.get_name)
        self.get_name = new_name

    def radd(self, key:str
             , link_type:Literal["=","!=","?=","<",">","<=",">="]
             , value=None
             ):
        '''
            添加一项数据，如要添加一项后原数据从空变为
            building = {
               texture = "path/to/texture"
               	production_method_groups = {
		            pmg_explosives_building_chemical_plants
		            pmg_ownership_capital_building_explosives_factory      
	            }
            }
            则调用
            obj.add("texture", "=", '"path/to/texture"')
            obj.add("production_method_groups", "=", [
                "pmg_explosives_building_chemical_plants",
                "pmg_ownership_capital_building_explosives_factory"
            ])

        '''
        if value == None:
            self.data[self.get_name][1] = [key]
            return self
        self.data[self.get_name][1] = {}
        self.data[self.get_name][1][key] = [link_type, value]

        return self

    def rdelete(self, key:str):
        '''
            删除一项数据，如要删除一项后原数据为
            building = {
               texture = "path/to/texture"
               	production_method_groups = {
                    pmg_explosives_building_chemical_plants
                    pmg_ownership_capital_building_explosives_factory      
                }
            }
            则调用
            obj.delete("texture")
        '''
        if key in self.data[self.get_name][1].keys():
            del self.data[self.get_name][1][key]
        return self
    
    def add(self, key:str
            , link_type:Literal["=","!=","?=","<",">","<=",">="]
            , value = None, root_path:str = '', if_recursive:bool = False):
        '''
            在指定层级添加一项数据，如要添加一项后原数据为
            building = {
                texture = "path/to/texture"
                unlocking_technologies = {
		            intensive_agriculture
	            }
                possible = {
                        error_check = {     
                            severity = fail         <---添加位置
                        }
                }
            }
            则调用
            obj.add("possible", "=", {})
            obj.add("error_check", "=", {},"possible")
            obj.add("severity", "=", "fail","possible.error_check")
            或
            obj.add("severity", "=", "fail","possible.error_check",if_recursive=True)

        '''
        if root_path == "":
            self.radd(key, link_type, value)
            return self
        root_path_list = root_path.split(".")
        #根据root_path_list，找到对应的层级
        current_data = self.data[self.get_name][1]
        trace = ""
        for path in root_path_list:
            trace = trace + path + "."
            #如果当前层级不存在，则创建
            if path not in current_data.keys():
                if if_recursive:
                    current_data[path] = [
                        "=",
                        {}
                    ]
                else:
                    raise Exception("当前层级不存在:"+trace)
            #进入下一层级
            current_data = current_data[path][1]
        #添加数据
        #如果当前层级为列表，则key添加到列表中
        if isinstance(current_data, list):
            #若value为None，则添加key到列表中
            if value == None:
                current_data.append(key)
                return self 
            #若value不为None，则以 key link_type value的形式添加到列表中
            current_data.append([link_type, value])
            return self
        #如果当前层级为字典，则添加到字典中
        if isinstance(current_data, dict):
            current_data[key] = [link_type, value]
            return self
        
    def delete(self, key:str, root_path:str = ''):
        '''
            删除指定层级的一项数据，如要删除一项后原数据为
            building = {
                texture = "path/to/texture"
                unlocking_technologies = {
                    intensive_agriculture
                    manufacturies                   <---删除位置
                }
                possible = {
                        error_check = {
                            severity = fail
                        }
                }
            }
            则调用
            obj.delete("manufacturies","unlocking_technologies")
        '''
        if root_path == "":
            self.rdelete(key)
            return self
        root_path_list = root_path.split(".")
        #根据root_path_list，找到对应的层级
        current_data = self.data[self.get_name][1]
        trace = ""
        for path in root_path_list:
            trace = trace + path + "."
            #如果当前层级不存在，则创建
            if path not in current_data.keys():
                raise Exception("当前层级不存在:"+trace)
            #进入下一层级
            current_data = current_data[path][1]
        #删除数据
        #如果当前层级为列表，则key添加到列表中
        if isinstance(current_data, list):
            current_data.remove(key)
            return self
        #如果当前层级为字典，则添加到字典中
        if isinstance(current_data, dict):
            del current_data[key]
            return self
        
    def insert(self,value 
               ,root_path:str
               ,if_recursive:bool = False
               ):
        '''
            插入一项数据，如要插入一项后原数据为
            building = {
                texture = "path/to/texture"
                unlocking_technologies = {
		            intensive_agriculture
                    manufacturies                   <---插入位置
	            }
                possible = {
                        error_check = {
                            severity = fail
                        }
                }
            }
            则调用
            obj.insert("manufacturies","unlocking_technologies")
        '''
        self.add(value, "=", None, root_path, if_recursive)
    
    def trace(self, root_path:str):
        '''
            获取指定层级的数据
        '''
        root_path_list = root_path.split(".")
        #根据root_path_list，找到对应的层级
        current_data = self.data[self.get_name][1]
        trace = ""
        for path in root_path_list:
            trace = trace + path + "."
            #如果当前层级不存在,则报错
            if path not in current_data.keys():
                return None
                #raise Exception("当前层级不存在:"+trace)
            #进入下一层级
            current_data = current_data[path][1]
        return current_data
    
    # def init_from_file(self):
    #     result = parser_file(self.original_file)
    #     #获取result中非link_type_dict的第一个key
    #     key = ""
    #     for k in result.keys():
    #         if k != "link_type_dict":
    #             key = k
    #             break
    #     self.data[self.name] = ["=",result[key]]


    def output(self, output_file: str):
        output_to_txt(output_path=output_file, dict=self.data)

    def __str__(self) -> str:
        return str(self.data)
    
    def __getitem__(self, key):
        #如果key为int，则返回data中的第key项
        if isinstance(key, int):
            return self.data[key]
        #如果key为str，则返回data中第二项中的key项
        if isinstance(key, str):
            return self.data[1][key]
        raise Exception("key必须为int或str")

    
    
    
    
    @staticmethod
    def compile_template(template_list: list["BaseTemplate"],
                         output_file: str
                         ):
        '''
            编译模板,将多个模板合并为一个模板后输出
        '''
        result = {}
        for template in template_list:
            print(template.get_name)
            result[template.get_name] = template.data[template.get_name]
        output_to_txt(output_path=output_file, dict=result)




class BaseManager:
    '''
        模板管理器,对于每一个类都有一个对应的管理器
    '''
    def __init__(self,class_type:BaseTemplate,if_init=False):
        if not issubclass(class_type, BaseTemplate):
            raise Exception("class_type必须为BaseTemplate的子类")
        self.map = {}
        self.class_type = class_type
        #基于class_type创建一个新的类
        self.prototype = self.class_type(name="prototype",if_init=if_init)


    def set_property(self, name, property) -> None:
        '''
            设置属性
        '''
        self.map[name] = property

    def get_property(self, name,if_create:bool = True) -> BaseTemplate:
        '''
            获取属性
        '''
        property = self.map.get(name)
        if not property:
            if not if_create:
                return None
                #raise Exception("未找到对应的属性:"+name)
            #未找到对应的属性，则返回一个新的属性
            property = self.prototype._clone(name)
            self.map[name] = property
        return property
    
    def rename(self, old_name, new_name) -> None:
        '''
            重命名
        '''
        if old_name in self.map:
            self.map[new_name] = self.map.pop(old_name)
            self.map[new_name].rename(new_name)
        else:
            raise Exception("未找到对应的属性:"+old_name)
        
    def clone_from(self, prototype_name: str , new_name: str) -> BaseTemplate:
        '''
            从指定的一项克隆一个新的对象
        '''
        prototype = self.get_property(prototype_name, False)
        if not prototype:
            raise Exception("未找到对应的属性:"+prototype_name)
        result = prototype.clone_from(prototype, new_name)
        self.map[new_name] = result
        return result

    
    def output(self, output_file: str) -> None:
        '''
            输出
        '''
        BaseTemplate.compile_template(list(self.map.values()), output_file)
    
    def output_as_json(self, output_file: str) -> None:
        '''
            输出为json
        '''
        import json
        result = [
            it.data for it in self.map.values()
        ]
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(result, indent=4, ensure_ascii=False))

    def init_from_folder(self, folder_path: str) -> None:
        '''
            从文件夹初始化
        '''

        result, result_list = parser_folder(folder_path)
        for key in result:
            self.map[key] = self.prototype._clone(key)
            self.map[key].data = {
                key: result[key]
            }

    def keys(self) -> list:
        '''
            获取所有的key
        '''
        return self.map.keys()
        
    def pop(self, key) -> BaseTemplate:
        return self.map.pop(key)
    

    # manager输出时把map中的所有template合并输出
    def __iter__(self) -> iter:
        return iter(self.map.values())
    
    def __getitem__(self, key) -> BaseTemplate:
        return self.get_property(name=key, if_create=False)
    
    def __str__(self) -> str:
        list = []
        for key in self.map:
            
            list.append(str(self.map[key].data))
        return "\n".join(list)



            


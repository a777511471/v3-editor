# 对文件夹内的所有文件进行操作
import os
from utils.utils import ContentParser
from PyQt5.QtWidgets import *

def parser_file(path):
    '''
        @param path: 文件路径
    '''
    # 检测目标路径是否为txt文件，否则报错
    if not path.endswith('.txt'):
        raise Exception('目标路径不是txt文件')
    # 如果目标是txt文件,则进行解析
    # 检测是否包含bom头，如果有则去除
    # 如果目标是txt文件,则进行解析
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 检测是否包含bom头，如果有则去除
        if len(content) <= 1:
            result = {}
        else:
            if content.startswith('\ufeff'):
                content = content[1:]
                # 解析文件内容
            parser = ContentParser(content)
            result = parser.parse()
    return result


def parser_folder(path):
    '''
        @param path: 文件夹路径
    '''
    final_result = {}
    result_list = []
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        # 如果目标是文件夹，递归调用parser_folder，将返回的结果添加到最终结果中
        if os.path.isdir(file_path):
            result, result_list = parser_folder(file_path)
            for key in result:
                final_result[key] = result[key]
            result_list += result_list
            continue

        # 如果目标不是txt文件,则跳过
        if not file_path.endswith('.txt'):
            continue
        # 如果目标是txt文件,则进行解析
        try:
            result = parser_file(file_path)
        except Exception as e:
            print('文件解析错误：', file_path)
            QMessageBox.information(None, '错误', '文件解析错误：'+file_path+'\n'+str(e), QMessageBox.Ok)
            raise e
        # 将解析结果添加到列表中，并将解析结果中的每一项添加到最终结果中
        result_list.append(result)
        # 将解析结果中的每一项添加到最终结果中
        for key in result:
            final_result[key] = result[key]
    return final_result, result_list


# 返回指定文件夹下中所有txt文件的文件名序列
def get_all_txt_files(path) -> list:
    '''
        获取指定文件夹下中所有txt文件的文件名序列，包括子文件夹内的txt文件
        @param path: 文件夹路径
        @return: 文件名序列
    '''
    files = os.listdir(path)
    result = []
    for file in files:
        file_path = os.path.join(path, file)
        # 如果目标是文件夹，递归调用get_all_txt_files，将返回的结果添加到最终结果中
        if os.path.isdir(file_path):
            result += get_all_txt_files(file_path)
            continue
        # 如果目标不是txt文件,则跳过
        if not file_path.endswith('.txt'):
            continue
        # 如果目标是txt文件,则添加到最终结果中
        result.append(file_path)
    return result


# 按mod结构解析整个项目
def parser_default(path) -> dict:
    '''
        在给定的根目录下，按V3结构依次解析所有文件夹的内容
        @param path: 游戏或mod的根目录
        @return: 以文件夹名为key, 对应模板的manager为value的字典
    '''

    from utils.template import BaseManager
    from template.buildings import Buildings, Buildings_group, Pmg, Pm
    from template.goods import Goods

    from os.path import join

    result = {}

    # 解析building_groups,路径 path' , 'common' , 'building_groups
    building_groups_path = join(path, 'common', 'building_groups')
    building_groups_manager = BaseManager(Buildings_group)
    building_groups_manager.init_from_folder(building_groups_path)
    result['bg'] = building_groups_manager

    # 解析buildings,路径 path' , 'common' , 'buildings
    buildings_path = join(path, 'common', 'buildings')
    buildings_manager = BaseManager(Buildings)
    buildings_manager.init_from_folder(buildings_path)
    result['buildings'] = buildings_manager

    # 解析pmgs,路径 path' , 'common' , 'production_method_groups
    pmgs_path = join(path, 'common', 'production_method_groups')
    pmgs_manager = BaseManager(Pmg)
    pmgs_manager.init_from_folder(pmgs_path)
    result['pmgs'] = pmgs_manager

    # 解析pm,路径 path' , 'common' , 'production_methods
    pm_path = join(path, 'common', 'production_methods')
    pm_manager = BaseManager(Pm)
    pm_manager.init_from_folder(pm_path)
    result['pm'] = pm_manager

    # 解析goods,路径 path' , 'common' , 'goods
    goods_path = join(path, 'common', 'goods')
    goods_manager = BaseManager(Goods)
    goods_manager.init_from_folder(goods_path)
    result['goods'] = goods_manager

    return result


# 将指定的BaseManager输出成文件
def output_manager(manager, path, outputname='zzz_generated.txt'):
    '''
        将指定的BaseManager编译成文件
        @param manager: BaseManager对象
        @param path: 游戏或mod的根目录
        @param outputname: 输出文件名

    '''

    from utils.template import BaseManager
    from template.buildings import Buildings, Buildings_group, Pmg, Pm
    from template.goods import Goods

    from os.path import join

    # 检测outputname是存在后缀，如果没有则添加后缀 txt
    if not outputname.endswith('.txt'):
        outputname += '.txt'
        print("原文件名后缀不符合，已添加后缀 " + outputname)

    # 检测BaseManager中的class_type是否为Buildings_group
    if manager.class_type == Buildings_group:
        output_txt = os.path.join(path, 'common', 'building_groups', outputname)
        manager.output(output_txt)
        return

    # 检测BaseManager中的class_type是否为Buildings
    if manager.class_type == Buildings:
        output_txt = os.path.join(path, 'common', 'buildings', outputname)
        manager.output(output_txt)
        return

    # 检测BaseManager中的class_type是否为Pmg
    if manager.class_type == Pmg:
        output_txt = os.path.join(path, 'common', 'production_method_groups', outputname)
        manager.output(output_txt)
        return

    # 检测BaseManager中的class_type是否为Pm
    if manager.class_type == Pm:
        output_txt = os.path.join(path, 'common', 'production_methods', outputname)
        manager.output(output_txt)
        return

    # 检测BaseManager中的class_type是否为Goods
    if manager.class_type == Goods:
        output_txt = os.path.join(path, 'common', 'goods', outputname)
        manager.output(output_txt)
        return


def init_folder_structure(mod_base_path):
    '''
        初始化mod的文件夹结构
        @param mod_base_path: mod的根目录
    '''
    from os.path import join
    # 创建common文件夹
    common_path = join(mod_base_path, 'common')
    if not os.path.exists(common_path):
        os.makedirs(common_path)

    common_list = [
        'building_groups',
        'buildings',
        'production_method_groups',
        'production_methods',
        'goods',
    ]

    # 依次创建common下的文件夹
    for folder in common_list:
        folder_path = join(common_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    return

from utils.backend import BackendManager
from template.buildings import *


def get_buildings(BM: BackendManager):
    mods_list, raw_list = BM.get_part("buildings")
    ans = mods_list + raw_list
    return ans.sort()


def get_building_detail(BM: BackendManager, name: str):
    buildings, source = BM.get_part_detail("buildings", name)
    buildings: Buildings
    buildings_dict = {
        "name": buildings.get_name,
        "building_group": buildings.get_building_group(),
        "buildable": buildings.get_buildable(),
        "expandable": buildings.get_expandable(),
        "downsizeable": buildings.get_downsizeable(),
        "unique": buildings.get_unique(),
        "has_max_level": buildings.get_has_max_level(),
        "ignore_stateregion_max_level": buildings.get_ignore_stateregion_max_level(),
        "enable_air_connection": buildings.get_enable_air_connection(),
        "port": buildings.get_port(),
        "unlocking_technologies": buildings.get_unlocking_technologies(),
        "can_build": buildings.get_can_build(),
        "construction_points": buildings.get_construction_points(),
        "construction_modifier": buildings.get_construction_modifier(),
        "owners": buildings.get_owners(),
        "economic_contribution": buildings.get_economic_contribution(),
        "min_raise_to_hire": buildings.get_min_raise_to_hire(),
        "naval": buildings.get_naval(),
        "canal": buildings.get_canal(),
        "ai_value": buildings.get_ai_value(),
        "ai_subsidies_weight": buildings.get_ai_subsidies_weight(),
        "slaves_role": buildings.get_slaves_role(),
        "production_methods": buildings.get_production_methods(),
        "should_auto_expand": buildings.get_should_auto_expand(),
        "city_type": buildings.get_city_type(),
        "generates_residences": buildings.get_generates_residences(),
        "terrain_manipulator": buildings.get_terrain_manipulator(),
        "levels_per_mesh": buildings.get_levels_per_mesh(),
        "residence_points_per_level": buildings.get_residence_points_per_level(),
        "override_centerpiece_mesh": buildings.get_override_centerpiece_mesh(),
        "centerpiece_mesh_weight": buildings.get_centerpiece_mesh_weight(),
        "meshes": buildings.get_meshes(),
        "entity_not_constructed": buildings.get_entity_not_constructed(),
        "entity_under_construction": buildings.get_entity_under_construction(),
        "entity_constructed": buildings.get_entity_constructed(),
        "locator": buildings.get_locator(),
        "lens": buildings.get_lens()

    }
    return buildings_dict, source


def get_goods_detail(BM: BackendManager, name: str):
    goods, source = BM.get_part_detail("goods", name)
    return goods, source


def get_pm_detail(BM: BackendManager, name: str):
    pm, source = BM.get_part_detail("pm", name)
    pm: Pm
    pm_dict = {
        "name": pm.get_name,
        "input": pm.get_inputs(),
        "output": pm.get_outputs(),
        "level": pm.get_level_scaled(),
        "unscaled": pm.get_unscaled(),
        "texture": pm.get_texture(),
        "is_default": pm.get_is_default(),
        "country_modifiers_workforce": pm.get_country_modifiers_workforce(),
        "country_modifiers_level": pm.get_country_modifiers_level(),
        "country_modifiers_unscaled": pm.get_country_modifiers_unscaled(),
        "state_modifiers_workforce": pm.get_state_modifiers_workforce(),
        "state_modifiers_level": pm.get_state_modifiers_level(),
        "state_modifiers_unscaled": pm.get_state_modifiers_unscaled(),
        "timed_modifiers": pm.get_timed_modifiers(),
        "required_input_goods": pm.get_required_input_goods(),
        "unlocking_laws": pm.get_unlocking_laws(),
        "unlocking_technologies": pm.get_unlocking_technologies(),
        "unlocking_production_methods": pm.get_unlocking_production_methods(),
        "unlocking_global_technologies": pm.get_unlocking_global_technologies(),
        "ai_weight": pm.get_ai_weight(),
        "pollution_generation": pm.get_pollution_generation()
    }
    return pm_dict, source


def get_pmg_detail(BM: BackendManager, name: str):
    pmg, source = BM.get_part_detail("pmgs", name)
    pmg: Pmg
    pmg_dict = {
        "name": pmg.get_name,
        "production_methods": pmg.get_pms(),
        "is_hidden_when_unavailable": pmg.get_is_hidden_when_unavailable(),
        "ai_selection": pmg.get_ai_selection(),
        "texture": pmg.get_texture()
    }
    return pmg_dict, source

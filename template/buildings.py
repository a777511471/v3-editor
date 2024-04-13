from utils.template import BaseTemplate


class Buildings_group(BaseTemplate):
    def __init__(self, name, if_init=False):
        original_file = "template/original/buildings_groups.txt"
        super().__init__(name, original_file, if_init)

    def _clone(self, name):
        return Buildings_group(name, self.if_init)


class Buildings(BaseTemplate):
    def __init__(self, name, if_init=False):
        original_file = "template/original/buildings.txt"
        super().__init__(name, original_file, if_init)

    def _clone(self, name):
        return Buildings(name, self.if_init)

    def set_texture(self, texture_path):
        self.add("texture", "=", texture_path)

    def set_city_type(self, city_type):
        self.add("city_type", "=", city_type)

    def set_lpm(self, lpm):
        self.add("level_per_mesh", "=", lpm)

    # unlocking_technologies
    def add_unlocking_technology(self, tech):
        self.insert(tech, "unlocking_technologies", True)

    def remove_unlocking_technology(self, tech):
        self.delete(tech, "unlocking_technologies")

    def get_unlocking_technologies(self):
        return self.trace("unlocking_technologies")

    # production_method_groups
    def add_production_method_group(self, pmg):
        self.insert(pmg, "production_method_groups", True)

    def remove_production_method_group(self, pmg):
        self.delete(pmg, "production_method_groups")

    def get_production_method_groups(self):
        return self.trace("production_method_groups")

    # required_construction
    def set_required_construction(self, construction):
        self.add("required_construction", "=", construction)

    def get_required_construction(self):
        return self.trace("required_construction")

    def get_building_group(self):
        return self.trace("required_construction")

    def get_buildable(self):
        return self.trace("buildable")

    def get_expandable(self):
        return self.trace("expandable")

    def get_downsizeable(self):
        return self.trace("downsizeable")

    def get_unique(self):
        return self.trace("unique")

    def get_has_max_level(self):
        return self.trace("has_max_level")

    def get_ignore_stateregion_max_level(self):
        return self.trace("ignore_stateregion_max_level")

    def get_enable_air_connection(self):
        return self.trace("enable_air_connection")

    def get_port(self):
        return self.trace("port")

    def get_can_build(self):
        return self.trace("can_build")

    def get_construction_points(self):
        return self.trace("required_construction")

    def get_construction_modifier(self):
        return self.trace("construction_modifier")

    def get_owners(self):
        return self.trace("owners")

    def get_economic_contribution(self):
        return self.trace("economic_contribution")

    def get_min_raise_to_hire(self):
        return self.trace("min_raise_to_hire")

    def get_naval(self):
        return self.trace("naval")

    def get_canal(self):
        return self.trace("canal")

    def get_ai_value(self):
        return self.trace("ai_value")

    def get_ai_subsidies_weight(self):
        return self.trace("ai_subsidies_weight")

    def get_slaves_role(self):
        return self.trace("slaves_role")

    def get_production_methods(self):
        return self.trace("production_method_groups")

    def get_should_auto_expand(self):
        return self.trace("should_auto_expand")

    def get_city_type(self):
        return self.trace("city_type")

    def get_generates_residences(self):
        return self.trace("generates_residences")

    def get_terrain_manipulator(self):
        return self.trace("terrain_manipulator")

    def get_levels_per_mesh(self):
        return self.trace("levels_per_mesh")

    def get_residence_points_per_level(self):
        return self.trace("residence_points_per_level")

    def get_override_centerpiece_mesh(self):
        return self.trace("override_centerpiece_mesh")

    def get_centerpiece_mesh_weight(self):
        return self.trace("centerpiece_mesh_weight")

    def get_meshes(self):
        return self.trace("meshes")

    def get_entity_not_constructed(self):
        return self.trace("entity_not_constructed")

    def get_entity_under_construction(self):
        return self.trace("entity_under_construction")

    def get_entity_constructed(self):
        return self.trace("entity_constructed")

    def get_locator(self):
        return self.trace("locator")

    def get_lens(self):
        return self.trace("lens")


class Pmg(BaseTemplate):
    def __init__(self, name, if_init=False, Buildings: Buildings = None):
        original_file = "template/original/production_method_groups.txt"
        super().__init__(name, original_file, if_init)
        if Buildings:
            self.bind(Buildings)

    def bind(self, Building: Buildings):
        Building.insert(self.get_name, "production_methods", True)

    def _clone(self, name):
        return Pmg(name, self.if_init)

    def add_pm(self, pm_name):
        self.insert(pm_name, "production_methods", True)

    def rm_pm(self, pm_name):
        self.delete(pm_name, "production_methods")

    def get_pms(self):
        return self.trace("production_methods")

    def set_texture(self, texture_path):
        self.add("texture", "=", texture_path)

    def get_is_hidden_when_unavailable(self):
        return self.trace("is_hidden_when_unavailable")

    def get_ai_selection(self):
        return self.trace("ai_selection")

    def get_texture(self):
        return self.trace("texture")


class Pm(BaseTemplate):
    def __init__(self, name, if_init=False, Pmg: Pmg = None):
        original_file = "template/original/production_methods.txt"
        super().__init__(name, if_init)
        if Pmg:
            self.bind(Pmg)

    def bind(self, Pmg: Pmg):
        Pmg.insert(self.get_name, "production_methods", True)

    def _clone(self, name):
        return Pm(name, self.if_init)

    def set_texture(self, texture_path):
        self.add("texture", "=", texture_path)

    def add_input(self, good, amount):
        path = "building_modifiers.workforce_scaled"

        key = "goods_input_" + good + "_add"
        self.add(key, "=", amount, path, True)

    def remove_input(self, good):
        key = "goods_input_" + good + "_add"
        path = "building_modifiers.workforce_scaled"
        self.delete(key, path)

    def get_inputs(self):
        goods_dict = self.trace("building_modifiers.workforce_scaled")
        result = {}
        if goods_dict is None:
            return result
        # 解析存在的输入
        for good in goods_dict:
            if good.startswith("goods_input_"):
                good_name = good.split("_")[2]
                result[good_name] = goods_dict[good][1]

        return result

    def get_outputs(self):
        goods_dict = self.trace("building_modifiers.workforce_scaled")
        result = {}

        if goods_dict is None:
            return result
        # 解析存在的输入
        for good in goods_dict:
            if good.startswith("goods_output_"):
                good_name = good.split("_")[2]
                result[good_name] = goods_dict[good][1]

        return result

    def add_output(self, good, amount):
        path = "building_modifiers.workforce_scaled"

        key = "goods_output_" + good + "_add"
        self.add(key, "=", amount, path, True)

    def get_level_scaled(self):
        return self.trace("building_modifiers.level_scaled")

    def get_unscaled(self):
        return self.trace("building_modifiers.unscaled")

    def get_country_modifiers_workforce(self):
        return self.trace("country_modifiers.workforce_scaled")

    def get_country_modifiers_level(self):
        return self.trace("country_modifiers.level_scaled")

    def get_country_modifiers_unscaled(self):
        return self.trace("country_modifiers.unscaled")

    def get_state_modifiers_workforce(self):
        return self.trace("state_modifiers.workforce_scaled")

    def get_state_modifiers_level(self):
        return self.trace("state_modifiers.level_scaled")

    def get_state_modifiers_unscaled(self):
        return self.trace("state_modifiers.unscaled")

    def get_timed_modifiers(self):
        return self.trace("timed_modifier")

    def get_texture(self):
        return self.trace("texture")

    def get_required_input_goods(self):
        return self.trace("required_input_goods")

    def get_is_default(self):
        return self.trace("is_default")

    def get_unlocking_laws(self):
        return self.trace("unlocking_laws")

    def get_unlocking_technologies(self):
        return self.trace("unlocking_technologies")

    def get_unlocking_production_methods(self):
        return self.trace("unlocking_production_methods")

    def get_unlocking_global_technologies(self):
        return self.trace("unlocking_global_technologies")

    def get_ai_weight(self):
        return self.trace("ai_weight")

    def get_pollution_generation(self):
        return self.trace("pollution_generation")

    def remove_output(self, good):
        key = "goods_output_" + good + "_add"
        path = "building_modifiers.workforce_scaled"
        self.delete(key, path)

    def add_employee(self, type, amount):
        path = "building_modifiers.level_scaled"
        key = "building_employment_" + type + "_add"
        self.add(key, "=", amount, path, True)

    def remove_employee(self, type):
        path = "building_modifiers.level_scaled"
        key = "building_employment_" + type + "_add"
        self.delete(key, path)

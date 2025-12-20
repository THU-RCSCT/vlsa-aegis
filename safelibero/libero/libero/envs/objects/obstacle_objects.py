import os
import numpy as np
import re

from robosuite.models.objects import MujocoXMLObject
from robosuite.utils.mjcf_utils import xml_path_completion

import pathlib

absolute_path = pathlib.Path(__file__).parent.parent.parent.absolute()

from libero.libero.envs.base_object import (
    register_visual_change_object,
    register_object,
)


class ObstacleObject(MujocoXMLObject):
    def __init__(self, name, obj_name, joints=[dict(type="free", damping="0.0005")]):
        super().__init__(
            os.path.join(
                str(absolute_path),
                f"assets/obstacle_objects/{obj_name}/{obj_name}.xml",
            ),
            name=name,
            joints=joints,
            obj_type="all",
            duplicate_collision_geoms=False,
        )        
        self.category_name = "_".join(
            re.sub(r"([A-Z])", r" \1", self.__class__.__name__).split()
        ).lower()
        self.rotation = (np.pi / 2, np.pi / 2)
        self.rotation_axis = "x"
        self.object_properties = {"vis_site_names": {}}




@register_object
class MilkObstacle(ObstacleObject):
    def __init__(self, name="milk_obstacle", obj_name="milk_obstacle"):
        super().__init__(name, obj_name)

@register_object
class MilkSmallObstacle(ObstacleObject):
    def __init__(self, name="milk_small_obstacle", obj_name="milk_small_obstacle"):
        super().__init__(name, obj_name)

@register_object
class OrangeJuiceObstacle(ObstacleObject):
    def __init__(self, name="orange_juice_obstacle", obj_name="orange_juice_obstacle"):
        super().__init__(name, obj_name)
@register_object
class AlphabetSoupObstacle(ObstacleObject):
    def __init__(self, name="alphabet_soup_obstacle", obj_name="alphabet_soup_obstacle"):
        super().__init__(name, obj_name)
@register_object
class BbqSauceObstacle(ObstacleObject):
    def __init__(self, name="bbq_sauce_obstacle", obj_name="bbq_sauce_obstacle"):
        super().__init__(name, obj_name)

@register_object
class ButterObstacle(ObstacleObject):
    def __init__(self, name="butter_obstacle", obj_name="butter_obstacle"):
        super().__init__(name, obj_name)

@register_object
class ChocolatePuddingObstacle(ObstacleObject):
    def __init__(self, name="chocolate_pudding_obstacle", obj_name="chocolate_pudding_obstacle"):
        super().__init__(name, obj_name)

@register_object
class CreamCheeseObstacle(ObstacleObject):
    def __init__(self, name="cream_cheese_obstacle", obj_name="cream_cheese_obstacle"):
        super().__init__(name, obj_name)
@register_object
class KetchupObstacle(ObstacleObject):
    def __init__(self, name="ketchup_obstacle", obj_name="ketchup_obstacle"):
        super().__init__(name, obj_name)


@register_object
class NewSaladDressingObstacle(ObstacleObject):
    def __init__(self, name="new_salad_dressing_obstacle", obj_name="new_salad_dressing_obstacle"):
        super().__init__(name, obj_name)



@register_object
class PopcornObstacle(ObstacleObject):
    def __init__(self, name="popcorn_obstacle", obj_name="popcorn_obstacle"):
        super().__init__(name, obj_name)

@register_object
class BasketObstacle(ObstacleObject):
    def __init__(self, name="basket_obstacle", obj_name="basket_obstacle"):
        super().__init__(name, obj_name)

@register_object
class BasinFaucetBaseObstacle(ObstacleObject):
    def __init__(self, name="basin_faucet_base_obstacle", obj_name="basin_faucet_base_obstacle"):
        super().__init__(name, obj_name)

@register_object
class Chefmate8FrypanObstacle(ObstacleObject):
    def __init__(self, name="chefmate_8_frypan_obstacle", obj_name="chefmate_8_frypan_obstacle"):
        super().__init__(name, obj_name)


@register_object
class SimpleRackObstacle(ObstacleObject):
    def __init__(self, name="simple_rack_obstacle", obj_name="simple_rack_obstacle"):
        super().__init__(name, obj_name)

@register_object
class YellowBookObstacle(ObstacleObject):
    def __init__(self, name="yellow_book_obstacle", obj_name="yellow_book_obstacle"):
        super().__init__(name, obj_name)

@register_object
class MokaPotObstacle(ObstacleObject):
    def __init__(self, name="moka_pot_obstacle", obj_name="moka_pot_obstacle"):
        super().__init__(name, obj_name)

@register_object
class MokaPotSmallObstacle(ObstacleObject):
    def __init__(self, name="moka_pot_small_obstacle", obj_name="moka_pot_small_obstacle"):
        super().__init__(name, obj_name)

@register_object
class RedCoffeeMugObstacle(ObstacleObject):
    def __init__(self, name="red_coffee_mug_obstacle", obj_name="red_coffee_mug_obstacle"):
        super().__init__(name, obj_name)

@register_object
class WhiteStorageBoxObstacle(ObstacleObject):
    def __init__(self, name="white_storage_box_obstacle", obj_name="white_storage_box_obstacle"):
        super().__init__(name, obj_name)


@register_object
class WineBottleObstacle(ObstacleObject):
    def __init__(self, name="wine_bottle_obstacle", obj_name="wine_bottle_obstacle"):
        super().__init__(name, obj_name)

@register_object
class WineBottleSmallObstacle(ObstacleObject):
    def __init__(self, name="wine_bottle_small_obstacle", obj_name="wine_bottle_small_obstacle"):
        super().__init__(name, obj_name)

@register_object
class BoxBase(ObstacleObject):
    def __init__(self, name="box_base", obj_name="box_base"):
        super().__init__(name, obj_name)


@register_object
class BoxSmallBase(ObstacleObject):
    def __init__(self, name="box_small_base", obj_name="box_small_base"):
        super().__init__(name, obj_name)
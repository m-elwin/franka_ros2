from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("fer", package_name="fer_moveit_config").to_moveit_configs()
    moveit_config.move_group_capabilities["capabilities"] = "" # work around for a bug in generate_move_group_launch
    return generate_move_group_launch(moveit_config)

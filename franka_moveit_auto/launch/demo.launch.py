from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("fer", package_name="franka_moveit_auto").to_moveit_configs()
    x = generate_demo_launch(moveit_config)
    print(x)
    return x

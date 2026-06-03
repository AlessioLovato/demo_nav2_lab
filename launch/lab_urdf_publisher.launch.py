from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )

    topic_name_arg = DeclareLaunchArgument(
        'topic_name',
        default_value='/lab_description',
        description='The name of the topic to publish the URDF of the lab environment'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')
    urdf_path = os.path.join(
        get_package_share_directory('demo_nav2_lab'),
        'urdf',
        'lab_mesh.urdf'
    )

    with open(urdf_path, 'r', encoding='utf-8') as urdf_file:
        robot_description = urdf_file.read()

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='lab_robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': robot_description},
            {'use_sim_time': use_sim_time},
        ],
        remappings=[
            ('/robot_description', LaunchConfiguration('topic_name')),
        ]
    )

    static_map_to_lab = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='map_to_lab_link_static_tf',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'lab_link'],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    return LaunchDescription([
        use_sim_time_arg,
        topic_name_arg,
        robot_state_publisher,
        # static_map_to_lab,
    ])

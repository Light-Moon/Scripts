import os
from resource_management.libraries.functions.constants import Direction
from resource_management.libraries.functions import default
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.version import format_stack_version
from resource_management.libraries.functions import format
from resource_management.libraries.functions.stack_features import check_stack_feature
from resource_management.libraries.functions import StackFeature

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()

# upgrade params
stack_name = default("/hostLevelParams/stack_name", None)
upgrade_direction = default("/commandParams/upgrade_direction", Direction.UPGRADE)
stack_version_unformatted = config['hostLevelParams']['stack_version']
stack_version_formatted = format_stack_version(stack_version_unformatted)

ctdfs_conf_dir = '/etc/ctdfs/conf'
if stack_version_formatted and check_stack_feature(StackFeature.ROLLING_UPGRADE, stack_version_formatted):
    ctdfs_conf_dir = format('{stack_root}/current/ctdfs/conf')
#!/usr/bin/env python
import os
import sys
from pathlib import Path
from faraday_plugins.plugins.manager import PluginsManager, ReportAnalyzer


def main():
    my_envs = os.environ
    # If the script is run outside the dispatcher
    # the environment variables
    # are checked.

    tool = os.environ.get('EXECUTOR_CONFIG_TOOL', None)

    if 'EXECUTOR_CONFIG_REPORT_NAME' in my_envs:
        report_name = os.environ.get('EXECUTOR_CONFIG_REPORT_NAME')
    else:
        print(
            "Param REPORT_NAME no set",
            file=sys.stderr
        )
        sys.exit()

    if 'REPORT_DIR' in my_envs:
        report_dir = os.environ.get('REPORT_DIR')
    else:
        print(
            "Environment variable REPORT_DIR no set",
            file=sys.stderr
        )
        sys.exit()

    filename = Path(report_dir) / report_name
    manager = PluginsManager()

    if tool is not None:
        plugin = manager.get_plugin(tool)
    else:
        plugin = ReportAnalyzer(manager).get_plugin(filename)

    with open(filename, 'r') as f:
        plugin.parseOutputString(f.read())
        print(plugin.get_json())


if __name__ == '__main__':
    main()

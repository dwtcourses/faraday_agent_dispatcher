#!/usr/bin/env python
import os
import sys
from faraday_plugins.plugins.manager import PluginsManager
import subprocess
import tempfile
from pathlib import Path


def main():
    url_target = os.environ.get('EXECUTOR_CONFIG_W3AF_TARGET_URL')
    if not url_target:
        print("URL not provided", file=sys.stderr)
        sys.exit()

    # If the script is run outside the dispatcher the environment variables are checked.
    # ['W3AF_PATH']
    if 'W3AF_PATH' in os.environ:
        with tempfile.TemporaryDirectory() as tempdirname:
            name_result = Path(tempdirname) / 'config_report_file.w3af'

            with open(name_result, 'w') as f:
                command_text = f'plugins\n output console,xml_file\n output\n output config xml_file\n ' \
                               f'set output_file {tempdirname}/output-w3af.xml\n set verbose True\n back\n ' \
                               f'output config console\n set verbose False\n back\n crawl all, !bing_spider, ' \
                               f'!google_spider, !spider_man\n crawl\n grep all\n grep\n audit all\n audit\n ' \
                               f'bruteforce all\n bruteforce\n back\n target\n set target {url_target}\n ' \
                               f'back\n start\n exit'
                f.write(command_text)

            try:
                os.chdir(path=os.environ.get('W3AF_PATH'))

            except FileNotFoundError:
                print(f'The directory where w3af is located could not be found. Check environment variable W3AF_PATH = '
                      f'{os.environ.get("W3AF_PATH")}', file=sys.stderr)
                sys.exit()

            if os.path.isfile('w3af_console'):
                w3af_process = subprocess.run(f'./w3af_console -s {name_result}', shell=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
                if len(w3af_process.stdout) > 0:
                    print(f"W3AF stdout: {w3af_process.stdout.decode('utf-8')}", file=sys.stderr)
                if len(w3af_process.stderr) > 0:
                    print(f"W3AF stderr: {w3af_process.stderr.decode('utf-8')}", file=sys.stderr)

                plugin = PluginsManager().get_plugin("w3af")
                plugin.parseOutputString(f'{tempdirname}/output-w3af.xml')
                print(plugin.get_json())
            else:
                print(f'w3af_console file could not be found. For this reason the command cannot be run.'
                      f'Actual value = {os.environ.get("W3AF_PATH")}/w3af_console ', file=sys.stderr)
                sys.exit()

    else:
        print("W3AF_PATH not set", file=sys.stderr)
        sys.exit()


if __name__ == '__main__':
    main()
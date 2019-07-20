#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Base.application import manager
from flask_script import Server
from Base.routeConfig.routeConfig import *

manager.add_command("runapi", Server(host='0.0.0.0', port=app.config['SERVER_PORT'], use_debugger=app.config['DEBUG']))


def main():
    # manager.run()
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()

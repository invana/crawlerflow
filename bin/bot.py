# -*- coding: utf-8 -*-
import sys
import os
invana_bot_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append("{}/../".format(invana_bot_path))

from invana_bot.cmd.run import invana_bot_run

invana_bot_run()

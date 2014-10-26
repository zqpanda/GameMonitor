#!/bin/env python
# -*- coding:utf-8 -*-

import logging
logging.basicConfig(
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    filename='../log/monitor.log',
    level=logging.DEBUG,
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

{% if cookiecutter.abort_pre_gen == "yes" %}
sys.exit(1)
{% else %}
sys.exit(0)
{% endif %}

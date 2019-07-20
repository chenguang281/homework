#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

class UUIDUtils:

    @staticmethod
    def gen_id():
        return uuid.uuid4().hex
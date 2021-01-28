#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Microsoft App id : 4752eb87-8ffe-4677-981c-7159eb0688a2
# Microsoft app pwd: __2gI8QcpWRq8G-svc9Xp4OGW-sY.uj3W~

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "bc4fdbe8-a324-4513-bcc7-5510260dd85d")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "jfor5qLdi8pf8t5Cjj-Hz_~9-KjA.vgb4_")

#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "78287145-538e-4eec-8177-e4214c13f1e4")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "TU_sVUebtCf8F_ZyRQ7XCJ25~m_Idd4eF3")

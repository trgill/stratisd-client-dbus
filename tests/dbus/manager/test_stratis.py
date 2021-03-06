# Copyright 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test 'stratisd'.
"""

import time
import unittest

from stratisd_client_dbus import Manager
from stratisd_client_dbus import get_object

from stratisd_client_dbus._constants import TOP_OBJECT
from stratisd_client_dbus._implementation import ManagerSpec

from .._misc import checked_property
from .._misc import Service

_PN = ManagerSpec.PropertyNames

class StratisTestCase(unittest.TestCase):
    """
    Test meta information about stratisd.
    """

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)
        self._proxy = get_object(TOP_OBJECT)
        Manager.ConfigureSimulator(self._proxy, denominator=8)

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testStratisVersion(self):
        """
        Getting version should succeed.

        Major version number should be 0.
        """
        version = checked_property(
           Manager.Properties.Version(get_object(TOP_OBJECT)),
           ManagerSpec.PROPERTY_SIGS[_PN.Version]
        )
        (major, _, _) = version.split(".")
        self.assertEqual(major, "0")

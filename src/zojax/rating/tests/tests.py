##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import os, unittest, doctest
from zope import interface, schema
from zope.app.testing.functional import ZCMLLayer

from zojax.content.type.item import PersistentItem
from zojax.content.type.interfaces import IItem

zojaxRatingLayer = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxRatingLayer', allow_teardown=True)


class ITestContent(IItem):

    text = schema.Text(title = u'Text')


class TestContent(PersistentItem):
    interface.implements(ITestContent)

    text = u''


def test_suite():
    testbrowser = doctest.DocFileSuite(
        "tests.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    testbrowser.layer = zojaxRatingLayer

    return unittest.TestSuite((testbrowser,))

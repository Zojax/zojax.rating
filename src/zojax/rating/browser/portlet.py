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
from zope.security import checkPermission
from zope.traversing.browser import absoluteURL
from zope.cachedescriptors.property import Lazy
from lovely.rating.interfaces import IRatable

from zojax.rating.browser.rate import RateForm
from zojax.rating.interfaces import IAverageRating


class RatingPortlet(object):

    def update(self):
        if not self.isAvailable():
            return
        try:
            context = self.manager.view.maincontext
        except AttributeError:
            context = self.context
        self.contextURL = absoluteURL(context, self.request)
        if self.allowRate:
            self.form = RateForm(context, self.request)
            self.form.update()

    @Lazy
    def average(self):
        context = self.manager.view.maincontext
        averageRating = IAverageRating(context, None)
        if averageRating is None:
            return None
        return averageRating.average

    @Lazy
    def allowRate(self):
        context = self.manager.view.maincontext
        return checkPermission('zojax.rating.Rate', context)

    def isAvailable(self):
        if self.manager.view is None:
            return False

        try:
            context = self.manager.view.maincontext
        except AttributeError:
            context = self.context

        if not IRatable.providedBy(context):
            return False

        return self.average is not None or self.allowRate

    @Lazy
    def averageAsString(self):
        return "%i_%s" % (int(self.average),
                          self.average % 1 > 0.4 and '5' or '0')

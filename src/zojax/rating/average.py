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
from zope import interface, component
from lovely.rating.interfaces import IRatable, IRatingsManager

from interfaces import IAverageRating
from rating import OVERALL_RATING_DEFINITION_NAME, overallRatingDefinition


class AverageRating(object):
    interface.implements(IAverageRating)
    component.adapts(IRatable)

    def __init__(self, context):
        self.context = context

    @property
    def average(self, defn = overallRatingDefinition):
        manager = IRatingsManager(self.context)

        total = 0.0
        rates = manager.getRatings(OVERALL_RATING_DEFINITION_NAME)
        if not rates:
            return None

        for rate in rates:
            total += defn.scoreSystem.getNumericalValue(rate.value)

        average = total / len(rates)
        return average

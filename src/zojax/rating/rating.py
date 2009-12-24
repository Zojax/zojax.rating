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
from lovely.rating.definition import RatingDefinition
from lovely.rating.scoresystem import SimpleScoreSystem

from zojax.rating.interfaces import _, OVERALL_RATING_DEFINITION_NAME


fiveSteps = SimpleScoreSystem(
    'fiveSteps', _(u"Five Steps"), _(u"A five step scoring system"),
    [(u"5", 5),
     (u"4", 4),
     (u"3", 3),
     (u"2", 2),
     (u"1", 1)])

overallRatingDefinition = RatingDefinition(_(u"Overall Rating"), fiveSteps)

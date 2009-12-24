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
from zope import interface, schema, event
from zope.lifecycleevent import ObjectModifiedEvent
from zope.traversing.browser import absoluteURL
from lovely.rating.interfaces import IRatingsManager

from z3c.form.form import Form
from z3c.form.field import Fields
from z3c.form.button import buttonAndHandler

from zojax.rating.interfaces import _, OVERALL_RATING_DEFINITION_NAME
from zojax.statusmessage.interfaces import IStatusMessage


class IRateForm(interface.Interface):

    rate = schema.Choice(
        title=_(u"Your rating"),
        required=True,
        values=(u'--',
                u'5',
                u'4',
                u'3',
                u'2',
                u'1'),
        default=u'--')


class RateHelper(object):
    interface.implements(IRateForm)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getRate(self):
        manager = IRatingsManager(self.context)
        rate = manager.getRating(
            OVERALL_RATING_DEFINITION_NAME, self.request.principal.id)
        if rate is None:
            return u'--'
        else:
            return rate.value

    def setRate(self, value):
        manager = IRatingsManager(self.context)
        if value == u'--':
            manager.remove(
                OVERALL_RATING_DEFINITION_NAME, self.request.principal.id)
        else:
            manager.rate(
                OVERALL_RATING_DEFINITION_NAME, value, self.request.principal.id)

        # Invoke ObjectModifedEvent to reindex the rated object in catalog
        event.notify(ObjectModifiedEvent(self.context))

    rate = property(getRate, setRate)


class RateForm(Form):

    fields = Fields(IRateForm)
    label = _("Rate Form")

    def render(self):
        return u''

    def getContent(self):
        return RateHelper(self.context, self.request)

    @buttonAndHandler(_('Rate'), name='rate')
    def handleRate(self, action):
        data, errors = self.extractData()
        self.data = data
        contextURL = absoluteURL(self.context, self.request)
        if errors:
            IStatusMessage(self.request).add(self.formErrorsMessage, 'warning')
            self.request.response.redirect(contextURL)
            return

        rate = data['rate']
        self.getContent().rate = rate
        IStatusMessage(self.request).add(_(u"Your rating was saved"))
        self.request.response.redirect(contextURL)

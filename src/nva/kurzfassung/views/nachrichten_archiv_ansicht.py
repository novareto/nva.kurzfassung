# -*- coding: utf-8 -*-

import DateTime
from plone import api
from nva.kurzfassung import _
from nva.kurzfassung.views.erweiterte_kurzfassung import ErweiterteKurzfassung
from Products.Five.browser import BrowserView


class NachrichtenArchivAnsicht(ErweiterteKurzfassung):
    """ Erbt von der Erweiterten Kurzfassung """

    @property
    def query(self):
        end = DateTime.DateTime() - 60 # If we have some clock skew peek a little to the future
        start = DateTime.DateTime() - 365
        date_range_query = { 'query':(start,end), 'range': 'min:max'}
        pathes = []
        path = u''.join(self.context.getPhysicalPath(), '/')
        pathes.append(path)
        if hasattr(self.context, 'newsfolder'):
            if self.context.newsfolder:
                for i in self.context.newsfolder:
                    pathes.append(u''.join(i.to_object.getPhysicalPath(), '/'))
        brains = api.content.find(portal_type="News Item", path=pathes, created=date_range_query, sort_on='created', sort_order='reverse')
        return brains

    def aktuelllink(self):
        return self.context.absolute_url()

# -*- coding: utf-8 -*-
import DateTime
from plone import api
from nva.kurzfassung import _
from nva.kurzfassung.views.erweiterte_kurzfassung import ErweiterteKurzfassung
from Products.Five.browser import BrowserView
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

class NachrichtenAnsicht(ErweiterteKurzfassung):
    """Ansicht erbt von der Erweiterten Kurzfassung"""

    @property
    def query(self):
        registry = getUtility(IRegistry)
        archivzeit = registry['nva.folderbehaviors.interfaces.ISchmuckbilder.archivzeit']
        end = DateTime.DateTime() + 0.1 # If we have some clock skew peek a little to the future
        start = DateTime.DateTime() - archivzeit
        date_range_query = { 'query':(start,end), 'range': 'min:max'}
        pathes = []
        path = u'/'.join(self.context.getPhysicalPath())
        pathes.append(path)
        if hasattr(self.context, 'newsfolder'):
            if self.context.newsfolder:
                for i in self.context.newsfolder:
                    pathes.append(u''.join(i.to_object.getPhysicalPath(), '/'))
        brains = api.content.find(portal_type="News Item", path=pathes, created=date_range_query, sort_on='created', sort_order='reverse')
        return brains

    def archivlink(self):
        return self.context.absolute_url() + '/@@archiv_nachricht_view'

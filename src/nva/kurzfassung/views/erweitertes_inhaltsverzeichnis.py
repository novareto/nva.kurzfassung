# -*- coding: utf-8 -*-

from nva.kurzfassung import _
from Products.Five.browser import BrowserView


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ErweitertesInhaltsverzeichnis(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('enhanced_contentdir.pt')

    def __call__(self):
        self.msg = _(u'A small message')
        return self.index()

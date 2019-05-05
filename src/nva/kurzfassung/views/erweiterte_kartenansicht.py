# -*- coding: utf-8 -*-

from nva.kurzfassung import _
from nva.kurzfassung.views.erweiterte_kurzfassung import ErweiterteKurzfassung
from Products.Five.browser import BrowserView


class ErweiterteKartenansicht(ErweiterteKurzfassung):
    """Content-Liste wird von der erweiterten Kurzfassung geerbt und adaptiert"""

    def cardlist(self):
        return [self.contentlist()[i:i+2] for i in range(0, len(self.contentlist()), 2)]

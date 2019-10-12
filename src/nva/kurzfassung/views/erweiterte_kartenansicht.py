# -*- coding: utf-8 -*-

from nva.kurzfassung import _
from nva.kurzfassung.views.erweiterte_kurzfassung import ErweiterteKurzfassung
from Products.Five.browser import BrowserView


class ErweiterteKartenansicht(ErweiterteKurzfassung):
    """Content-Liste wird von der erweiterten Kurzfassung geerbt und adaptiert"""

    def cardlist(self):
        size = 3
        if hasattr(self.context, 'columns'):
            if self.context.columns:
                size = self.context.columns
        artikel = self.contentlist()
        return [artikel[i:i+size] for i in range(0, len(artikel), size)]

# -*- coding: utf-8 -*-

from nva.kurzfassung import _
from nva.kurzfassung.views.erweiterte_kurzfassung import ErweiterteKurzfassung
from Products.Five.browser import BrowserView

class ZweiSpaltenAnsicht(ErweiterteKurzfassung):
    """Erbt von der erweiterten Kurzfassung"""

    def __call__(self):
        return self.index()

class ZweiSpaltenContext(ErweiterteKurzfassung):
    """Erbt von der erweiterten Kurzfassung"""

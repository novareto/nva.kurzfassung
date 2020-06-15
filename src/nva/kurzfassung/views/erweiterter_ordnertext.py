# -*- coding: utf-8 -*-

from nva.kurzfassung import _
from nva.kurzfassung.views.erweiterte_kurzfassung import ErweiterteKurzfassung
from Products.Five.browser import BrowserView


class ErweiterterOrdnertext(ErweiterteKurzfassung):
    """Content-Liste wird von der Erweiterten Kurzfassung geerbt."""

# -*- coding: utf-8 -*-

from nva.kurzfassung import _
from nva.kurzfassung.views.nachrichten_ansicht import NachrichtenAnsicht
from Products.Five.browser import BrowserView


class NachrichtenListe(NachrichtenAnsicht):
    """ Erbt von der Nachrichten Ansicht """

    def archivlink(self):
        return self.context.absolute_url() + '/@@archiv_nachricht_liste_view'


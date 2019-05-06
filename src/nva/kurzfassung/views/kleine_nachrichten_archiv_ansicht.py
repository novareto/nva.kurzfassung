# -*- coding: utf-8 -*-

from nva.kurzfassung import _
from nva.kurzfassung.views.nachrichten_archiv_ansicht import NachrichtenArchivAnsicht
from Products.Five.browser import BrowserView


class KleineNachrichtenArchivAnsicht(NachrichtenArchivAnsicht):
    """ Erbt von der Nachrichten Ansicht """

    def aktuelllink(self):
        return self.context.absolute_url()

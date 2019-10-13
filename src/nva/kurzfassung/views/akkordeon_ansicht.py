# -*- coding: utf-8 -*-

from nva.kurzfassung import _
from nva.kurzfassung.views.erweiterte_kurzfassung import ErweiterteKurzfassung
from Products.Five.browser import BrowserView


class AkkordeonAnsicht(ErweiterteKurzfassung):
    """Content-Liste wird von der erweiterten Kurzfassung geerbt und adaptiert"""

    def formatCollapsed(self, contentlist):
        html = ''
        if contentlist:
            html = u'<dl>'
            for i in contentlist:
                html += u'<dt><a href="%s" title="%s">%s</a></dt>' %(i.getURL(), i.Title, i.Title)
                html += u'<dd>%s</dd>' %(i.Description)
            html += u'</dl>'
        return html

    def formatcontent(self):
        """
        Formatiert die Ordnerinhalte fuer die Akkordeon-Ansicht
        """
        contents = []
        index = 0
        for i in self.query():
            entry = {}
            obj = i.getObject()
            entry['title'] = obj.title
            entry['index'] = index
            entry['description'] = obj.description
            if obj.portal_type == 'LDAPPerson':
                entry['description'] = self.formatPerson(obj)
            if obj.portal_type in ["Schutzhandschuh", "Hautreinigungsmittel", "Hautschutzmittel", "Hautpflegemittel", "Desinfektionsmittel"]:
                if obj.hersteller:
                    entry['description'] = obj.hersteller.to_object.title
            entry['text'] = ''
            if entry['description']:
                entry['text'] = u'<p class="documentDescription">%s</p>' % entry['description']
            if 'text' in obj.__dict__:
                if obj.text:
                    try:
                        entry['text'] += obj.text.output
                    except:
                        entry['text'] += obj.text
            if obj.portal_type in ["Folder", "Collection"]:
                 entry['text'] += self.formatCollapsed(self.query(obj))
            if 'schlusstext' in obj.__dict__:
                if obj.schlusstext:
                    entry['text'] += obj.schlusstext.output
            entry['datum'] = i.created.strftime('%d.%m.%Y')
            entry['url'] = obj.absolute_url()
            if obj.portal_type == 'Link':
                entry['url'] = self.formatLink(obj)
            entry['excludeFromDisplay'] = self.excludeFromDisplay(obj)
            entry['cards'] = self.getContextCards(obj)
            if not self.excludeFromDisplay(obj):
                contents.append(entry)
                index += 1
        return contents

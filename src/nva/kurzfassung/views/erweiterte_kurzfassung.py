# -*- coding: utf-8 -*-
import re
from zope.interface import Interface
from nva.kurzfassung import _
from Products.Five.browser import BrowserView
from plone import api
from plone.app.contenttypes.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish
from nva.kurzfassung.config import getDefault


try:
    from nva.folderbehaviors.schmuckbilder import selectSchmuckbilder
    SCHMUCKBILDER = True
except:
    SCHMUCKBILDER = False


def formatphone(number):
    """ formatiert eine Telefonnummer nach DIN """

    if not number:
        return u'-'
    if not number.startswith('+49'):
        return number
    if len(number) < 8:
        return number
    country = number[:3]
    durchwahl = number[-4:]
    rest = number[3:-4]
    return '%s(0)%s-%s' %(country, rest, durchwahl)


class ErweiterteKurzfassung(BrowserView):
    """Erweiterte Kurzfassung"""


    def query(self, obj=None):
        """
        Listing der Ordnerinhalte oder Ergebnisse der Kollektion
        """
        if obj:
            query_context = obj
        else:
            query_context = self.context
        if ICollection.providedBy(query_context):
            return query_context.queryCatalog(batch=False)
        elif IFolderish.providedBy(query_context):
            return query_context.getFolderContents(batch=False)


    def createVideoentry(self, obj):
        """
        Formatiert ein Video in der Darstellungsform
        """
        videoentry = {}
        videoentry['src'] = obj.src
        videoentry['videotype'] = 'video/mp4'
        if obj.src:
            if 'youtube' in obj.src:
                videoentry['vidoetype'] = 'video/youtube'
        videoentry['embed'] = ''
        if not obj.src:
            videoentry['embed'] = obj.embed
        videoentry['videoformat'] = "embed-responsive embed-responsive-16by9"
        return videoentry


    def leermeldung(self):
        """
        Liefert eine selbst konfigurierte Leermeldung zurueck
        """
        emptymessage = ''
        if hasattr(self.context, 'leermeldung'):
            emptymessage = self.context.leermeldung
        return emptymessage


    def formatLink(self, link):
        """
        Gibt bei Objekttyp Link die Remote-URL zurueck
        """
        remoteurl = link.remoteUrl
        if 'resolveuid' in remoteurl:
            objuid = remoteurl.split('/')
            try:
                remoteurl = api.content.get(UID=objuid).absolute_url()
            except:
                remoteurl = link.absolute_url()
        return remoteurl


    def formatPerson(self, person):
        """
        Formatiert die Beschreibung fuer eine Person
        """
        description = ''
        if not person.username:
            description = 'Telefon:%s E-Mail:%s' %(person.telefon, person.email)
        else:
            user = api.user.get(username = person.username)
            description = 'Kontakt: %s (%s)' %(formatphone(user.getProperty('telefon')),
                                                           user.getProperty('email'))
        return description


    def excludeFromDisplay(self, obj):
        """
        Gibt zurueck ob das Objekt im Listing angezeigt werden soll oder nicht
        """
        excludeFromDisplay = False
        if hasattr(obj, 'excludeFromDisplay'):
            excludeFromDisplay = obj.excludeFromDisplay
        return excludeFromDisplay


    def getSchmuckbild(self, obj):
        """
        Gibt ein Schmuckbild zurueck, wenn vorhanden
        """
        try:
            contentid = selectSchmuckbilder(self.context).getTerm(obj.schmuckbild).token
            brain = api.content.find(portal_type='Image', UID=contentid)[0]
            imgobj = brain.getObject()
            imgurl = '%s/@@images/image' %imgobj.absolute_url()
            imgtitle = brain.Description
            image = (imgurl, imgtitle)
        except:
            image = ()
        return image


    def formatPreviewImage(self, obj):
        """
        Formatiert ein Vorschaubild fuer die Ordneransichten
        """
        img = {}
        img['title'] = obj.title
        img['description'] = obj.description
        img['url'] = ''
        img['reference'] = '#'
        img['reftitle'] = ''
        if hasattr(obj, 'relatedItems'):
            if obj.relatedItems:
                img['reference'] = obj.relatedItems[0].to_object.absolute_url()
                img['reftitle'] = obj.relatedItems[0].to_object.title
        if 'newsurl' in obj.__dict__:
            if obj.newsurl:
                img['reference'] = obj.newsurl.to_object.absolute_url()
                img['reftitle'] = obj.newsurl.to_object.title
        if 'extnews' in obj.__dict__:
            if obj.extnews:
                img['reference'] = obj.extnews
                img['reftitle'] = obj.extnewstitle
        if hasattr(obj, 'alttitle'):
            if obj.alttitle:
                img['title'] = obj.alttitle
        if hasattr(obj, 'image'):
            if obj.image:
                img['url'] = '%s/@@images/image' %obj.absolute_url()
                return img
        if hasattr(obj, 'bild'):
            if obj.bild:
                img['url'] = '%s/@@images/bild' %obj.absolute_url()
                return img
        if hasattr(obj, 'portraet'):
            if obj.portraet:
                img['url'] = '%s/@@images/portraet' %obj.absolute_url()
                return img
        if hasattr(obj, 'schmuckbild'):
            if obj.schmuckbild:
                schmuck = self.getSchmuckbild(obj)
                if schmuck:
                    img['url'] = image[0]
                    img['description'] = image[1]
                    return img
        if hasattr(obj, 'poster'):
            if obj.poster:
                img['url'] = '%s/@@images/poster' %obj.absolute_url()
                return img
        if hasattr(obj, 'newsimage'):
            if obj.newsimage:
                if obj.newsimage.to_object:
                    img['url'] = '%s/@@images/image' % obj.newsimage.to_object.absolute_url()
                    img['title'] = obj.newsimage.to_object.title
                    img['description'] = obj.newsimage.to_object.description
                    return img
        if hasattr(obj, 'titleimage'):
            if obj.titleimage:
                img['url'] = '%s/@@images/titleimage' % obj.absolute_url()
                return img
        if hasattr(obj, 'titleimages'):
            if obj.titleimages:
                if obj.titleimages[0].to_object:
                    img['url'] = '%s/@@images/image' % obj.titleimages[0].to_object.absolute_url()
                    img['title'] = obj.titleimages[0].to_object.title
                    img['description'] = obj.titleimages[0].to_object.description
                    return img
        if not img['url'] and obj.portal_type == "News Item":
            img = getDefault()
            return img
        return {}


    def formatVideo(self, obj):
        """
        Formatiert ein Vorschauvideo
        """
        video = ''
        if obj.portal_type in ['Videoembed']:
            video = self.createVideoentry(obj)
        
        return video

    def formatCollection(self, contextobj):
        weiter = False
        objlist = self.query(contextobj)
        if len(objlist) > 5:
            objlist = objlist[:5]
            weiter = True
        html = u'<dl>'
        for i in objlist:
            obj = i.getObject()
            definition = ''
            html += u'<dt><a href="%s" title="%s">%s</a></dt>' % (obj.absolute_url(), obj.title, obj.title)
            if obj.portal_type == "Event":
                if obj.start:
                    definition = '<i class="far fa-calendar-alt"></i> %s' % obj.start.strftime('%d.%m.%Y ')
                if obj.location:
                    definition += '<i class="fas fa-map-marker-alt"></i> %s' % obj.location
            elif obj.portal_type == "News Item":
                definition = "%s %s" (obj.modified.strftime("%d.%m.%Y"), obj.description)
            else:
                definition = obj.description
            html += '<dd>%s</dd>' % definition
            html += '</dl>'
        if weiter:
            html += '<a href="%s" title="%s">weiter</a>' % (contextobj.absolute_url(), contextobj.title)
        return html    

    def getContextCards(self, obj, cardtype='cards'):
        """
        Formatiert die Contextinformationen
        """
        cardlist = []
        if hasattr(obj, cardtype):
            for i in getattr(obj, cardtype, []):
                entry = {}
                contextobj = i.to_object
                entry['type'] = contextobj.portal_type
                entry['title'] = contextobj.title
                entry['text'] = ''
                if contextobj.portal_type in ['Document', 'News Item']:
                    if contextobj.text:
                        entry['text'] = contextobj.text.output
                elif contextobj.portal_type in ['Collection']:
                    entry['text'] = self.formatCollection(contextobj)
                entry['cardclass'] = 'card border-primary mb-3'    
                if hasattr(contextobj, 'cardcolor'):
                    entry['cardclass'] = contextobj.cardcolor
                previewimage = self.formatPreviewImage(contextobj)        
                entry['imageurl'] = previewimage.get('url')
                entry['imagetitle'] = previewimage.get('title')
                entry['imagedesc'] = previewimage.get('description')
                entry['reference'] = previewimage.get('reference')
                entry['reftitle'] = previewimage.get('reftitle')
                cardlist.append(entry)
        return cardlist
                

    def formatcontent(self):
        """
        Formatiert die Ordnerinhalte
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
            if hasattr(obj, 'text'):
                if obj.text:
                    try:
                        entry['text'] = obj.text.output
                    except:
                        entry['text'] = obj.text
            entry['datum'] = i.created.strftime('%d.%m.%Y')
            entry['url'] = obj.absolute_url()
            if obj.portal_type == 'Image':
                entry['url'] = obj.absolute_url() + '/image_view_fullscreen'
            if obj.portal_type == 'Link':
                entry['url'] = self.formatLink(obj)
            entry['excludeFromDisplay'] = self.excludeFromDisplay(obj)
            entry['image'] = ''
            entry['smallimg'] = ''
            entry['topimage'] = ''
            img = self.formatPreviewImage(obj)
            if img:
                imgtag = '<img src="%s" class="%s" title="%s" alt="%s">'
                large = img['url'] + '/large'
                imgclass = 'img-fluid'
                entry['image'] = imgtag % (large, imgclass, img['title'], img['description'])
                small = img['url'] + '/mini'
                imgclass = 'align-self-center mr-3'
                entry['smallimg'] = imgtag % (small, imgclass, img['title'], img['description'])
                top = img['url']
                imgclass = 'img-fluid img-top'
                entry['topimage'] = imgtag % (top, imgclass, img['title'], img['description'])
            entry['video'] = self.formatVideo(obj)
            entry['cards'] = self.getContextCards(obj)
            entry['content-cards'] = self.getContextCards(obj, 'contentcards')
            if not self.excludeFromDisplay(obj):
                contents.append(entry)
                index +=1
        return contents


    def getBatchValue(self):
        default = 10000
        if hasattr(self.context, 'batchvalue'):
            if self.context.batchvalue == 0:
                return default
            else:
                return self.context.batchvalue
        return default


    def contentlist(self):
        self.mytitle = self.context.Title()
        self.mydesc = self.context.Description()
        self.myhtml = ''
        self.endhtml = ''
        if hasattr(self.context, 'text'):
            if self.context.text:
                self.myhtml = self.context.text.output
        if hasattr(self.context, 'schlusstext'):
            if self.context.schlusstext:
                self.endhtml = self.context.schlusstext.output
        self.emptymessage = self.leermeldung()
        self.mastercards = self.getContextCards(self.context)
        self.batchvalue = self.getBatchValue()
        return self.formatcontent()

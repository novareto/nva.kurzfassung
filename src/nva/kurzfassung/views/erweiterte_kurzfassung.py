# -*- coding: utf-8 -*-
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


    @property
    def query(self):
        """
        Listing der Ordnerinhalte oder Ergebnisse der Kollektion
        """
        if ICollection.providedBy(self.context):
            return self.context.queryCatalog(batch=False)
        elif IFolderish.providedBy(self.context):
            return self.context.getFolderContents(batch=False)


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


    def getSchmuckbild(self, imagetag, obj):
        """
        Gibt ein Schmuckbild zurueck, wenn vorhanden
        """
        try:
            contentid = selectSchmuckbilder(self.context).getTerm(obj.schmuckbild).token
            brain = api.content.find(portal_type='Image', UID=contentid)[0]
            imgobj = brain.getObject()
            imgurl = '%s/@@images/image/large' %imgobj.absolute_url()
            imgtitle = brain.Description
            image = imagetag %(imgurl, imgtitle)
        except:
            image = ''
        return image


    def formatPreviewImage(self, obj):
        """
        Formatiert ein Vorschaubild fuer die Ordneransichten
        """
        image = ''
        imagetag = '<img src="%s" title="%s" class="img-fluid">'
        imgtitle = obj.title
        if hasattr(obj, 'alttitle'):
            if obj.alttitle:
                imgtitle = obj.alttitle
        if hasattr(obj, 'image'):
            if obj.image:
                imgurl = '%s/@@images/image/large' %obj.absolute_url()
                image = imagetag %(imgurl, imgtitle)
                return image
        if hasattr(obj, 'bild'):
            if obj.bild:
                imgurl = '%s/@@images/bild/large' %obj.absolute_url()
                image = imagetag %(imgurl, imgtitle)
                return image
        if hasattr(obj, 'portraet'):
            if obj.portraet:
                imgurl = '%s/@@images/portraet/large' %obj.absolute_url()
                image = imagetag %(imgurl, imgtitle)
                return image
        if hasattr(obj, 'schmuckbild'):
            if obj.schmuckbild:
                image = self.getSchmuckbild(imagetag, obj)
                return image 
        if hasattr(obj, 'poster'):
            if obj.poster:
                imgurl = '%s/@@images/poster/large' %obj.absolute_url()
                image = imagetag %(imgurl,imgtitle)
                return image
        if hasattr(obj, 'newsimage'):
            if obj.newsimage:
                if obj.newsimage.to_object:
                    imgurl = '%s/@@images/image/large' % obj.newsimage.to_object.absolute_url()
                    imgtitle = obj.newsimage.to_object.title
                    image = imagetag %(imgurl, obj.newsimage.to_object.title)
                    return image
        if hasattr(obj, 'titleimage'):
            if obj.titleimage:
                imgurl = '%s/@@images/titleimage/mini' % obj.absolute_url()
                image = imagetag %(imgurl, imgtitle)
                return image
        if hasattr(obj, 'titleimages'):
            if obj.titleimages:
                if obj.titleimages[0].to_object:
                    imgurl = '%s/@@images/image/large' % obj.titleimages[0].to_object.absolute_url()
                    imgtitle = obj.titleimages[0].to_object.description
                    image = imagetag %(imgurl, imgtitle)
                    return image
        if not image and obj.portal_type == "News Item":
            image = getDefault()
        return image


    def formatVideo(self, obj):
        """
        Formatiert ein Vorschauvideo
        """
        video = ''
        if obj.portal_type in ['Videoembed']:
            video = self.createVideoentry(obj)
        
        return video


    def getContextCards(self, obj):
        """
        Formatiert die Contextinformationen
        """
        cardlist = []
        if hasattr(obj, 'cards'):
            for i in obj.cards:
                entry = {}
                contextobj = i.to_object
                entry['type'] = contextobj.portal_type
                entry['title'] = contextobj.title
                entry['text'] = ''
                if contextobj.portal_type in ['Document', 'News Item']:
                    if contextobj.text:
                        entry['text'] = contextobj.text.output
                entry['imageurl'] = ''
                if contextobj.portal_type in ['Image']:
                    if contextobj.image:
                        entry['imageurl'] = '%s/@@images/image/preview' % contextobj.absolute_url()
                cardlist.append(entry)
        return cardlist 
                

    def formatcontent(self):
        """
        Formatiert die Ordnerinhalte
        """
        contents = []
        for i in self.query:
            entry = {}
            obj = i.getObject()
            entry['title'] = obj.title
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
            if obj.portal_type == 'Link':
                entry['url'] = self.formatLink(obj)
            entry['excludeFromDisplay'] = self.excludeFromDisplay(obj)
            entry['image'] = self.formatPreviewImage(obj)
            entry['video'] = self.formatVideo(obj)
            if not self.excludeFromDisplay(obj):
                contents.append(entry)
            entry['cards'] = self.getContextCards(obj)
        return contents


    def contentlist(self):
        self.mytitle = self.context.Title()
        self.mydesc = self.context.Description()
        self.myhtml = ''
        if hasattr(self.context, 'text'):
            if self.context.text:
                self.myhtml = self.context.text.output
        self.emptymessage = self.leermeldung()
        return self.formatcontent()

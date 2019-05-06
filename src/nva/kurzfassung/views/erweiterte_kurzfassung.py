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
            imgurl = brain.getURL()
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
        imagetag = '<img src="%s" title="%s" class="img-responsive">'
        imgtitle = obj.title
        if hasattr(obj, 'alttitle'):
            if obj.alttitle:
                imgtitle = obj.alttitle
        if hasattr(obj, 'titleimages'):
            if obj.titleimages:
                if obj.titleimages[0].to_object:
                    imgurl = '%s/@@images/image/mini' % obj.titleimages[0].to_object.absolute_url()
                    imgtitle = obj.titleimages[0].to_object.description
                    image = imagetag %(imgurl, imgtitle)
        if hasattr(obj, 'newsimage'):
            if obj.newsimage:
                if obj.newsimage.to_object:
                    imgurl = '%s/@@images/image/mini' % obj.newsimage.to_object.absolute_url()
                    imgtitle = obj.newsimage.to_object.title
                    image = imagetag %(imgurl, obj.newsimage.to_object.title)
        if hasattr(obj, 'poster'):
            if obj.poster:
                imgurl = '%s/@@images/poster/mini' %obj.absolute_url()
                image = imagetag %(imgurl,imgtitle)
        if hasattr(obj, 'schmuckbild'):
            if obj.schmuckbild:
                image = self.getSchmuckbild(imagetag, obj)
        if hasattr(obj, 'portraet'):
            if obj.portraet:
                imgurl = '%s/@@images/portraet/mini' %obj.absolute_url()
                image = imagetag %(imgurl, imgtitle)
        if hasattr(obj, 'image'):
            if obj.image:
                imgurl = '%s/@@images/image/mini' %obj.absolute_url()
                image = imagetag %(imgurl, imgtitle)
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
            entry['datum'] = i.created.strftime('%d.%m.%Y')
            entry['url'] = obj.absolute_url()
            if obj.portal_type == 'Link':
                entry['url'] = self.formatLink(obj)
            entry['excludeFromDisplay'] = self.excludeFromDisplay(obj)
            entry['image'] = self.formatPreviewImage(obj)
            entry['video'] = self.formatVideo(obj)
            if not self.excludeFromDisplay(obj):
                contents.append(entry)
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

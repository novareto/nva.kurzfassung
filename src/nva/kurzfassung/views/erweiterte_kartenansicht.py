# -*- coding: utf-8 -*-

from nva.kurzfassung import _
from nva.kurzfassung.views.erweiterte_kurzfassung import ErweiterteKurzfassung
from Products.Five.browser import BrowserView


class ErweiterteKartenansicht(ErweiterteKurzfassung):
    """Content-Liste wird von der erweiterten Kurzfassung geerbt und adaptiert"""


    def formatPreviewImage(self, obj):
        """
        Formatiert ein Vorschaubild fuer die Ordneransichten
        """
        image = ''
        imagetag = '<img src="%s" title="%s" class="img-fluid img-top">'
        imgtitle = obj.title
        if hasattr(obj, 'alttitle'):
            if obj.alttitle:
                imgtitle = obj.alttitle
        if hasattr(obj, 'image'):
            if obj.image:
                imgurl = '%s/@@images/image/preview' %obj.absolute_url()
                image = imagetag %(imgurl, imgtitle)
                return image
        if hasattr(obj, 'bild'):
            if obj.bild:
                imgurl = '%s/@@images/bild/preview' %obj.absolute_url()
                image = imagetag %(imgurl, imgtitle)
                return image
        if hasattr(obj, 'portraet'):
            if obj.portraet:
                imgurl = '%s/@@images/portraet/preview' %obj.absolute_url()
                image = imagetag %(imgurl, imgtitle)
                return image
        if hasattr(obj, 'schmuckbild'):
            if obj.schmuckbild:
                image = self.getSchmuckbild(imagetag, obj)
                return image
        if hasattr(obj, 'poster'):
            if obj.poster:
                imgurl = '%s/@@images/poster/preview' %obj.absolute_url()
                image = imagetag %(imgurl,imgtitle)
                return image
        if hasattr(obj, 'newsimage'):
            if obj.newsimage:
                if obj.newsimage.to_object:
                    imgurl = '%s/@@images/image/preview' % obj.newsimage.to_object.absolute_url()
                    imgtitle = obj.newsimage.to_object.title
                    image = imagetag %(imgurl, obj.newsimage.to_object.title)
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

    def getFolderCards(self):
        """
        Formatiert die Contextinformationen
        """
        cardlist = []
        if hasattr(self.context, 'cards'):
            for i in self.context.cards:
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

    def cardlist(self):
        size = 3
        if hasattr(self.context, 'columns'):
            if self.context.columns:
                size = self.context.columns
        return [self.contentlist()[i:i+size] for i in range(0, len(self.contentlist()), size)]

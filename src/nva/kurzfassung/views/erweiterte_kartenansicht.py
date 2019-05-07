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
        imagetag = '<img src="%s" title="%s" class="card-img-top">'
        imgtitle = obj.title
        if hasattr(obj, 'alttitle'):
            if obj.alttitle:
                imgtitle = obj.alttitle
        if hasattr(obj, 'titleimages'):
            if obj.titleimages:
                if obj.titleimages[0].to_object:
                    imgurl = '%s/@@images/image/large' % obj.titleimages[0].to_object.absolute_url()
                    imgtitle = obj.titleimages[0].to_object.description
                    image = imagetag %(imgurl, imgtitle)
        if hasattr(obj, 'newsimage'):
            if obj.newsimage:
                if obj.newsimage.to_object:
                    imgurl = '%s/@@images/image/large' % obj.newsimage.to_object.absolute_url()
                    imgtitle = obj.newsimage.to_object.title
                    image = imagetag %(imgurl, obj.newsimage.to_object.title)
        if hasattr(obj, 'poster'):
            if obj.poster:
                imgurl = '%s/@@images/poster/large' %obj.absolute_url()
                image = imagetag %(imgurl,imgtitle)
        if hasattr(obj, 'schmuckbild'):
            if obj.schmuckbild:
                image = self.getSchmuckbild(imagetag, obj)
        if hasattr(obj, 'portraet'):
            if obj.portraet:
                imgurl = '%s/@@images/portraet/large' %obj.absolute_url()
                image = imagetag %(imgurl, imgtitle)
        if hasattr(obj, 'image'):
            if obj.image:
                imgurl = '%s/@@images/image/large' %obj.absolute_url()
                image = imagetag %(imgurl, imgtitle)
        if not image and obj.portal_type == "News Item":
            image = getDefault()

        return image


    def cardlist(self):
        return [self.contentlist()[i:i+3] for i in range(0, len(self.contentlist()), 3)]

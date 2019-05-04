import random
from plone import api
from nva.folderbehaviors.interfaces import ISchmuckbilder
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

def getDefault():
    images = []
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISchmuckbilder)
    path =  settings.schmuckbilder
    brains = api.content.find(portal_type="Folder", path=path)
    if brains:
        folder = brains[0].getObject()
        if folder.relatedItems:
            obj = folder.relatedItems[0].to_object
            if obj.portal_type == 'Folder':
                defaults = obj.getFolderContents()
                for i in defaults:
                    if i.portal_type == 'Image':
                        imgtag = '<img src="%s/@@images/image/mini" title="%s" class="media-object img-responsive">' %(i.getURL(), i.Title)
                        images.append(imgtag)
    to = len(images)
    if to == 1:
        return images[0]
    if to > 1:
        imageindex = random.randint(0, to-1)
        return images[imageindex]
    return ''

# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'nva.kurzfassung:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.

    typesTool = getToolByName(context, 'portal_types')

    typefolder = typesTool['Folder']
    viewlist = typefolder.getProperty('view_methods', d=None)
    if 'enhanced_foldersummary' not in viewlist:
        viewlist = viewlist + ('enhanced_foldersummary',)
    if 'enhanced_folderlist' not in viewlist:
        viewlist = viewlist + ('enhanced_folderlist',)
    if 'enhanced_foldertext' not in viewlist:
        viewlist = viewlist + ('enhanced_foldertext',)
    if 'enhanced_cardview' not in viewlist:
        viewlist = viewlist + ('enhanced_cardview',)
    if 'akkordeon_view' not in viewlist:
        viewlist = viewlist + ('akkordeon_view',)        
    if 'download_view' not in viewlist:
        viewlist = viewlist + ('download_view',)        
    if 'download_image_view' not in viewlist:
        viewlist = viewlist + ('download_image_view',)        
    typefolder.manage_changeProperties(view_methods = viewlist)

    typecollection = typesTool['Collection']
    viewlist = typecollection.getProperty('view_methods', d=None)
    if 'enhanced_foldersummary' not in viewlist:
        viewlist = viewlist + ('enhanced_foldersummary',)
    if 'enhanced_folderlist' not in viewlist:
        viewlist = viewlist + ('enhanced_folderlist',)
    if 'enhanced_foldertext' not in viewlist:
        viewlist = viewlist + ('enhanced_foldertext',)
    if 'enhanced_cardview' not in viewlist:
        viewlist = viewlist + ('enhanced_cardview',)
    if 'akkordeon_view' not in viewlist:
        viewlist = viewlist + ('akkordeon_view',)
    if 'download_view' not in viewlist:
        viewlist = viewlist + ('download_view',) 
    if 'download_image_view' not in viewlist:
        viewlist = viewlist + ('download_image_view',)
    typecollection.manage_changeProperties(view_methods = viewlist)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.

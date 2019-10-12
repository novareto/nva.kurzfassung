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
    if 'enhanced_cardview' not in viewlist:
        viewlist = viewlist + ('enhanced_cardview',)
    if 'enhanced_cardcolumns' not in viewlist:
        viewlist = viewlist + ('enhanced_cardcolumns',)
    if 'nachricht_view' not in viewlist:
        viewlist = viewlist + ('nachricht_view',)
    if 'small_nachricht_view' not in viewlist:
        viewlist = viewlist + ('small_nachricht_view',)
    if 'nachricht_liste_view' not in viewlist:
        viewlist = viewlist + ('nachricht_liste_view',)
    if 'enhanced_contentdir' not in viewlist:
        viewlist = viewlist + ('enhanced_contentdir',)
    if 'enhanced_tableview' not in viewlist:
        viewlist = viewlist + ('enhanced_tableview',)
    if 'zwei_spalten_view' not in viewlist:
        viewlist = viewlist + ('zwei_spalten_view',)
    if 'zwei_spalten_context_view' not in viewlist:
        viewlist = viewlist + ('zwei_spalten_context_view',)
    typefolder.manage_changeProperties(view_methods = viewlist)

    typecollection = typesTool['Collection']
    viewlist = typecollection.getProperty('view_methods', d=None)
    if 'enhanced_foldersummary' not in viewlist:
        viewlist = viewlist + ('enhanced_foldersummary',)
    if 'enhanced_folderlist' not in viewlist:
        viewlist = viewlist + ('enhanced_folderlist',)
    if 'enhanced_cardview' not in viewlist:
        viewlist = viewlist + ('enhanced_cardview',)
    if 'enhanced_cardcolumns' not in viewlist:
        viewlist = viewlist + ('enhanced_cardcolumns',)
    if 'enhanced_contentdir' not in viewlist:
        viewlist = viewlist + ('enhanced_contentdir',)
    if 'enhanced_tableview' not in viewlist:
        viewlist = viewlist + ('enhanced_tableview',)
    if 'zwei_spalten_view' not in viewlist:
        viewlist = viewlist + ('zwei_spalten_view',)
    if 'zwei_spalten_context_view' not in viewlist:
        viewlist = viewlist + ('zwei_spalten_context_view',)
    typecollection.manage_changeProperties(view_methods = viewlist)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.

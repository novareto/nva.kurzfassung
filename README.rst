===============
nva.kurzfassung
===============

Die nva.kurzfassung stellt eine Sammlung von Ordneransichten für das CMS-Plone zur Verfügung. Das Package setzt nva.folderbehaviors, plonetheme.tokyo 
und plonetheme.siguv voraus. 

Das Package ging aus einer kundenspezfischen Anpassung der Standard-Plone Kurzfassung hervor. Diese Version wurde fortan Erweiterte Kurzfassung
genannt. Später kamen immer weitere Anpassungen und spezifische Ordneransichten hinzu. Alle Darstellungsformen können sowohl auf Ordner als auch auf
Kollektionen angewendet werden.

Features
--------

- In der Viewklasse ./views/erweiterte_kurzfassung.ErweiterteKurzfassung wird aus den Inhalten des Ordners eine Liste mit Dictionaries zusammengestellt.

- Dieses Dicts werden anstatt der Objekte oder Brains an die View-Templates übergeben.

- Die Dictionaries berücksichtigen sowohl eigene Inhaltstypen der SIGUV-Kooperation als auch Erweiterungen, die über nva.folderbehaviors bereitgestellt werden.  

- Alle anderen Viewklassen erben von "ErweiterteKurzfassung". Eventuell werden spezifische Methoden überschrieben oder notwendige Methoden für die Darstellung ergänzt.


Examples
--------

- https://newbgetem.bg-kooperation.de

Documentation
-------------

Die Konfiguration der Views (Zusammenspiel zwischen Viewklasse und Template) kann ./views/configure.zcml entnommen werden::

  <browser:page
     name="enhanced_folderlist"
     for="*"
     class=".erweiterte_ordnerliste.ErweiterteOrdnerliste"
     template="templates/enhanced_folderlist.pt"
     permission="zope2.View"
     />

  <browser:page
     name="enhanced_foldersummary"
     for="*"
     class=".erweiterte_kurzfassung.ErweiterteKurzfassung"
     template="templates/enhanced_foldersummary.pt"
     permission="zope2.View"
     />

Die Methoden der Klasse ErweiterteKurzfassung werden in den Docstrings im Modul ./views/erweiterte_kurzfassung.ErweiterteKurzfassung dokumentiert.


Translations
------------

Das Package steht nur in Deutsch zur Verfügung.

Installation
------------

Install nva.kurzfassung by adding it to your buildout::

    [buildout]

    ...

    eggs =
        nva.kurzfassung


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/novareto/nva.kurzfassung/issues
- Source Code: https://github.com/novareto/nva.kurzfassung


Support
-------

lwalther@novareto.de

License
-------

The project is licensed under the GPLv2.

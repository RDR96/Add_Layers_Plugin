# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AddLayers
                                 A QGIS plugin
 This plugin will add layers with only one button
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2019 by TheSigProject
        email                : rdrcorvera@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5 import QtGui, QtCore, QtWidgets
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import *
from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer
import win32api
import os






# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .add_layers_dialog import AddLayersDialog
import os.path



class AddLayers:
    """QGIS Plugin Implementation."""
    x = 0
    y = 0
    layers_list = []
    extension_list = []

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'AddLayers_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Add Layers')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('AddLayers', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/add_layers/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Add Layers'),
            callback=self.run,
            parent=self.iface.mainWindow())
        
               

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Add Layers'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):

        """Run method that performs all the real work"""
        

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = AddLayersDialog()

        # show the dialog
        self.dlg.show()
        self.dlg.gridLayout_2.setRowStretch(0, 3)
        self.dlg.gridLayout_2.setRowStretch(1, 1)
                    
        self.dlg.pushButton.clicked.connect(self.test_print)

        # Run the dialog event loop
        result = self.dlg.exec_()            
        # See if OK was pressed
        if result:
            for index, layer in enumerate(self.layers_list):  
                if self.extension_list[index] == '.tif':   
                    newLayer = QgsRasterLayer(layer, 'test')                
                    win32api.MessageBox(0, str(layer), 'title', 0x00001000)                
                    QgsProject.instance().addMapLayer(newLayer)
                else:
                    newLayer = QgsVectorLayer(layer, 'test', 'ogr')                
                    win32api.MessageBox(0, str(layer), 'title', 0x00001000)                
                    QgsProject.instance().addMapLayer(newLayer)
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            

    
    def test_print(self):      
        label = QtWidgets.QLabel()        
        file, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Select file", "", "Raster layers(*.tif);;Vector layers(*.shp)")        

        """label.setText(file)"""        
            
        url = QtCore.QUrl.fromLocalFile(file)
        from pathlib import Path    

        filename = Path(file).name
        label.setText(filename)
        label.setAlignment(QtCore.Qt.AlignCenter)
        if file not in self.layers_list:
            self.dlg.gridLayout_2.addWidget(label, self.x, self.y) 
            fileAux, file_extension = os.path.splitext(file)
            self.extension_list.append(file_extension)
            self.layers_list.append(file)
            self.y += 1
            if self.y == 2:
                self.x += 1
                self.y = 0
        else:
            win32api.MessageBox(0, 'Ya se encuentra seleccionado', 'title', 0x00001000)
        
        """win32api.MessageBox(0, filename, 'title', 0x00001000)"""        
        
        
            
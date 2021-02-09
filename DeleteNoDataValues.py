# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   Delete NoData Values in XYZ-Files                       *
*   Nicole Kamp                                                           *
*   nicole.kamp@stmk.gv.at / niki.kamp@gmail.com                                                   *
*   February 2021                                                         *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtCore import QFileInfo
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFolderDestination, 
                       QgsProcessingMultiStepFeedback)
from qgis import processing

import osgeo.gdal as gdal
import numpy as np

from osgeo import ogr, osr
import string, os, sys, copy, shutil, math, numpy, time, datetime, glob
from time import *
from sys import *

class DeleteNoDataAlgorithm(QgsProcessingAlgorithm):
    """
Python Script zur Entfernung von NoData-Werten aus XYZ-Files
Eingabe der Input- und Output-Parameter
    """
    INPUT_Pfad = 'INPUT_Folder'
    OUTPUT_Pfad = 'OUTPUT_Folder'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DeleteNoDataAlgorithm()

    def name(self):
        return 'deletenodata'

    def displayName(self):
        return self.tr('Delete_NoDataValues_XYZ')

    def group(self):
        return self.tr('GISStmk-Tools')

    def groupId(self):
        return 'scripts'

    def shortHelpString(self):
        return self.tr("Tool zur Entfernung von NoData-Werten aus XYZ-Files (Kamp, 2021).")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.INPUT_Pfad, 
                self.tr('INPUT_Folder')
            )
        )
                     
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_Pfad, 
                self.tr('OUTPUT_Folder')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        feedback = QgsProcessingMultiStepFeedback(1, feedback)
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        
        results = {}
        outputs = {}
        
        count = 0

        for raster in glob.glob(str(parameters[self.INPUT_Pfad])+'/*.xyz'):
            fileInfo = QFileInfo(raster)
            baseName = fileInfo.baseName()
            xyz_old = str(parameters[self.INPUT_Pfad])+'/'+baseName+'.xyz'
            xyz = str(parameters[self.OUTPUT_Pfad])+'/'+baseName+'_nodata.xyz'
            
            xyz_read = open(xyz_old, "r")
            xyz_write = open(xyz, "w")
            
            count = count+1
            
            for i in xyz_read:
                index=i.find(str(-3.40282e+38))
                if index == -1:
                    xyz_write.write(i)
                
            outputs['AdaptedXYZFiles'] = count
            results['Löschen von NoData-Werten abgeschlossen!'] = outputs
            
        return results           

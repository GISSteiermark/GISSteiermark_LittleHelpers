# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   Create TFWs for GeoTIFFs                                              *
*   Version: 1.1.                                                         *
*   QGIS-Version: 3.22.6-Białowieża                                       *
*   Nicole Kamp                                                           *
*   nicole.kamp@stmk.gv.at / niki.kamp@gmail.com                          *
*   September 2022                                                        *
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
                       QgsProcessingParameterFile,  
                       QgsProcessingMultiStepFeedback)
from qgis import processing

import osgeo.gdal as gdal
import numpy as np

from osgeo import ogr, osr
import string, os, sys, copy, shutil, math, numpy, time, datetime, glob
from time import *
from sys import *

class GeoTIFF2XYZAlgorithm(QgsProcessingAlgorithm):
    """
Python Script zur Erstellung von TFWs für GeoTIFFs
Eingabe der Input- und Output-Parameter
    """
    INPUT_Pfad = 'INPUT_Folder'
    OUTPUT_Pfad = 'OUTPUT_Folder'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return GeoTIFF2XYZAlgorithm()

    def name(self):
        return 'geotiff_tfw'

    def displayName(self):
        return self.tr('GeoTIFF2TFW')

    def group(self):
        return self.tr('GISStmk-ALSTools')

    def groupId(self):
        return 'gisstmk_alsscripts'

    def shortHelpString(self):
        return self.tr("Tool zur Erstellung von TFWs für GeoTIFFs"+"\n"+"QGIS-Version: 3.22.6-Białowieża"+"\n"+"Version 1.1"+"\n"+"(Kamp, 2022)")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_Pfad, 
                self.tr('INPUT_Folder'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFile(
                self.OUTPUT_Pfad, 
                self.tr('OUTPUT_Folder'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        feedback = QgsProcessingMultiStepFeedback(1, feedback)
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        
        results = {}
        outputs = {}

        for raster in glob.glob(str(parameters[self.INPUT_Pfad])+'/*.tif'):
            fileInfo = QFileInfo(raster)
            baseName = fileInfo.baseName()
            tiff = str(parameters[self.INPUT_Pfad])+'/'+baseName+'.tif'
            tiff_tfw = str(parameters[self.OUTPUT_Pfad])+'/'+baseName+'.tif'
            
            alg_params = {
                'COPY_SUBDATASETS': False,
                'DATA_TYPE': 0,
                'EXTRA': '',
                'INPUT': str(tiff),
                'NODATA': None,
                'OPTIONS' : 'tfw=yes',
                'TARGET_CRS': None,
                'OUTPUT': str(tiff_tfw)
            }
            outputs['tiff_tfw'] = processing.run('gdal:translate', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['Berechnung der TFWs abgeschlossen!'] = outputs['tiff_tfw']['OUTPUT']
        return results           

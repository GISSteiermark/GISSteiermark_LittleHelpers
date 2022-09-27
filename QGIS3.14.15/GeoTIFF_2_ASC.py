# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   Convert GeoTIFFs from a folder into ASC-Files                         *
*   Nicole Kamp                                                           *
*   niki.kamp@gmail.com                                                   *
*   February 2021                                                          *
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

class GeoTIFF2ASCAlgorithm(QgsProcessingAlgorithm):
    """
Python Script zur Umrechnung von GeoTIFF- in XYZ-Files
Eingabe der Input- und Output-Parameter
    """
    INPUT_Pfad = 'INPUT_Folder'
    OUTPUT_Pfad = 'OUTPUT_Folder'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return GeoTIFF2ASCAlgorithm()

    def name(self):
        return 'geotiff2asc'

    def displayName(self):
        return self.tr('GeoTIFF2ASC')

    def group(self):
        return self.tr('GISStmk-Tools')

    def groupId(self):
        return 'scripts'

    def shortHelpString(self):
        return self.tr("Tool zur Umrechnung von GeoTIFF- in ASC-Files (Kamp, 2020).")

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

        for raster in glob.glob(str(parameters[self.INPUT_Pfad])+'/*.tif'):
            fileInfo = QFileInfo(raster)
            baseName = fileInfo.baseName()
            tiff = str(parameters[self.INPUT_Pfad])+'/'+baseName+'.tif'
            asc = str(parameters[self.OUTPUT_Pfad])+'/'+baseName+'.asc'
        
            alg_params = {
                'COPY_SUBDATASETS': False,
                'DATA_TYPE': 6,
                'EXTRA': '',
                'INPUT': str(tiff),
                'NODATA': None,
                'OPTIONS': '',
                'TARGET_CRS': None,
                'OUTPUT': str(asc)
        }
            outputs['tiff2asc'] = processing.run('gdal:translate', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['Kovertierung nach ASC abgeschlossen!'] = outputs['tiff2asc']['OUTPUT']
        return results           

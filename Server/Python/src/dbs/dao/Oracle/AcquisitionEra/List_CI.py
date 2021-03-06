#!/usr/bin/env python
"""
This module provides Acquisition.Lis-CI data access object.
"""

from WMCore.Database.DBFormatter import DBFormatter
from dbs.utils.dbsExceptionHandler import dbsExceptionHandler

class List_CI(DBFormatter):
    """
    DataTier List DAO class.
    """
    def __init__(self, logger, dbi, owner):
        """
        Add schema owner and sql.
        """
        DBFormatter.__init__(self, logger, dbi)
        self.owner = "%s." % owner if not owner in ("", "__MYSQL__") else ""
        self.logger = logger
        self.sql = \
"""
SELECT AE.ACQUISITION_ERA_NAME, AE.START_DATE, AE.END_DATE, AE.CREATION_DATE, AE.CREATE_BY, AE.DESCRIPTION   
FROM %sACQUISITION_ERAS AE 
""" % (self.owner)

    def execute(self, conn, acquisitionEra="", transaction = False):
	if not conn:
	    dbsExceptionHandler("dbsException-failed-connect2host", "Oracle/AcquisitionEra/List. Expects db connection from upper layer.", self.logger.exception)
        sql = self.sql
	binds={}
	if acquisitionEra:
            op = ("=", "like")["%" in acquisitionEra]
	    sql += "WHERE AE.ACQUISITION_ERA_NAME %s :acquisitionEra" %op 
	    binds = {"acquisitionEra":acquisitionEra}
        self.dbi.processData("alter session set NLS_COMP=LINGUISTIC", None, conn, transaction)
        self.dbi.processData("alter session set NLS_SORT=BINARY_CI", None, conn, transaction)
        result = self.dbi.processData(sql, binds, conn, transaction)
        plist = self.formatDict(result)
        self.dbi.processData("alter session set NLS_COMP=BINARY", None, conn, transaction)
        self.dbi.processData("alter session set NLS_SORT=BINARY", None, conn, transaction)
        return plist

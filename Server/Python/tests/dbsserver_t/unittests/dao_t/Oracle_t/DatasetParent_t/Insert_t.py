"""
DatasetParent.Insert unittests
"""

import os
import unittest

from dbsserver_t.utils.DaoConfig import DaoConfig
from dbsserver_t.utils.DBSDataProvider import create_dbs_data_provider
from dbs.dao.Oracle.DatasetParent.Insert import Insert as DatasetParentInsert
from dbs.dao.Oracle.Dataset.GetID import GetID as DatasetID

class Insert_t(unittest.TestCase):
    @DaoConfig("DBSWriter")
    def __init__(self, methodName='runTest'):
        super(Insert_t, self).__init__(methodName)
        data_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data.pkl')
        self.data_provider = create_dbs_data_provider(data_type='transient', data_location=data_location)
        self.data = self.data_provider.get_dataset_parentage_data(regenerate=True)[0]
         
    def setUp(self):
        """setup all necessary parameters"""
        self.conn = self.dbi.connection()
        self.dataset_insert = DatasetParentInsert(self.logger, self.dbi, self.dbowner)
        self.dataset_id = DatasetID(self.logger, self.dbi, self.dbowner)
                  
    def tearDown(self):
        """Clean-up all necessary parameters"""
        self.conn.close()

    def test01(self):
        """dao.Oracle.DatasetParent.Insert: Basic"""
        tran = self.conn.begin()

        try:
            parentage = {'this_dataset_id' : self.dataset_id.execute(self.conn, self.data["this_dataset"], tran),
                         'dataset' : self.data["parent_dataset"]}

            self.dataset_insert.execute(self.conn, parentage, tran)
        except Exception as ex:
            tran.rollback()
            raise ex
        else:
            tran.commit()
        finally:
            if tran:
                tran.close()

import os
import unittest
import logging
import pandas as pd
import sqlite3

from pipeline import transform_data, save_to_sqlite

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, 'data')
CSV_PATH1 = os.path.join(DATA_DIR, 'green_infrastructure.csv')
CSV_PATH2 = os.path.join(DATA_DIR, 'air_quality_data.csv')
DB_PATH = os.path.join(DATA_DIR, 'combined_data.db')

class TestDataPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.makedirs(DATA_DIR, exist_ok=True)

    def test_create_and_transform_data(self):
       
        data = {
            'Column 1': [1, 2],
            'Column 2': [3, 4],
            'Column 3': [5, 6]
        }
        df = pd.DataFrame(data)
        test_csv_path = os.path.join(DATA_DIR, 'test_transform.csv')
        df.to_csv(test_csv_path, index=False)
        logging.info(f'Manually created data and saved to {test_csv_path}')
        
        
        transformed_df = transform_data(test_csv_path)
        expected_columns = ['column_1', 'column_2', 'column_3']
        self.assertListEqual(list(transformed_df.columns), expected_columns)
   
        expected_data = {
            'column_1': [1, 2],
            'column_2': [3, 4],
            'column_3': [5, 6]
        }
        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(transformed_df, expected_df)
        
      
        os.remove(test_csv_path)

    def test_save_to_sqlite(self):
        df = pd.DataFrame({
            'column_1': [1, 2, 3],
            'column_2': ['a', 'b', 'c']
        })
        save_to_sqlite(df, DB_PATH, 'test_table')
        logging.info(f'Saved data to SQLite database at {DB_PATH} in table test_table')

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_table'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)
        
     
        cursor.execute("SELECT * FROM test_table")
        rows = cursor.fetchall()
        expected_rows = [(1, 'a'), (2, 'b'), (3, 'c')]
        self.assertEqual(rows, expected_rows)
        
        conn.close()

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile(CSV_PATH1):
            os.remove(CSV_PATH1)
        if os.path.isfile(CSV_PATH2):
            os.remove(CSV_PATH2)
        if os.path.isfile(DB_PATH):
            os.remove(DB_PATH)
        if os.path.exists(DATA_DIR):
            os.rmdir(DATA_DIR)

if __name__ == "__main__":
    unittest.main()

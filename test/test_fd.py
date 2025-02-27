import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import re
from src.fd import search_files_by_pattern, search_text_in_files

class TestSearchFilesByPattern(unittest.TestCase):
    
    @patch('os.walk')
    def test_search_files_by_pattern(self, mock_walk):
        mock_walk.return_value = [
            ('/root', ('subdir',), ('file1.txt', 'file2.log', 'file3.txt')),
            ('/root/subdir', (), ('file4.txt',)),
        ]
        pattern = r'\.txt$'
        expected = ['/root/file1.txt', '/root/file3.txt', '/root/subdir/file4.txt']
        result = search_files_by_pattern('/root', pattern)
        self.assertEqual(result, expected)

class TestSearchTextInFiles(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open, read_data='search text is here')
    @patch('os.stat')
    def test_search_text_in_files(self, mock_stat, mock_open):
        files = ['/root/file1.txt']
        search_text = 'search text'
        
        mock_stat.return_value = MagicMock()
        
        expected = [
            {
                'file_name': 'file1.txt',
                'file_path': '/root/file1.txt',
                'file_attributes': mock_stat.return_value
            }
        ]
        result = search_text_in_files(files, search_text)
        self.assertEqual(result, expected)
        
if __name__ == '__main__':
    unittest.main()

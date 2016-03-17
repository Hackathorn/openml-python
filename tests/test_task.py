import os

from openml.util import is_string
from openml.testing import TestBase
from openml import OpenMLSplit
import openml


class TestTask(TestBase):
    def test_get_task_list(self):
        # We can only perform a smoke test here because we test on dynamic
        # data from the internet...
        def check_task(task):
            self.assertEqual(type(task), dict)
            self.assertGreaterEqual(len(task), 2)
            self.assertIn('did', task)
            self.assertIsInstance(task['did'], int)
            self.assertIn('status', task)
            self.assertTrue(is_string(task['status']))
            self.assertIn(task['status'],
                          ['in_preparation', 'active', 'deactivated'])

        tasks = openml.tasks.get_task_list(self.connector, task_type_id=1)
        # 1759 as the number of supervised classification tasks retrieved
        # openml.org from this call; don't trust the number on openml.org as
        # it also counts private datasets
        self.assertGreaterEqual(len(tasks), 1759)
        for task in tasks:
            check_task(task)

        tasks = openml.tasks.get_task_list(self.connector, task_type_id=1)
        self.assertGreaterEqual(len(tasks), 735)
        for task in tasks:
            check_task(task)

    def test_download_task(self):
        task = openml.tasks.download_task(self.connector, 1)
        print(task)
        self.assertTrue(os.path.exists(
            os.path.join(os.getcwd(), "tasks", "1", "task.xml")))
        self.assertTrue(os.path.exists(
            os.path.join(os.getcwd(), "tasks", "1", "datasplits.arff")))
        self.assertTrue(os.path.exists(
            os.path.join(os.getcwd(), "datasets", "1", "dataset.arff")))

    def test_download_split(self):
        task = openml.tasks.download_task(self.connector, 1)
        split = task.download_split()
        self.assertEqual(type(split), OpenMLSplit)
        self.assertTrue(os.path.exists(
            os.path.join(os.getcwd(), "tasks", "1", "datasplits.arff")))

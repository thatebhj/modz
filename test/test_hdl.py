# This file is placed in the Public Domain.
# pylint: disable=C0114,C0115,C0116


"handler"


import unittest


from cmdz.handler import Handler


class TestHandler(unittest.TestCase):

    def test_handler(self):
        hdl = Handler()
        self.assertEqual(type(hdl), Handler)

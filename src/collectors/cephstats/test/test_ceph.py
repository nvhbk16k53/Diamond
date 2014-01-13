#!/usr/bin/env python
import os
import sys

curdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curdir)
sys.path.insert(0, '../')

import unittest
import re


def get_ceph_info(info):
    convert = {'B': 1, 'K': 1000, 'M': 1000000, 'G': 1000000000}
 
    pattern = re.compile(r'\bclient io .*')
    ceph_stats = pattern.search(info).group()
    number = re.compile(r'\d+')
    unit = re.compile(r'\w+')

    rd = number.search(ceph_stats)
    rd_unit = unit.search(ceph_stats, rd.end()).group().upper()[0]
    if rd_unit not in convert:
        rd_unit = 'B'

    wr = number.search(ceph_stats, rd.end())
    wr_unit = unit.search(ceph_stats, wr.end()).group().upper()[0]
    if wr_unit not in convert:
        wr_unit = 'B'

    iops = number.search(ceph_stats, wr.end())
    iops_unit = unit.search(ceph_stats, iops.end()).group().upper()[0]
    if iops_unit not in convert:
        iops_unit = 'B'
 
    return {
            'rd': str(int(rd.group()) * convert[rd_unit]),
            'wr': str(int(wr.group()) * convert[wr_unit]),
            'iops': str(int(iops.group()) * convert[iops_unit])
            }


class TestCeph(unittest.TestCase):
    """
    Test collect ceph data
    """
    def test_sample_data(self):
        """
        Get ceph information from sample data
        """
        f = open('sample.txt')
        self.assertEqual(get_ceph_info(f.read()), {'rd': '8643000', 'wr': '4821000', 'iops': '481'})
        f.close()

if __name__ == '__main__':
    unittest.main()

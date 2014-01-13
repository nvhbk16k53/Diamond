import subprocess
import re
import os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '../ceph')

import ceph


"""
Get ceph status from one node
"""


class CephStatsCollector(ceph.CephCollector):
    def _get_stats(self):
        """
        Get ceph stats
        """
        try:
            output = subprocess.check_output(['ceph', '-s'])
        except subprocess.CalledProcessError, err:
            self.log.info(
                    'Could not get stats: %s' % err)
            self.log.exception('Could not get stats')
            return {}

        convert = {'B': 1, 'K': 1000, 'M': 1000000, 'G': 1000000000}
 
        pattern = re.compile(r'\bclient io .*')
        ceph_stats = pattern.search(output).group()
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

    def collect(self):
        """
        Collect ceph stats
        """
        stats = self._get_stats()
        self._publish_stats('cephstats', stats)

        return

"""
Implementation of the FATES FUNIT test.

This "system" test runs FATES's Fortran unit tests. We're abusing the system test
infrastructure to run these, so that a run of the test suite can result in the unit tests
being run as well.

Grid and compset are irrelevant for this test type.
"""

import os
from CIME.SystemTests.funit import FUNIT
from CIME.XML.standard_module_setup import *

logger = logging.getLogger(__name__)


class FUNITCTSM(FUNIT):
    def __init__(self, case):
        FUNIT.__init__(self, case)

    def get_test_spec_dir(self):
        lnd_root = self._case.get_value("COMP_ROOT_DIR_LND")
        return os.path.join(lnd_root, "src", "fates", "testing")
      
    def run_phase(self):

        rundir = self._case.get_value("RUNDIR")
        exeroot = self._case.get_value("EXEROOT")

        log = os.path.join(rundir, "funit.log")
        if os.path.exists(log):
            os.remove(log)

        test_spec_dir = self.get_test_spec_dir()
        unit_test_tool = os.path.abspath(
            os.path.join(
                test_spec_dir, "run_unit_tests.py"
            )
        )
        args = f"--build-dir {exeroot}"

        stat = run_cmd(
            "{} {} >& funit.log".format(unit_test_tool, args), from_dir=rundir
        )[0]

        append_testlog(open(os.path.join(rundir, "funit.log"), "r").read())

        expect(stat == 0, "RUN FAIL for FUNIT")

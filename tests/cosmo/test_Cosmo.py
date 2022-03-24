import unittest
import os

from icolos.core.workflow_steps.calculation.cosmo import StepCosmo

from icolos.utils.enums.step_enums import StepBaseEnum
from icolos.utils.enums.program_parameters import TurbomoleEnum

from tests.tests_paths import (
    PATHS_EXAMPLEDATA,
    export_unit_test_env_vars,
    get_mol_as_Compound,
    get_mol_as_Conformer,
)
from icolos.utils.enums.compound_enums import ConformerContainerEnum
from icolos.utils.general.files_paths import attach_root_path


_SBE = StepBaseEnum
_TE = TurbomoleEnum()
_CTE = ConformerContainerEnum()


class Test_Cosmo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._test_dir = attach_root_path("tests/junk/Cosmo")
        if not os.path.isdir(cls._test_dir):
            os.makedirs(cls._test_dir)

        export_unit_test_env_vars()

    def setUp(self):
        # initialize a Compound with 1 Enumeration and 2 Conformers (done by OMEGA)
        _paracetamol_molecule = get_mol_as_Compound(PATHS_EXAMPLEDATA.PARACETAMOL_PATH)
        conf = get_mol_as_Conformer(PATHS_EXAMPLEDATA.CLUSTERING_11CONFS)[0]
        with open(PATHS_EXAMPLEDATA.PARACETAMOL_COSMO, "r") as f:
            cosmofile = f.readlines()
        conf.add_extra_data(key=_CTE.EXTRA_DATA_COSMOFILE, data=cosmofile)
        _paracetamol_molecule[0].add_conformer(conf, auto_update=True)
        self._paracetamol_molecule = _paracetamol_molecule

    @classmethod
    def tearDownClass(cls):
        pass

    def test_Cosmo_output_parsing(self):
        step_conf = {
            _SBE.STEPID: "01_cosmo",
            _SBE.STEP_TYPE: _SBE.STEP_COSMO,
            _SBE.EXEC: {_SBE.EXEC_PREFIXEXECUTION: "module load COSMOtherm/20.0.0"},
            _SBE.SETTINGS: {
                _SBE.SETTINGS_ARGUMENTS: {
                    _SBE.SETTINGS_ARGUMENTS_FLAGS: [],
                    _SBE.SETTINGS_ARGUMENTS_PARAMETERS: {},
                }
            },
        }
        cosmo_step = StepCosmo(**step_conf)
        cosmo_step.data.compounds = [self._paracetamol_molecule]
        cosmo_output_path = PATHS_EXAMPLEDATA.PARACETAMOL_COSMO_OUTPUT
        cosmo_step._parse_output(
            path_output=cosmo_output_path, conformer=cosmo_step.get_compounds()[0][0][0]
        )

        # test general block
        self.assertEqual(
            cosmo_step.get_compounds()[0][0][0].get_molecule().GetProp("E_cosmo"),
            "-406899.0254",
        )

        # test solvent blocks
        self.assertEqual(
            cosmo_step.get_compounds()[0][0][0].get_molecule().GetProp("Gsolv_meoh"),
            "-13.13470",
        )
        self.assertEqual(
            cosmo_step.get_compounds()[0][0][0].get_molecule().GetProp("Gsolv_h2o"),
            "-10.51388",
        )
        self.assertEqual(
            cosmo_step.get_compounds()[0][0][0].get_molecule().GetProp("G_propanone"),
            "-406899.11871",
        )
        try:
            self.assertEqual(
                cosmo_step.get_compounds()[0][0][0]
                .get_molecule()
                .GetProp("G_propanonee"),
                "",
            )
        except KeyError as e:
            self.assertEqual("'G_propanonee'", str(e))

    def test_Cosmo_run(self):
        step_conf = {
            _SBE.STEPID: "01_cosmo",
            _SBE.STEP_TYPE: _SBE.STEP_COSMO,
            _SBE.EXEC: {_SBE.EXEC_PREFIXEXECUTION: "module load COSMOtherm/20.0.0"},
            _SBE.SETTINGS: {
                _SBE.SETTINGS_ARGUMENTS: {
                    _SBE.SETTINGS_ARGUMENTS_FLAGS: [],
                    _SBE.SETTINGS_ARGUMENTS_PARAMETERS: {
                        _TE.CT_CONFIG: [
                            'ctd = BP_TZVPD_FINE_20.ctd cdir = "/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/CTDATA-FILES" ldir = "/opt/scp/software/COSMOtherm/20.0.0/licensefiles"',
                            "unit notempty wtln ehfile",
                            "!! generated by COSMOthermX !!",
                            "f = mol.cosmo",
                            'f = "h2o_c0.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/h" VPfile',
                            'f = "methanol_c0.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/m" VPfile',
                            'f = "1-octanol_c0.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/1" Comp = "1-octanol" [  VPfile',
                            'f = "1-octanol_c1.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/1"',
                            'f = "1-octanol_c2.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/1"',
                            'f = "1-octanol_c3.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/1"',
                            'f = "1-octanol_c4.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/1"',
                            'f = "1-octanol_c5.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/1"',
                            'f = "1-octanol_c6.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/1" ]',
                            'f = "dimethylsulfoxide_c0.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/d" VPfile',
                            'f = "cyclohexane_c0.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/c" VPfile',
                            'f = "chcl3_c0.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/c" VPfile',
                            'f = "propanone_c0.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/p" VPfile',
                            'f = "acetonitrile_c0.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/a" VPfile',
                            'f = "thf_c0.cosmo" fdir="/opt/scp/software/COSMOtherm/20.0.0/COSMOtherm/DATABASE-COSMO/BP-TZVPD-FINE/t" VPfile',
                            "henry= 2 tc=25.0 GSOLV",
                            "henry= 3 tc=25.0 GSOLV",
                            "henry= 4 tc=25.0 GSOLV",
                            "henry= 5 tc=25.0 GSOLV",
                            "henry= 6 tc=25.0 GSOLV",
                            "henry= 7 tc=25.0 GSOLV",
                            "henry= 8 tc=25.0 GSOLV",
                            "henry= 9 tc=25.0 GSOLV",
                            "henry= 10 tc=25.0 GSOLV",
                        ]
                    },
                }
            },
        }
        cosmo_step = StepCosmo(**step_conf)
        cosmo_step.data.compounds = [self._paracetamol_molecule]

        # conformer coordinates should not be touched by the execution
        self.assertListEqual(
            list(
                cosmo_step.get_compounds()[0][0][0]
                .get_molecule()
                .GetConformer(0)
                .GetPositions()[0]
            ),
            [5.3347, 12.9328, 24.6745],
        )
        cosmo_step.execute()
        self.assertListEqual(
            list(
                cosmo_step.get_compounds()[0][0][0]
                .get_molecule()
                .GetConformer(0)
                .GetPositions()[0]
            ),
            [5.3347, 12.9328, 24.6745],
        )
        self.assertEqual(
            cosmo_step.get_compounds()[0][0][0].get_molecule().GetProp("Gsolv_h2o"),
            "-10.51388",
        )
        cosmofile = cosmo_step.get_compounds()[0][0][0].get_extra_data()[
            _CTE.EXTRA_DATA_COSMOFILE
        ]
        self.assertTrue("nspa=   92" in cosmofile[5])

        # check write-out
        out_path = os.path.join(self._test_dir, "cosmo_output_files.sdf")
        cosmo_step.write_conformers(out_path)
        stat_inf = os.stat(out_path)
        self.assertEqual(stat_inf.st_size, 2010)

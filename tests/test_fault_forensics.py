import importlib.util
import unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/'skills/fault-forensics/scripts/decode_cortex_fault.py'
spec=importlib.util.spec_from_file_location('fault',P)
fault=importlib.util.module_from_spec(spec);spec.loader.exec_module(fault)

class FaultTests(unittest.TestCase):
    def capture(self,**changes):
        return {'architecture':'cortex-m4','cfsr':'0x02000000','hfsr':'0x40000000',**changes}
    def test_usage_escalation_is_not_root_cause(self):
        r=fault.decode(self.capture())
        self.assertIn('DIVBYZERO',r['cfsr_flags']);self.assertIn('FORCED',r['hfsr_flags'])
        self.assertEqual(r['evidence'],'offline-register-interpretation')
        self.assertIsNone(r['root_cause'])
    def test_address_requires_valid_flag_and_capture(self):
        r=fault.decode(self.capture(cfsr=0,bfar='0x20001000'))
        self.assertNotIn('bfar',r['valid_fault_addresses'])
        r=fault.decode(self.capture(cfsr='0x8200',bfar='0x20001000'))
        self.assertEqual(r['valid_fault_addresses']['bfar'],'0x20001000')
        r=fault.decode(self.capture(cfsr='0x8000'))
        self.assertIn('bfar-valid-but-not-captured',r['limitations'])
    def test_imprecise_and_bad_stack_preserve_uncertainty(self):
        r=fault.decode(self.capture(cfsr='0x1400',pc='0x08001234'))
        self.assertIn('IMPRECISERR',r['cfsr_flags'])
        self.assertIn('stack-frame-may-be-unreliable',r['limitations'])
        self.assertIn('stacked-pc-may-not-identify-origin',r['limitations'])
    def test_reserved_bits_not_silently_decoded(self):
        r=fault.decode(self.capture(cfsr='0x00100000'))
        self.assertEqual(r['unmapped_cfsr_bits'],'0x00100000')
    def test_unknown_architecture_and_malformed_register_rejected(self):
        for change in ({'architecture':'cortex-m0plus'},{'cfsr':True},{'cfsr':-1},{'cfsr':2**32},{'hfsr':'oops'},{'pc':None}):
            with self.subTest(change=change),self.assertRaises(ValueError):fault.decode(self.capture(**change))
    def test_m3_reserved_fp_bits_stay_unmapped(self):
        r=fault.decode(self.capture(architecture="cortex-m3",cfsr=32))
        self.assertEqual(r["unmapped_cfsr_bits"],"0x00000020")
        self.assertNotIn("MLSPERR",r["cfsr_flags"])
        self.assertNotIn("stack-frame-may-be-unreliable",r["limitations"])
    def test_zero_flags_are_not_a_health_check(self):
        r=fault.decode(self.capture(cfsr=0,hfsr=0))
        self.assertIsNone(r['root_cause']);self.assertIn('capture-does-not-establish-device-health',r['limitations'])

if __name__=='__main__':unittest.main()

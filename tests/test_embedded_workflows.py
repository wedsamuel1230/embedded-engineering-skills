"""Behavior tests for offline intake, provenance and explicit telemetry analysis."""
from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


intake = load("intake", "skills/embedded-build-workflow/scripts/inspect_build.py")
memory = load("memory", "skills/embedded-build-workflow/scripts/check_memory_config.py")
trace = load("trace", "skills/wireless-telemetry/scripts/analyze_trace.py")


class OfflineIntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def project(self, name, text):
        folder = self.root / name; folder.mkdir(parents=True, exist_ok=True)
        (folder / "platformio.ini").write_text(text)
        return folder

    def test_mixed_projects_and_no_execution(self):
        self.project("native", "[env]\nplatform=platformio/espressif32@7.0.1\nboard=n16r8\n[env:robot]\nframework=espidf\nextra_scripts=sentinel.py\n")
        self.project("legacy", "[env:n16r8]\nplatform=locked-release\nboard=n16r8\nframework=arduino\n")
        marker = self.root / "executed"
        (self.root / "native/sentinel.py").write_text(f"open({str(marker)!r},'w').write('BAD')")
        before = {str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with patch.object(subprocess, "run", side_effect=AssertionError("must not execute")):
            result = intake.inspect(self.root)
        self.assertEqual(len(result['projects']), 2)
        self.assertEqual({p['environments'][0]['framework'] for p in result['projects']}, {'arduino','espidf'})
        self.assertFalse(marker.exists())
        self.assertEqual(before, {str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_inheritance_interpolation_and_secrets_remain_unresolved(self):
        self.project("p", "[platformio]\nextra_configs=../secret.ini\n[env:x]\nextends=env:base\nplatform=${common.platform}\nframework=espidf\nboard=test\nwifi_password=DO_NOT_REPORT\n")
        result = intake.inspect(self.root)['projects'][0]
        self.assertEqual(result['configuration_status'], 'unresolved')
        self.assertNotIn('DO_NOT_REPORT', json.dumps(result))
        self.assertIsNone(result['environments'][0]['platform'])

    def test_bad_environment_tokens_never_become_commands(self):
        for index, name in enumerate(('-x', 'space name', 'x;touch', 'x$(touch)', 'x`touch`')):
            self.project(str(index), f"[env:{name}]\nplatform=p\nframework=espidf\nboard=b\n")
        self.assertTrue(all(not p['environments'] for p in intake.inspect(self.root)['projects']))

    def test_url_credentials_are_redacted(self):
        self.project("p", "[env:x]\nplatform=https://USER:PRIVATE@host/a?token=SECRET\nframework=espidf\nboard=b\n")
        result = json.dumps(intake.inspect(self.root))
        self.assertNotIn('PRIVATE', result); self.assertNotIn('SECRET', result)
        self.assertIn('redacted-url', result)

    def test_generated_and_symlink_directories_are_ignored(self):
        self.project('.pio', '[env:bad]\n')
        if hasattr(Path, 'symlink_to'):
            try:
                (self.root / 'linked').symlink_to(self.root / '.pio', target_is_directory=True)
            except OSError:
                pass  # Windows may lack symlink privilege; .pio exclusion still checked.
        self.assertEqual(intake.inspect(self.root)['projects'], [])

    def test_duplicate_ini_and_unknown_target_do_not_pass(self):
        self.project('p', '[env:x]\n[env:x]\n')
        result = intake.inspect(self.root)['projects'][0]
        self.assertEqual(result['issues'], ['invalid-ini'])

    def test_micropython_source_is_detected_without_rust_route(self):
        (self.root/'py').mkdir();(self.root/'py/mpconfig.h').write_text('/* port config */')
        (self.root/'ports').mkdir();(self.root/'Cargo.toml').write_text('[package]')
        result=intake.inspect(self.root)
        self.assertEqual([h['framework_hint'] for h in result['native_hints']],['micropython'])


class MemoryEvidenceTests(unittest.TestCase):
    CONFIG = 'CONFIG_IDF_TARGET="esp32s3"\nCONFIG_ESPTOOLPY_FLASHSIZE_16MB=y\nCONFIG_ESPTOOLPY_FLASHMODE="qio"\nCONFIG_SPIRAM=y\nCONFIG_SPIRAM_MODE_OCT=y\n'
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        (self.root/'platformio.ini').write_text('[env:robot]\nframework=espidf\n')
        (self.root/'sdkconfig').write_text(self.CONFIG)
        self.expected={'chip':'esp32s3','board_identity':'declared DevKitC-1 rev1.1','module':'N16R8',
                       'flash_mb':16,'flash_mode':'qio','psram_mb':8,'psram_mode':'octal'}

    def provenance(self):
        return {'environment':'robot','framework':'espidf','framework_version':'6.0.1',
                'tool_versions':{'platformio':'6.2.0'},'sdkconfig_sha256':memory.digest(self.root/'sdkconfig'),
                'input_hashes':{'platformio.ini':memory.digest(self.root/'platformio.ini')}}

    def run_check(self, provenance=None):
        return memory.check(self.root, Path('sdkconfig'), self.expected, 'robot',
                            provenance if provenance is not None else self.provenance())

    def test_consistent_is_not_physical_memory_proof(self):
        result=self.run_check()
        self.assertEqual(result['status'], 'consistent-with-inspected-evidence')
        self.assertIn('physical-memory-capacity', result['unverified'])

    def test_wrong_capacity_and_psram_mode(self):
        self.expected['flash_mb']=32; self.expected['psram_mode']='quad'
        result=self.run_check()
        self.assertEqual(result['status'], 'confirmed-mismatch')
        self.assertEqual(result['findings'], ['flash_mb-mismatch','psram_mode-mismatch'])

    def test_missing_setting_is_unresolved_not_disabled(self):
        (self.root/'sdkconfig').write_text(self.CONFIG.replace('CONFIG_SPIRAM=y\n',''))
        self.assertEqual(self.run_check()['status'], 'unresolved')

    def test_explicit_disabled_psram_is_mismatch(self):
        (self.root/'sdkconfig').write_text(self.CONFIG.replace('CONFIG_SPIRAM=y','\n# CONFIG_SPIRAM is not set').replace('CONFIG_SPIRAM_MODE_OCT=y',''))
        self.assertIn('psram-disabled', self.run_check()['findings'])
        self.assertEqual(self.run_check()['status'], 'confirmed-mismatch')

    def test_conflicting_modes_are_unresolved(self):
        (self.root/'sdkconfig').write_text(self.CONFIG+'CONFIG_SPIRAM_MODE_QUAD=y\n')
        self.assertEqual(self.run_check()['status'], 'unresolved')

    def test_wrong_environment_and_unsupported_version(self):
        p=self.provenance(); p['environment']='receiver'
        self.assertEqual(self.run_check(p)['status'], 'unresolved')
        p=self.provenance(); p['framework_version']='unknown'
        self.assertEqual(self.run_check(p)['status'], 'unresolved')

    def test_changed_input_and_stale_generated_artifact(self):
        p=self.provenance(); (self.root/'platformio.ini').write_text('changed')
        self.assertEqual(self.run_check(p)['status'], 'unresolved')
        p=self.provenance(); (self.root/'sdkconfig').write_text(self.CONFIG+'# changed\n')
        self.assertEqual(self.run_check(p)['status'], 'unresolved')

    def test_missing_provenance_and_outside_input(self):
        self.assertEqual(self.run_check({})['status'], 'unresolved')
        p=self.provenance(); p['input_hashes']['../outside']='0'*64
        self.assertEqual(self.run_check(p)['status'], 'unresolved')

    def test_other_chip_and_incomplete_physical_identity(self):
        self.expected['chip']='rp2040'
        self.assertEqual(self.run_check()['status'], 'not-applicable')
        self.expected['chip']='esp32s3'; self.expected['board_identity']='unknown'
        self.assertEqual(self.run_check()['status'], 'unresolved')

    def test_conflicting_duplicate_mode_and_invalid_identity(self):
        (self.root/'sdkconfig').write_text(self.CONFIG+'CONFIG_ESPTOOLPY_FLASHMODE_QIO=n\nCONFIG_ESPTOOLPY_FLASHMODE_QIO=y\n')
        self.assertEqual(self.run_check()['status'], 'unresolved')
        (self.root/'sdkconfig').write_text(self.CONFIG)
        self.expected['board_identity']=True
        self.assertEqual(self.run_check()['status'], 'unresolved')


class TraceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'trace.csv'

    def telemetry(self, seq, rx, boot='a'):
        return dict(schema_version='1',kind='telemetry',session_id='s',stream='status',boot_id=boot,
                    seq=str(seq),rx_ms=str(rx),clock_id='pc',request_id='',request_ms='',reply_ms='',tx_clock_id='')

    def rtt(self, request='r', clock='pc'):
        return dict(schema_version='1',kind='rtt',session_id='s',stream='',boot_id='',seq='',rx_ms='',
                    clock_id='pc',request_id=request,request_ms='100',reply_ms='112',tx_clock_id=clock)

    def analyze(self, rows):
        with self.path.open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=trace.FIELDS); writer.writeheader(); writer.writerows(rows)
        return trace.analyze(self.path)

    def test_gaps_duplicates_and_reorder_are_not_loss(self):
        result=self.analyze([self.telemetry(1,10),self.telemetry(3,30),self.telemetry(2,40),self.telemetry(3,50)])
        self.assertEqual(result['observed_forward_gaps'],1)
        self.assertEqual(result['late_or_stale'],1); self.assertEqual(result['duplicates'],1)
        self.assertIsNone(result['loss_rate']); self.assertIsNone(result['one_way_latency'])

    def test_wrap_and_boot_reset_have_separate_epochs(self):
        result=self.analyze([self.telemetry(0xffffffff,10),self.telemetry(0,20),self.telemetry(1,30,'b')])
        self.assertEqual(result['sequence_wraps'],1); self.assertEqual(result['sequence_epochs'],2)
        self.assertEqual(result['observed_forward_gaps'],0)

    def test_unknown_boot_and_half_range_are_ambiguous(self):
        result=self.analyze([self.telemetry(1,10),self.telemetry(0x80000001,20),self.telemetry(2,30,'')])
        self.assertEqual(result['ambiguous_rows'],2)
        self.assertEqual(result['observed_forward_gaps'],0)

    def test_rtt_pairing_duplicate_and_cross_clock(self):
        result=self.analyze([self.rtt(),self.rtt(),self.rtt('bad','device')])
        self.assertEqual(result['rtt']['mean'],12); self.assertEqual(result['rtt']['samples'],1)
        self.assertEqual(result['duplicate_rtt'],1); self.assertEqual(result['rejected_rows'],1)
        self.assertEqual(result['status'],'invalid-input')

    def test_nonfinite_negative_and_missing_fields_count_rejections(self):
        row=self.telemetry(1,'NaN'); missing=self.rtt('missing'); missing['reply_ms']=''
        result=self.analyze([row,self.telemetry(2,-1),missing])
        self.assertEqual(result['rejected_rows'],3); self.assertEqual(result['accepted_rows'],0)

    def test_receiver_clock_regression_and_empty_input(self):
        result=self.analyze([self.telemetry(1,20),self.telemetry(2,10)])
        self.assertEqual(result['rejected_rows'],1)
        result=self.analyze([])
        self.assertEqual(result['rtt']['samples'],0); self.assertEqual(result['sequence_epochs'],0)

    def test_schema_and_size_limits_fail_clearly(self):
        self.path.write_text('other,columns\n1,2\n')
        with self.assertRaises(ValueError): trace.analyze(self.path)
        self.analyze([self.telemetry(1,10),self.telemetry(2,20)])
        with patch.object(trace,'MAX_ROWS',1), self.assertRaises(ValueError): trace.analyze(self.path)

    def test_no_initial_or_tail_gap_assumed(self):
        result=self.analyze([self.telemetry(1000,0)])
        self.assertEqual(result['observed_forward_gaps'],0)
        self.assertEqual(result['receiver_interarrival']['samples'],0)


if __name__ == '__main__':
    unittest.main()

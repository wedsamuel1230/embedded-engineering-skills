import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('platforms',ROOT/'scripts/validate_platforms.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class PlatformTests(unittest.TestCase):
    def test_portable_catalogue_discovers_all_skills_once(self):
        catalog=json.loads((ROOT/'catalog/index.json').read_text())
        names=[n for c in catalog['categories'] for n in c['skills']]
        actual={p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')}
        self.assertEqual(len(names),len(set(names)));self.assertEqual(set(names),actual)
        for c in catalog['categories']:
            self.assertTrue((ROOT/'catalog'/c['id']/'README.md').is_file())
            for n in c['skills']:
                self.assertIn(f'../../skills/{n}/SKILL.md',(ROOT/'catalog'/c['id']/'README.md').read_text())
    def test_identity_and_openai_presentation_migrate_together(self):
        manifests=[json.loads((ROOT/p).read_text()) for p in ('plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json','.cursor-plugin/plugin.json')]
        self.assertEqual({m['name'] for m in manifests},{'embedded-engineering-skills'})
        self.assertEqual({m['version'] for m in manifests},{'2.0.0'})
        self.assertNotIn('skills',manifests[0])
        self.assertEqual(manifests[0]['extensions']['com.openai']['interface'],manifests[1]['interface'])
        self.assertLessEqual(len(manifests[1]['interface']['shortDescription']),30)
        self.assertLessEqual(len(manifests[1]['interface']['defaultPrompt']),3)
        self.assertTrue(all('rust' not in m['keywords'] for m in manifests))
    def test_native_plans_have_no_device_or_download_step(self):
        cmds=mod.native_plan('pico-sdk','/sdk','/output','/toolchain')
        self.assertEqual(cmds[0][0],'cmake');self.assertEqual(cmds[1][:2],['cmake','--build'])
        mp=mod.native_plan('micropython','/sdk','/output',host='Darwin')
        self.assertIn('MICROPY_PY_THREAD=1',mp[0]);self.assertIn('CFLAGS_EXTRA=-Wno-error=gnu-folding-constant',mp[0])
        self.assertEqual(mp[1][0],str(Path('/output').resolve()/'micropython'))
        with self.assertRaises(ValueError):mod.native_plan('micropython','/sdk','/sdk/output')
        with self.assertRaises(ValueError):mod.native_plan('micropython','/sdk','/output',host='Windows')
        with self.assertRaises(ValueError):mod.native_plan('pico-sdk','/sdk','/output')
if __name__=='__main__':unittest.main()

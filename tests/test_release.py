import ast
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "plejd"


class ReleaseTests(unittest.TestCase):
    def test_manifest_pins_exact_reliability_commit(self):
        manifest = json.loads((COMPONENT / "manifest.json").read_text())
        self.assertEqual(manifest["version"], "0.21.3.post3")
        pyplejd = next(
            requirement
            for requirement in manifest["requirements"]
            if requirement.startswith("pyplejd ")
        )
        self.assertRegex(
            pyplejd,
            r"^pyplejd @ git\+https://github\.com/krsch79/pyplejd\.git@[0-9a-f]{40}$",
        )

    def test_reliability_defaults_are_enabled(self):
        tree = ast.parse((COMPONENT / "const.py").read_text())
        values = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Name):
                    values[target.id] = ast.literal_eval(node.value)
        self.assertFalse(values["ENABLE_ACTIVE_BUTTON_POLLING"])
        self.assertTrue(values["RECONNECT_NON_GATEWAY_CONTROL_WRITES"])
        self.assertEqual(values["DUPLICATE_BUTTON_EVENT_WINDOW_SECONDS"], 0.25)

    def test_component_sources_compile(self):
        for path in COMPONENT.glob("*.py"):
            compile(path.read_text(), str(path), "exec")

    def test_no_unpinned_pyplejd_requirement(self):
        manifest_text = (COMPONENT / "manifest.json").read_text()
        self.assertNotIn('"pyplejd==', manifest_text)
        self.assertEqual(len(re.findall(r"krsch79/pyplejd\.git@[0-9a-f]{40}", manifest_text)), 1)


if __name__ == "__main__":
    unittest.main()

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
        self.assertEqual(manifest["version"], "0.21.3.post12")
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
        self.assertTrue(values["ROUTE_CONTROL_WRITES_DIRECTLY"])
        self.assertTrue(values["RECONNECT_NON_GATEWAY_CONTROL_WRITES"])
        self.assertTrue(values["ON_DEMAND_CONTROL_CONNECTIONS"])
        self.assertEqual(values["DUPLICATE_BUTTON_EVENT_WINDOW_SECONDS"], 0.25)

    def test_on_demand_mode_uses_advertisements_without_keepalive(self):
        site_source = (COMPONENT / "plejd_site.py").read_text()
        entity_source = (COMPONENT / "plejd_entity.py").read_text()
        self.assertIn(
            "self.manager.disconnect_after_direct_control_write",
            site_source,
        )
        self.assertIn(
            "self.manager.filter_direct_state_updates = "
            "ON_DEMAND_CONTROL_CONNECTIONS",
            site_source,
        )
        self.assertIn(
            "self.manager.advertisement_callback(service_info.device.address)",
            site_source,
        )
        self.assertIn("if not ON_DEMAND_CONTROL_CONNECTIONS:", site_source)
        self.assertIn("self._data = self.device.state", entity_source)

    def test_component_sources_compile(self):
        for path in COMPONENT.glob("*.py"):
            compile(path.read_text(), str(path), "exec")

    def test_no_unpinned_pyplejd_requirement(self):
        manifest_text = (COMPONENT / "manifest.json").read_text()
        self.assertNotIn('"pyplejd==', manifest_text)
        self.assertEqual(len(re.findall(r"krsch79/pyplejd\.git@[0-9a-f]{40}", manifest_text)), 1)

    def test_gateway_selector_is_a_disabled_config_entity(self):
        tree = ast.parse((COMPONENT / "switch.py").read_text())
        gateway_class = next(
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef)
            and node.name == "PlejdConnectableSwitch"
        )
        categories = [
            node
            for node in gateway_class.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name)
                and target.id == "_attr_entity_category"
                for target in node.targets
            )
        ]
        self.assertEqual(len(categories), 1)
        value = categories[0].value
        self.assertIsInstance(value, ast.Attribute)
        self.assertEqual(value.attr, "CONFIG")

        enabled_defaults = [
            node
            for node in gateway_class.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name)
                and target.id == "_attr_entity_registry_enabled_default"
                for target in node.targets
            )
        ]
        self.assertEqual(len(enabled_defaults), 1)
        self.assertIsInstance(enabled_defaults[0].value, ast.Constant)
        self.assertFalse(enabled_defaults[0].value.value)

    def test_on_demand_mode_does_not_create_gateway_entities(self):
        binary_sensor_source = (COMPONENT / "binary_sensor.py").read_text()
        switch_source = (COMPONENT / "switch.py").read_text()
        self.assertIn("if not ON_DEMAND_CONTROL_CONNECTIONS:", binary_sensor_source)
        self.assertIn(
            "device.hw._powered and not ON_DEMAND_CONTROL_CONNECTIONS",
            switch_source,
        )

    def test_light_commands_have_structured_audit_logging(self):
        light_source = (COMPONENT / "light.py").read_text()
        self.assertIn("PLEJD_COMMAND_AUDIT", light_source)
        self.assertIn("_LOGGER.warning", light_source)
        self.assertIn('self._audit_command("turn_off")', light_source)
        self.assertIn('"turn_on",', light_source)
        self.assertNotIn("password", light_source.lower())


if __name__ == "__main__":
    unittest.main()

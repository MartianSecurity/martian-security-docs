"""Focused regressions for evidence preservation, malformed captures and readback."""

import copy
import importlib.util
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zlib

spec = importlib.util.spec_from_file_location("docs_maintenance", Path(__file__).with_name("docs_maintenance.py"))
maintenance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(maintenance)


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def png(extra=b""):
    header = struct.pack(">IIBBBBB", 1440, 1000, 8, 2, 0, 0, 0)
    pixels = zlib.compress((b"\0" + b"\0" * (1440 * 3)) * 1000)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + extra + chunk(b"IDAT", pixels) + chunk(b"IEND", b"")


class EvidenceTests(unittest.TestCase):
    def test_requirement_trimming_and_changed_capture_are_reported_but_additions_are_allowed(self):
        coverage = {"guides": [{"id": "sample", "requiredValidation": ["run", "refresh"], "screenshots": ["sample-shot"]}]}
        captures = {"screenshots": [{"id": "sample-shot", "sha256": "original"}]}
        current, images = copy.deepcopy(coverage), copy.deepcopy(captures)
        current["guides"].append({"id": "new-guide"})
        images["screenshots"].append({"id": "new-shot"})
        self.assertEqual(maintenance.compare_baseline(coverage, current, captures, images), [])
        current["guides"][0]["requiredValidation"].pop()
        images["screenshots"][0]["sha256"] = "replacement"
        changes = maintenance.compare_baseline(coverage, current, captures, images)
        self.assertEqual({row["change"] for row in changes}, {"requiredValidation", "changed_or_removed"})

    def test_crc_corruption_and_truncated_png_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "capture.png"
            path.write_bytes(png())
            self.assertTrue(maintenance.inspect_png(path)["matchesCurrentCaptureViewport"])
            for raw in [png()[:-1], png()[:40] + bytes([png()[40] ^ 1]) + png()[41:]]:
                with self.subTest(kind="invalid PNG"):
                    path.write_bytes(raw)
                    with self.assertRaises(ValueError):
                        maintenance.inspect_png(path)

    def test_png_metadata_is_flagged_without_disclosing_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "capture.png"
            path.write_bytes(png(chunk(b"tEXt", b"comment\0private synthetic canary")))
            result = maintenance.inspect_png(path)
            self.assertEqual(result["metadataChunksNeedingReview"], ["tEXt"])
            self.assertNotIn("private synthetic canary", str(result))

    def test_artifact_traversal_and_symlink_escape_are_refused(self):
        for route in ["//another.example/file", "/../secret", "/%2e%2e/secret", "/file?token=value", "https://another.example/file"]:
            with self.subTest(route=route), self.assertRaises(ValueError):
                maintenance.public_route(route)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "artifacts"
            root.mkdir()
            (root / "escaped").symlink_to(Path(temp))
            with self.assertRaises(ValueError):
                maintenance.expected_file(root, "/escaped/file")
        for site in ["http://example.test", "https://user:password@example.test", "https://example.test?token=value"]:
            with self.subTest(site=site), self.assertRaises(ValueError):
                maintenance.https_site(site)

    def test_http_success_with_wrong_bytes_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "index.html").write_text("reviewed build")

            def received(url, target, timeout):
                target.write_text("older deployed build")
                return url

            with patch.object(maintenance, "fetch_https", side_effect=received):
                result = maintenance.verify_published(root, "https://example.test", ["/"], root, 30)
            self.assertFalse(result["allHashesMatch"])
            self.assertFalse(result["checks"][0]["matchesExpectedArtifact"])


if __name__ == "__main__":
    unittest.main()

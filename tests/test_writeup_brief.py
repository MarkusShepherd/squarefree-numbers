"""Optional briefing tests; no provider invocations or Git mutations."""
import argparse
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import writeup_support as writeup


class BriefingTest(unittest.TestCase):
    def test_briefing_is_optional(self):
        self.assertEqual(writeup.briefing_input(None), {})

    def test_explicit_briefing_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'instructions.md'
            path.write_text('Specific instructions.\n')
            self.assertEqual(writeup.briefing_input(path), {'brief.md': path})
            self.assertEqual(path.read_text(), 'Specific instructions.\n')

    def test_missing_or_symlinked_briefing_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'missing.md'
            with self.assertRaises(ValueError):
                writeup.briefing_input(path)
            path.write_text('Instructions.\n')
            link = Path(tmp) / 'link.md'
            link.symlink_to(path)
            with self.assertRaises(ValueError):
                writeup.briefing_input(link)

    def test_check_accepts_no_briefing_and_validates_explicit_briefing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            driver = SimpleNamespace(ROOT=root, log=lambda message: None)
            args = argparse.Namespace(label='example', check=True, papers_dir=None, brief=None)
            with patch.object(writeup, 'archive_sources', return_value=(root, {}, {})):
                writeup.writeup(driver, args)
                args.brief = root / 'missing.md'
                with self.assertRaises(ValueError):
                    writeup.writeup(driver, args)
                args.brief.write_text('Instructions.\n')
                writeup.writeup(driver, args)

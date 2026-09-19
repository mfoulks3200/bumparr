import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from bumparr import brandslam, config, render_cards


class FontConfiguration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.font_dir = Path(self.tmp.name)
        self.brand = self.font_dir / "Brand.ttf"
        self.brand.touch()

    def tearDown(self):
        self.tmp.cleanup()

    def test_card_renderer_searches_configured_font_directory(self):
        with patch.object(config, "FONT_DIR", self.font_dir):
            self.assertEqual(render_cards._resolve_font_file("Brand.ttf", []),
                             str(self.brand))

    def test_static_slam_uses_configured_brand_font(self):
        pool = [self.brand, self.font_dir / "Other.ttf"]
        with patch.object(config, "BRAND_FONT", "Brand.ttf"):
            self.assertEqual(brandslam.static_face(random.Random(1), pool),
                             str(self.brand))

    def test_roulette_lands_on_configured_brand_font(self):
        pool = [self.brand] + [self.font_dir / ("Other%d.ttf" % i) for i in range(4)]
        with patch.object(config, "BRAND_FONT", "Brand.ttf"), \
             patch.object(config, "ROULETTE_MIN_FONTS", 4):
            spec = brandslam.roll(random.Random(1), pool, prob=1.0)
        self.assertEqual(spec["landing"], str(self.brand))


if __name__ == "__main__":
    unittest.main(verbosity=2)

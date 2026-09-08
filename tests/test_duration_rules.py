import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src' / 'ortho_pheno'))
from duration_rules import cn_number, extract_duration_days


class DurationRuleTests(unittest.TestCase):
    def assertOneDuration(self, text, expected, places=2):
        values = extract_duration_days(text)
        self.assertEqual(len(values), 1, msg=f'{text!r} -> {values!r}')
        self.assertAlmostEqual(values[0], expected, places=places)

    def test_arabic_and_chinese_numbers(self):
        self.assertEqual(cn_number('3'), 3.0)
        self.assertEqual(cn_number('三'), 3)
        self.assertEqual(cn_number('十'), 10)
        self.assertEqual(cn_number('十二'), 12)
        self.assertEqual(cn_number('二十'), 20)

    def test_one_and_half_month_is_not_truncated(self):
        self.assertOneDuration('外伤后腕痛1个半月', 1.5 * 30.44)

    def test_one_and_half_year_is_not_truncated(self):
        self.assertOneDuration('右腕受伤1年半', 1.5 * 365.25)

    def test_half_year(self):
        self.assertOneDuration('腕部疼痛半年', 0.5 * 365.25)

    def test_weeks_days_hours(self):
        self.assertOneDuration('外伤后3周', 21.0)
        self.assertOneDuration('摔伤10天', 10.0)
        self.assertOneDuration('受伤12小时', 0.5)

    def test_multiple_distinct_durations_are_preserved(self):
        values = extract_duration_days('2年前受伤，近3天疼痛加重')
        self.assertEqual(len(values), 2)
        self.assertAlmostEqual(max(values), 2 * 365.25, places=2)
        self.assertAlmostEqual(min(values), 3.0, places=2)


if __name__ == '__main__':
    unittest.main()

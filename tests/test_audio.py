import unittest
import audio

class TestExample(unittest.TestCase):

    def test_chorus_filter(self):
        res = audio.Chorus('foo', 'bar',
            delay='del',
            decay='dec',
            speed='s',
            depth='dep').as_string()
        expected = 'chorus=foo:bar:del:dec:s:dep'
        self.assertEqual(res, expected)

        res = audio.Chorus(1,2,3,4,5,6).as_string()
        expected = 'chorus=1:2:3:4:5:6'
        self.assertEqual(res, expected)

    def test_empty_filter(self):
        self.assertEqual(audio.create_filter_string(), '')

    def test_filter_string(self):
        string = 'chorus=foo:bar:del:dec:s:dep'
        expected = '-filter_complex "{}"'.format(string)
        res = audio.create_filter_string([string])

        self.assertEqual(res, expected)

    def test_filter_effect_instance(self):
        res = audio.create_filter_string([audio.Chorus(1,2,3,4,5,6)])
        expected = '-filter_complex "chorus=1:2:3:4:5:6"'
        self.assertEqual(res, expected)

    def test_filter_multi_effect(self):
        expected = '-filter_complex "chorus=1:2:3:4:5:6, aecho=1:2:3:4, banana milkshake"'
        res = audio.create_filter_string([
            audio.Chorus(1,2,3,4,5,6),
            audio.Echo(1,2,3,4,5,6),
            'banana milkshake',
            ])
        self.assertEqual(res, expected)

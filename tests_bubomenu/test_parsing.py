import unittest
# import os
# import sys
# sys.path.insert(0, os.path.abspath('..'))
from bubomenu import parsing


class MenuParserTestCase(unittest.TestCase):
    def setUp(self):
        self.sut = parsing.MenuParser()

    def test_parseLink_ifPresent_shouldReturnLink(self):
        # when
        ret = self.sut.parseLink("This is line|with.some.link")

        # then
        self.assertEqual("with.some.link", ret)

    def test_parseLink_ifEmptyLink_shouldReturnNone(self):
        # when
        ret = self.sut.parseLink("This is line")

        # then
        self.assertEqual(None, ret)

    def test_parseLink_ifNoLink_shouldReturnEmptyString(self):
        # when
        ret = self.sut.parseLink("This is line|")

        # then
        self.assertEqual("", ret)


class MenuItemsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_MenuRootButton_parseLine_ShouldConsumeFirstInput(self):
        pass

    def test_MenuRootButton_parseLine_ifFirstInputHasLink_ShouldThrow(self):
        pass

    def test_MenuRootButton_parseLine_ShouldCreateMenu(self):
        # created menu
        # returned menu
        pass

if __name__ == '__main__':
    unittest.main()
import unittest
# from mock import patch, Mock, MagicMock

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

    def test_firstParseLine_shouldCreateRootButton(self):
        # when
        self.sut.parseLine("UKRAINA")

        # then
        self.assertEqual(parsing.MenuRootButton, type(self.sut._current_item))

    def test_oneItemMenu_shouldParse(self):
        # when
        self.sut.parseLine("UKRAINA")
        self.sut.parseLine("    UKRAINA|http://jabolowaballada.blogspot.com/search/label/ukraina")

        # then
        self.assertEqual(parsing.Menu, type(self.sut._current_item))


class MenuItemsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_MenuRootButton_parseLine_ShouldConsumeFirstInput(self):
        # given
        sut = parsing.MenuRootButton(None)

        # when
        ret = sut.parseLine("A blablabla")

        # then
        self.assertEqual(sut, ret)
        self.assertEqual(0, len(sut._rg_child))

    def test_MenuRootButton_parseLine_ifFirstInputHasLink_ShouldThrow(self):
        # given
        sut = parsing.MenuRootButton(None)

        # when
        # then
        self.assertRaises(Exception, sut.parseLine, "A blablabla|")
        self.assertRaises(Exception, sut.parseLine, "A blablabla|some.link")

    def test_MenuRootButton_parseLine_ShouldCreateMenu(self):
        # created menu
        # returned menu
        pass


if __name__ == '__main__':
    unittest.main()

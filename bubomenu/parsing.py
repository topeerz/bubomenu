import re


class AbstractMenuItem(object):
    def __init__(self, parent):
        self._parent = parent
        self._rg_child = []
        self._content = None

    def parseLine(self, line):
        """
        :param line: input data
        :return: entity to handle next input (self, child or None)
        """
        raise NotImplementedError("Not implemented")

    def parseMyself(self, line):
        raise NotImplementedError("Not implemented")

    def html(self):
        html = "%(content)s" % { "content" : self._content }
        for child in self._rg_child:
           html += child.html()

        return html

class MenuRootButton(AbstractMenuItem):
    def parseMyself(self, line):
        self._content = line

    def parseLine(self, line):
        """
        :param line: parse data
        :return: return object to receive next input (child, parent or self)
        """

        root_button_initialized = self._content
        if not root_button_initialized:
            # my
            link = MenuParser.parseLink(line)
            if link or link == "":
                raise RuntimeError("Can't parse this")

            self.parseMyself(line)
            return self

        elif MenuParser.parseLink(line):
            if not len(self._rg_child):
                # first item is header
                child_menu = MenuHeaderItem(self)

            else:
                # otherwise menu item
                child_menu = MenuItem(self)

            self._rg_child.append(child_menu)
            return child_menu.parseLine(line)

        elif line and not MenuParser.parseLink(line):
            # submenu item
            child_menu = SubmenuItem(self)
            self._rg_child.append(child_menu)
            return child_menu.parseLine(line)

        else:
            # empty - we are done
            return self._parent


class MenuHeaderItem(AbstractMenuItem):
    def parseMyself(self, line):
        self._content = line

    def parseLine(self, line):
        self.parseMyself(line)
        return self._parent


class MenuItem(AbstractMenuItem):
    def parseMyself(self, line):
        self._content = line

    def parseLine(self, line):

        if MenuParser.parseLink(line):
            self._content = line
            return self._parent

        elif line and not MenuParser.parseLink(line):
            # submenu item
            child_menu = SubmenuItem(self)
            self._rg_child.append(child_menu)
            return child_menu.parseLine(line)

        else:
            # end
            return self._parent


class SubmenuItem(AbstractMenuItem):
    def parseMyself(self, line):
        self._content = line

    def parseLine(self, line):

        if MenuParser.parseLink(line):
            # submenu menu item
            child_menu = MenuItem(self)
            self._rg_child.append(child_menu)
            return child_menu.parseLine(line)

        elif "END_SUBMENU" in line:
            return self._parent

        elif line and not MenuParser.parseLink(line):
            self.parseMyself(line)
            return self

        else:
            raise RuntimeError("Can't parse this")


class MenuParser(object):
    """
    creating tree of menu objects
    providing html version
    providing helper methods
    """

    def __init__(self):
        self._buffer = None  # buffer to parse
        self._root_item = None  # root element
        self._current_item = None  # currently parsed element

    @staticmethod
    def parseLink(line):
        """String with link or Null"""
        link = None
        rg_line = line.split("|", 1)
        if len(rg_line) > 1:
            link = rg_line[1]

        return link

    def parseBuffer(self, buffer):
        self._buffer = buffer
        # slice line by line and feed parse line

    def parseLine(self, line):

        if self._current_item:
            self._current_item = self._current_item.parseLine(line)

        else:
            self._current_item = MenuRootButton(None)

            if not self._root_item:
                self._root_item = self._current_item;

            self._current_item = self._current_item.parseLine(line)

    def html(self):
        return self._root_item.html()

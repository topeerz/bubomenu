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

    def html(self):
        raise NotImplementedError("Not implemented")


class MenuRootButton(AbstractMenuItem):
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

            self._content = line
            return self

        elif MenuParser.parseLink(line):
            # menu item
            child_menu = Menu(self)
            self._rg_child + [child_menu]
            return child_menu.parseLine(line)

        elif not MenuParser.parseLink(line):
            # submenu item
            # my child
            # add child
            # pass line child
            # return what child returned
            raise RuntimeError("Not supported yet")

        elif line:
            return self

        else:
            # empty - we are done
            return self._parent


class Menu(AbstractMenuItem):
    def parseLine(self, line):
        return self


class MenuItem(AbstractMenuItem):
    def parseLine(self, line):
        pass


class SubmenuItem(AbstractMenuItem):
    def parseLine(self, line):
        pass


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
            self._current_item = self._current_item.parseLine(line)

    def html(self):
        return self._root_item.html()
        # if hasLink
        # if in button
        # if first in submenu
        # add header
        # else
        # add item
        # end
        #

        # else
        # if not in button
        # start button
        # else
        # if not in submenu - only one level of submenu supported rightnow
        # start submenu
        # else
        # close submenu
        # start submenu
        # end
        # end

        # end

        # if end
        # close submenu (if open)
        # close button
        # end

        # render to html

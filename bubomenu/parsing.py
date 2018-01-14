import re


class AbstractMenuItem(object):
    def __init__(self,parent):
        self._parent = parent
        self._rg_child = ()
        self._content = None

    def parseLine(self, line):
        raise NotImplementedError("Not implemented")


class MenuRootButton(AbstractMenuItem):
    def parseLine(self, line):

        root_button_initialized = self._content
        if not root_button_initialized:
            # my
            if MenuParser.parseLink(line):
                raise RuntimeError("Can't parse this")

            self._content = line
            return self

        elif MenuParser.parseLink(line):
            # menu item
            child_menu = Menu(self)
            self._rg_child.add(child_menu)
            return child_menu.parseLine(line)

        elif not MenuParser.parseLink(line):
            # submenu item
            # my child
            # add child
            # pass line child
            # return what child returned
            raise RuntimeError("Not supported yet")

        else:
            # empty - we are done
            return self._parent


class Menu(AbstractMenuItem):
    def parseLine(self, line):
        pass


class MenuItem(AbstractMenuItem):
    def parseLine(self, line):
        pass


class SubmenuItem(AbstractMenuItem):
    def parseLine(self, line):
        pass


class MenuParser(object):
    def __init__(self):
        self.buffer = None  # buffer to parse
        self.root_item = None  # root element
        self.current_item = None  # currently parsed element

    @staticmethod
    def parseLink(line):
        """String with link or Null"""
        link = None
        rg_line = line.split("|", 1)
        if len(rg_line) > 1:
            link = rg_line[1]

        return link

    def parse_line(self, line):
        self.current_item = self.current_item.parseLine(line)

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

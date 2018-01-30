import re

class MenuHtmlTemplates(object):

    TMenuRootButton = "\
        <div class='container'>\
            <p/>\
            <div class='dropdown'>\
                <button class='btn btn-default dropdown-toggle' data-toggle='dropdown' type='button'>%(name)s<span class='caret'/></button>\
                <ul class='dropdown-menu'>\
                %(stuffing)s\
                </ul>\
            </div>\
        </div>" # name, stuffing

    TMenuHeaderItem = "\
        <li><a href='%(link)s' tabindex='-1'>%(name)s</a></li>\
        <div class='divider'></div>" #link, name

    TMenuItem = "<li><a href='%(link)s' tabindex='-1'>%(name)s</a></li>" #link, name

    TSubmenuItem = "" \
         "<li class='dropdown-submenu'>\
            <a class='submenu-title' href='#' tabindex='-1'>%(name)s<span class='caret'/></a>\
            <ul class='dropdown-menu'>%(stuffing)s</ul>\
         </li>" #name, stuffing

class AbstractMenuItem(object):
    def __init__(self, parent):
        self._parent = parent
        self._rg_child = []
        self._name = ""
        self._link = ""

    def parseLine(self, line):
        """
        :param line: input data
        :return: entity to handle next input (self, child or None)
        """
        raise NotImplementedError("Not implemented")

    def parseMyself(self, line):
        raise NotImplementedError("Not implemented")

    def html(self):
        raise NotImplementedError("Not implemented")

class MenuRootButton(AbstractMenuItem):
    def parseMyself(self, line):
        self._name = line

    def html(self):

        stuffing = ""
        for child in self._rg_child:
            stuffing += child.html()

        html = MenuHtmlTemplates.TMenuRootButton % { "name" : self._name, "stuffing" :  stuffing }

        return html

    def parseLine(self, line):
        """
        :param line: parse data
        :return: return object to receive next input (child, parent or self)
        """

        root_button_initialized = self._name
        if not root_button_initialized:
            # my
            link = MenuParser.parseLink(line)
            if link or link == "":
                raise RuntimeError("Can't parse this:" + line)

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
        self._name = line.split('|')[0]
        self._link = line.split('|')[1]

    def html(self):

        stuffing = ""
        for child in self._rg_child:
            stuffing += child.html()

        html = MenuHtmlTemplates.TMenuHeaderItem % { "name" : self._name, "link" :  self._link }

        return html

    def parseLine(self, line):
        self.parseMyself(line)
        return self._parent


class MenuItem(AbstractMenuItem):
    def parseMyself(self, line):
        self._name = line.split('|')[0]
        self._link = line.split('|')[1]


    def html(self):

        stuffing = ""
        for child in self._rg_child:
            stuffing += child.html()

        html = MenuHtmlTemplates.TMenuItem % { "name" : self._name, "link" :  self._link }

        return html

    def parseLine(self, line):

        if MenuParser.parseLink(line):
            self.parseMyself(line)
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
        self._name = line


    def html(self):

        stuffing = ""
        for child in self._rg_child:
            stuffing += child.html()

        html = MenuHtmlTemplates.TSubmenuItem % { "name" : self._name, "stuffing" :  stuffing }

        return html

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
        for line in buffer.splitlines():
            print "LINE:" + line
            self.parseLine(line)

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

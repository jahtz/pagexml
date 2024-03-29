from typing import Self

from lxml import etree

from .types import XMLElement
from .element import Element


class Page:
    def __init__(self, attributes: dict):
        self._attributes: dict = attributes
        self._ro: list[str] = []  # reading order by region id's
        self._elements: list[Element] = []

    @classmethod
    def new(cls, **attributes: dict):
        """ Create a new Page object from scratch """
        return cls(attributes)

    @classmethod
    def from_etree(cls, tree: etree.Element) -> Self:
        """ Create a new Page object from a xml etree element """
        page = cls(dict(tree.items()))

        # reading order
        ro = tree.find('./{*}ReadingOrder')
        if ro is not None:
            ro_elements = tree.findall('../{*}RegionRefIndexed')
            if ro_elements is not None:
                sorted_ro = sorted(list(ro_elements), key=lambda i: i.get('index'))
                page._ro = list([i.get('regionRef') for i in sorted_ro])
            tree.remove(ro)

        # elements
        for element in tree:
            page.add_element(Element.from_etree(element))
        return page

    def to_etree(self) -> etree.Element:
        """ Convert the Page object to a xml etree element """
        # create page element
        page = etree.Element('Page', **self._attributes)

        # create reading order element
        reading_order = etree.SubElement(page, 'ReadingOrder')
        order_group = etree.SubElement(reading_order, 'OrderedGroup', id='g0')  # does id matter?
        for i, rid in enumerate(self._ro):
            etree.SubElement(order_group, 'RegionRefIndexed', index=str(i), regionRef=rid)

        # add elements
        for element in self._elements:
            page.append(element.to_etree())

        return page

    @property
    def attributes(self) -> dict:
        return self._attributes

    @property
    def elements(self) -> list[Element]:
        """ List of elements """
        return self.elements

    def set_attribute(self, key: str, value: str):
        """ Set an attribute """
        self._attributes[key] = value

    def remove_attribute(self, key: str):
        """ Remove an attribute """
        self._attributes.pop(key, None)

    def add_element(self, element: Element, index: int | None = None, reading_order: bool = True):
        """ Add an element to the elements list. """
        if index is None:
            self._elements.append(element)
            if element.is_region and reading_order:
                self._ro.append(element.attributes['id'])
        else:
            self._elements.insert(index, element)
            if element.is_region and reading_order:
                self._ro.insert(index, element.attributes['id'])

    def create_element(self, etype: XMLElement, index: int = None, **attributes: dict) -> Element:
        """ Create a new element and add it to the elements list """
        element = Element.new(etype, **attributes)
        self.add_element(element, index)
        return element

    def remove_element(self, element: Element):
        """ Remove an element from the elements list """
        self._elements.remove(element)

    def remove_element_by_index(self, index: int) -> Element:
        """ Remove an element from the elements list by its index """
        return self._elements.pop(index)

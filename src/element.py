from typing import Self

from lxml import etree

from .types import ElementType


class Element:
    def __init__(self, etype: ElementType, attributes: dict):
        self._etype: ElementType = etype
        self._attributes: dict = attributes
        self._elements: list[Element] = []
        self._text: str | None = None

    @classmethod
    def new(cls, etype: ElementType, **attributes: dict):
        """ Create a new Element object from scratch """
        return cls(etype, attributes)

    @classmethod
    def from_etree(cls, tree: etree.Element) -> Self:
        """ Create a new Element object from a xml etree element """
        element = cls(ElementType(tree.tag.split('}')[1]), dict(tree.items()))
        element.text = tree.text
        for child in tree:
            element.add_element(Element.from_etree(child))
        return element

    def to_etree(self) -> etree.Element:
        """ Convert the Element object to a xml etree element """
        # create element
        element = etree.Element(self._etype.value, **self._attributes)
        if self._text is not None:
            element.text = self._text

        # add elements
        for child in self._elements:
            element.append(child.to_etree())

        return element

    @property
    def etype(self) -> ElementType:
        """ Element type """
        return self._etype

    @property
    def attributes(self) -> dict:
        """ Element attributes """
        return self._attributes

    @property
    def text(self) -> str | None:
        """ Element text """
        return self._text

    @text.setter
    def text(self, value: str):
        """ Set the element text """
        self._text = value

    @property
    def elements(self) -> list[Self]:
        """ List of elements """
        return self.elements

    def is_region(self) -> bool:
        """ Check if the element is a region """
        return self._etype.value.contains('Region')

    def contains_text(self) -> bool:
        """ Check if the element contains text """
        return self._text is not None

    def set_attribute(self, key: str, value: str):
        """ Set an attribute """
        self._attributes[key] = value

    def remove_attribute(self, key: str):
        """ Remove an attribute """
        self._attributes.pop(key, None)

    def add_element(self, element: Self, index: int | None = None):
        """ Add an element to the elements list. """
        if index is None:
            self._elements.append(element)
        else:
            self._elements.insert(index, element)

    def create_element(self, etype: ElementType, index: int = None, **attributes: dict) -> Self:
        """ Create a new element and add it to the elements list """
        element = Element.new(etype, **attributes)
        self.add_element(element, index)
        return element

    def remove_element_by_index(self, index: int) -> Self:
        """ Remove an element from the elements list by its index """
        return self._elements.pop(index)


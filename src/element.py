# Copyright 2024 Janik Haitz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Self, Optional, Union

from lxml import etree

from .types import XMLType


class Element:
    def __init__(self, xmltype: XMLType, attributes: Optional[dict[str, str]] = None):
        self._xmltype: XMLType = xmltype
        self._attributes: dict[str, str] = {} if attributes is None else attributes
        self._elements: list[Element] = []
        self._text: Optional[str] = None

    def __len__(self) -> int:
        """ Return the number of elements """
        return len(self._elements)

    def __iter__(self) -> Self:
        """ Iterate through the list of elements """
        self.__n = 0
        return self

    def __next__(self) -> Self:
        """ Iterate through the list of elements """
        if self.__n < len(self._elements):
            element = self._elements[self.__n]
            self.__n += 1
            return element
        else:
            raise StopIteration

    def __getitem__(self, key: Union[int, str]) -> Optional[Union[Self, str]]:
        """ Get attribute or element with brackets operator """
        if isinstance(key, int) and key < len(self._elements):
            return self._elements[key]
        elif isinstance(key, str) and key in self._attributes:
            return self._attributes[key]
        return None

    def __setitem__(self, key: Union[int, str], value: Union[Self, str]) -> None:
        """ Set attribute or element with brackets operator """
        if isinstance(key, int) and isinstance(value, Element) and key < len(self._elements):
            self._elements[key] = value
        elif isinstance(key, str) and isinstance(value, str):
            self._attributes[str(key)] = str(value)

    def __contains__(self, key: Union[Self, str]) -> bool:
        """ Check if attribute or element exists """
        if isinstance(key, str):
            return key in self._attributes
        elif isinstance(key, Element):
            return key in self._elements
        return False

    @classmethod
    def new(cls, xmltype: XMLType, **attributes: str) -> Self:
        """ Create a new Element object from scratch """
        attributes = {str(k): str(v) for k, v in attributes.items() if v is not None}
        return cls(xmltype, attributes)

    @classmethod
    def from_etree(cls, tree: etree.Element) -> Self:
        """ Create a new Element object from a xml etree element """
        element = cls(XMLType(tree.tag.split('}')[1]), dict(tree.items()))
        element.text = tree.text
        for child in tree:
            element.add_element(Element.from_etree(child))
        return element

    def to_etree(self) -> etree.Element:
        """ Convert the Element object to a xml etree element """
        # create element
        element = etree.Element(self._xmltype.value, **self._attributes)
        if self._text is not None:
            element.text = self._text
        # add elements
        for child in self._elements:
            element.append(child.to_etree())
        return element

    @property
    def xmltype(self) -> XMLType:
        """ Get the type of the element """
        return self._xmltype

    @property
    def attributes(self) -> dict[str, str]:
        """ Get the elements attributes """
        return self._attributes

    @property
    def id(self) -> Optional[str]:
        """ Get the element id """
        return self._attributes.get('id', None)

    @id.setter
    def id(self, _id: Optional[str]) -> None:
        self._attributes['id'] = _id

    @property
    def type(self) -> Optional[str]:
        """ Get the element type """
        return self._attributes.get('id', None)

    @type.setter
    def type(self, _type: Optional[str]) -> None:
        """ Set the element type """
        self._attributes['_type'] = _type

    @property
    def text(self) -> Optional[str]:
        """ Get text of the element """
        return self._text

    @text.setter
    def text(self, value: Optional[str]) -> None:
        """ Set the element text """
        self._text = value

    @property
    def elements(self) -> list[Self]:
        """ Get the list of elements """
        return self._elements

    def is_region(self) -> bool:
        """ Check if the element is a region """
        return 'Region' in self._xmltype.value

    def contains_text(self) -> bool:
        """ Check if the element contains any text """
        return self._text is not None

    def set_attribute(self, key: str, value: str) -> None:
        """ Set an attribute """
        self._attributes[key] = value

    def delete_attribute(self, key: str) -> None:
        """ Delete an attribute """
        self._attributes.pop(key, None)

    def add_element(self, element: Self, index: Optional[int] = None) -> None:
        """ Add an element to the elements list. """
        if index is None:
            self._elements.append(element)
        else:
            self._elements.insert(index, element)

    def create_element(self, xmltype: XMLType, index: Optional[int] = None, **attributes: str) -> Self:
        """ Create a new element and add it to the elements list """
        element = Element.new(xmltype, **attributes)
        self.add_element(element, index)
        return element

    def remove_element(self, element: Union[int, Self]) -> Optional[Self]:
        """ Remove an element from the elements list """
        if isinstance(element, int) and element < len(self._elements):
            return self._elements.pop(element)
        elif isinstance(element, Element) and element in self._elements:
            self._elements.remove(element)
            return element
        return None

    def get_coords(self) -> Optional[Self]:
        """ Returns the first Coords element. None if nothing found """
        for element in self._elements:
            if element.xmltype == XMLType.Coords:
                return element
        return None

    def get_baseline(self) -> Optional[Self]:
        """ Returns the first Baseline element. None if nothing found """
        for element in self._elements:
            if element.xmltype == XMLType.Baseline:
                return element
        return None

    def clear(self):
        """ Remove all elements """
        self._elements.clear()

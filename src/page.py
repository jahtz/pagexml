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
from .element import Element


class Page:
    def __init__(self, attributes: Optional[dict[str, str]] = None):
        self._attributes: dict[str, str] = {} if attributes is None else attributes
        self._ro: list[str] = []  # reading order by region id's
        self._elements: list[Element] = []

    def __len__(self) -> int:
        """ Return the number of elements """
        return len(self._elements)

    def __iter__(self) -> Self:
        """ Iterate through the list of elements """
        self.__n = 0
        return self

    def __next__(self) -> Element:
        """ Iterate through the list of elements """
        if self.__n < len(self._elements):
            element = self._elements[self.__n]
            self.__n += 1
            return element
        else:
            raise StopIteration

    def __getitem__(self, key: Union[str, int]) -> Optional[Union[Element, str]]:
        """ Get attribute or element with brackets operator """
        if isinstance(key, int) and len(self._elements) > 0:
            return self._elements[min(key, len(self._elements)-1)]
        elif isinstance(key, str) and key in self._attributes:
            return self._attributes[key]
        return None

    def __setitem__(self, key: Union[str, int], value: Union[Element, str]) -> None:
        """ Set attribute or element with brackets operator """
        if isinstance(key, int) and isinstance(value, Element) and len(self._elements) > 0:
            self._elements[min(key, len(self._elements)-1)] = value
        elif isinstance(key, str):
            self._attributes[key] = str(value)

    def __contains__(self, key: Union[Element, str]) -> bool:
        """ Check if attribute or element exists """
        if isinstance(key, str):
            return key in self._attributes
        elif isinstance(key, Element):
            return key in self._elements
        return False

    @classmethod
    def new(cls, **attributes: str):
        """ Create a new Page object from scratch """
        attributes = {str(k): str(v) for k, v in attributes.items() if v is not None}
        return cls(attributes)

    @classmethod
    def from_etree(cls, tree: etree.Element) -> Self:
        """ Create a new Page object from a xml etree element """
        page = cls(dict(tree.items()))
        # reading order
        if (ro := tree.find('./{*}ReadingOrder')) is not None:
            if (ro_elements := tree.findall('../{*}RegionRefIndexed')) is not None:
                page._ro = list([i.get('regionRef') for i in sorted(list(ro_elements), key=lambda i: i.get('index'))])
            tree.remove(ro)
        # elements
        for element in tree:
            page.add_element(Element.from_etree(element), reading_order=False)
        return page

    def to_etree(self) -> etree.Element:
        """ Convert the Page object to a xml etree element """
        # create page element
        page = etree.Element('Page', **self._attributes)
        # create reading order element
        if len(self._ro) > 0:
            reading_order = etree.SubElement(page, 'ReadingOrder')
            order_group = etree.SubElement(reading_order, 'OrderedGroup', id='g0')  # does id matter?
            for i, rid in enumerate(self._ro):
                etree.SubElement(order_group, 'RegionRefIndexed', index=str(i), regionRef=rid)
        # add elements
        for element in self._elements:
            page.append(element.to_etree())
        return page

    @property
    def attributes(self) -> dict[str, str]:
        """ Get the elements attributes """
        return self._attributes

    @property
    def elements(self) -> list[Self]:
        """ Get the list of elements """
        return self._elements

    @property
    def reading_order(self) -> list[str]:
        """ List of region id's in reading order """
        return self._ro

    @property
    def image_filename(self) -> Optional[str]:
        """ Get the image filename """
        return self._attributes.get('imageFilename', None)

    @image_filename.setter
    def image_filename(self, filename: str) -> None:
        """ Set the image filename """
        if filename is None:
            self._attributes.pop('imageFilename', None)
        else:
            self._attributes['imageFilename'] = str(filename)

    @property
    def image_width(self) -> Optional[int]:
        """ Get the image width """
        if (width := self._attributes.get('imageWidth', None)) is not None:
            return int(width)
        else:
            return None

    @image_width.setter
    def image_width(self, image_width: Union[int, str]) -> None:
        """ Set the image width """
        if image_width is None:
            self._attributes.pop('imageWidth', None)
        else:
            self._attributes['imageWidth'] = str(image_width)

    @property
    def image_height(self) -> Optional[int]:
        """ Get the image width """
        if (width := self._attributes.get('imageHeight', None)) is not None:
            return int(width)
        else:
            return None

    @image_height.setter
    def image_height(self, image_height: Union[int, str]) -> None:
        """ Set the image height """
        if image_height is None:
            self._attributes.pop('imageHeight', None)
        else:
            self._attributes['imageHeight'] = str(image_height)

    @reading_order.setter
    def reading_order(self, reading_order: list[str]) -> None:
        """ Set the reading order """
        self._ro = reading_order

    def set_attribute(self, key: str, value: Optional[str]) -> None:
        """ Set an attribute """
        if value is None:
            self._attributes.pop(str(key), None)
        else:
            self._attributes[str(key)] = str(key)

    def delete_attribute(self, key: str) -> None:
        """ Delete an attribute """
        self._attributes.pop(str(key), None)

    def add_element(self, element: Element, index: Optional[int] = None, reading_order: bool = True) -> None:
        """ Add an element to the elements list. """
        if index is None:
            self._elements.append(element)
            if element.is_region and reading_order and 'id' in element:
                self._ro.append(element.attributes['id'])
        else:
            self._elements.insert(index, element)
            if element.is_region and reading_order and 'id' in element:
                self._ro.insert(index, element.attributes['id'])

    def create_element(self, xmltype: XMLType, index: int = None, **attributes: str) -> Element:
        """ Create a new element and add it to the elements list """
        element = Element.new(xmltype, **attributes)
        self.add_element(element, index)
        return element

    def remove_element(self, element: Union[int, Element]) -> Optional[Element]:
        """ Remove an element from the elements list """
        if isinstance(element, int) and element < len(self._elements):
            return self._elements.pop(element)
        elif isinstance(element, Element) and element in self._elements:
            self._elements.remove(element)
            return element
        return None

    def get_regions(self, xmltype: Optional[XMLType] = None) -> list[Element]:
        """ Returns a list of all region elements that are direct children """
        if xmltype is None:
            return list([e for e in self._elements if e.is_region()])
        return list([e for e in self._elements if e.is_region() and e.xmltype == xmltype])

    def clear(self):
        """ Remove all elements """
        self._elements.clear()

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
from pathlib import Path
from datetime import datetime

from lxml import etree

from .page import Page


XMLNS = 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15'
XMLNS_XSI = 'http://www.w3.org/2001/XMLSchema-instance'
XSI_SCHEMA_LOCATION = 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15/pagecontent.xsd'


class PageXML:
    def __init__(self, creator: Optional[str] = None, created: Optional[str] = None, last_change: Optional[str] = None):
        self._creator: Optional[str] = creator
        self._created: Optional[str] = created
        self._last_change: Optional[str] = last_change
        self._pages: list = []

    def __len__(self) -> int:
        """ Return the number of pages """
        return len(self._pages)

    def __iter__(self) -> Self:
        """ Iterate through the list of pages """
        self.__n = 0
        return self

    def __next__(self) -> Page:
        """ Iterate through the list of pages """
        if self.__n < len(self._pages):
            page = self._pages[self.__n]
            self.__n += 1
            return page
        else:
            raise StopIteration

    def __getitem__(self, key: int) -> Page | None:
        """ Get page with brackets operator """
        if len(self._pages) > 0:
            return self._pages[min(key, len(self._pages)-1)]
        return None

    def __setitem__(self, key: int, value: Page):
        """ Set page with brackets operator """
        if len(self._pages) > 0:
            self._pages[min(key, len(self._pages)-1)] = value

    def __contains__(self, key: Page) -> bool:
        """ Check if page exists """
        if isinstance(key, Page):
            return key in self._pages
        return False

    @classmethod
    def new(cls, creator: str = 'PageXML by jahtz'):
        """ Create a new PageXML object from scratch """
        return cls(creator, datetime.now().isoformat(), datetime.now().isoformat())


    @classmethod
    def from_etree(cls, tree: etree.Element) -> Self:
        """ Create a new PageXML object from a xml etree element """
        # PageXML element with metadata
        if (md_tree := tree.find('./{*}Metadata')) is not None:
            if (creator := md_tree.find('./{*}Creator')) is not None:
                creator = creator.text
            if (created := md_tree.find('./{*}Created')) is not None:
                created = created.text
            if (last_change := md_tree.find('./{*}LastChange')) is not None:
                last_change = last_change.text
            pxml = cls(creator, created, last_change)
        else:
            pxml = cls.new()
        # page elements
        if (pages := tree.findall('./{*}Page')) is not None:
            for page_tree in pages:
                pxml.add_page(Page.from_etree(page_tree))
        return pxml

    @classmethod
    def from_xml(cls, fp: Union[Path, str]) -> Self:
        """ Create a new PageXML object from a xml string """
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(fp, parser).getroot()
        return cls.from_etree(tree)


    def to_etree(self):
        """ Convert the PageXML object to a xml etree element """
        self.change()
        # create root element
        xsi_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", 'schemaLocation')
        nsmap = {None: XMLNS, 'xsi': XMLNS_XSI}
        root = etree.Element('PcGts', {xsi_qname: XSI_SCHEMA_LOCATION}, nsmap=nsmap)
        # create metadata element
        metadata = etree.SubElement(root, 'Metadata')
        etree.SubElement(metadata, 'Creator').text = self._creator
        etree.SubElement(metadata, 'Created').text = self._created
        etree.SubElement(metadata, 'LastChange').text = self._last_change
        # create page elements
        for page in self._pages:
            root.append(page.to_etree())
        return root

    def to_xml(self, fp: Union[Path, str]):
        """ Write the PageXML object to a file """
        with open(fp, 'wb') as f:
            f.write(etree.tostring(self.to_etree(), pretty_print=True, encoding='utf-8', xml_declaration=True))

    @property
    def creator(self) -> str:
        """ Creator of the PageXML file """
        return self._creator

    @creator.setter
    def creator(self, creator: str) -> None:
        """ Set the creator of the PageXML file """
        self._creator = str(creator)

    @property
    def created(self) -> str:
        """ Date and time of the creation of the PageXML file (ISO format)"""
        return self._created

    @created.setter
    def created(self, created: Union[str, datetime]) -> None:
        """ Set the date and time of the creation of the PageXML file (ISO format)"""
        if isinstance(created, datetime):
            self._created = created.isoformat()
        else:
            self._created = created

    @property
    def last_change(self) -> str:
        """ Date and time of the last change of the PageXML file (ISO format)"""
        return self._last_change

    @last_change.setter
    def last_change(self, last_change: Union[str, datetime]) -> None:
        """ Set the date and time of the last change of the PageXML file (ISO format)"""
        if isinstance(last_change, datetime):
            self._last_change = last_change.isoformat()
        else:
            self._last_change = last_change

    def change(self) -> None:
        """ Update the last_change attribute to the current time """
        self._last_change = datetime.now().isoformat()

    @property
    def pages(self) -> list[Page]:
        """ List of pages """
        return self._pages

    def add_page(self, page: Page, index: Optional[int] = None) -> None:
        """ Add a page to the pages list """
        if index is None:
            self._pages.append(page)
        else:
            self._pages.insert(index, page)

    def create_page(self, index: Optional[int] = None, **attributes: str) -> Page:
        """ Create a new page and add it to the pages list """
        page = Page.new(**attributes)
        self.add_page(page, index)
        return page

    def remove_page(self, page: Union[Page, int]) -> Optional[Page]:
        """ Remove a page from the pages list """
        if isinstance(page, int) and page < len(self._pages):
            return self._pages.pop(page)
        elif isinstance(page, Page) and page in self._pages:
            self._pages.remove(page)
            return page
        return None

    def clear(self):
        """ Remove all pages """
        self._pages.clear()

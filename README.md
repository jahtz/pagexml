# pagexml
Python package for working with PageXML files.

## Installation
```bash
git clone https://github.com/jatzelberger/pagexml.git
pip3 install -r ./pagexml/requirements.txt
```

## Usage
```python
from pagexml import PageXML, Page, Element, ElementType

# Create new PageXML object
pxml = PageXML.new('some creator')

# Load PageXML object from file
pxml = PageXML.from_xml('path/to/file.xml')

# Load PageXML object from lxml.etree object
pxml = PageXML.from_etree(etree)


# Create new Page
page = pxml.create_page(imageFilename='image.jpg', width=1000, height=1000)

# Manipulate Page attributes
page.set_attribute('imageFilename', 'new_image.jpg')

# Add element (Region,...)
# with create_element method on parent
region = page.create_element(ElementType.TextRegion, id='r1', more_attrs='attribute', ...)
# or Element constructor
attributes = {"id": "l1", "more_attrs": "attribute", ...}
element = Element.new(ElementType.TextLine, **attributes)
element.text = "Hello, World!"
region.add_element(element)
#...

# Convert PageXML object to lxml.etree object
tree = pxml.to_etree()

# Write PageXML object to file
pxml.to_xml('path/to/file.xml')
```

## ZPD
Developed at Centre for [Philology and Digitality](https://www.uni-wuerzburg.de/en/zpd/) (ZPD), [University of Würzburg](https://www.uni-wuerzburg.de/en/).
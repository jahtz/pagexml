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
# or
page2 = Page.new(**{'imageFilename': 'image.jpg', 'width': 1000, 'height': 1000})
pxml.add_page(page2)

# Create new Region or Element 
region = page.create_element(ElementType.TextRegion, **{'id': 'r1', 'more_attrs':'attribute', ...})
# or
line = Element.new(ElementType.TextLine, id='l1')
region.add_element(line)
# Regions will automatically be appended to ReadingOrder
# prevent with 'reading_order=False' argument

# add text to an Element
line.text = 'Hello World!'
# or remove it
line.text = None

# Manipulate or add Page or Element attributes
page.set_attribute('imageFilename', 'new_image.jpg')
# or
page['imageFilename'] = 'new_image.jpg'

# Remove attribute
del page.attributes['key']
# or
page.attributes.pop('key', None)  # prevents KeyError

# Iterate over Pages, Regions or Elements
for page in pxml:
    print(len(page))  # print number of Regions and Elements

# Convert PageXML object to lxml.etree object
tree = pxml.to_etree()

# Write PageXML object to file
pxml.to_xml('path/to/file.xml')
```

## ZPD
Developed at Centre for [Philology and Digitality](https://www.uni-wuerzburg.de/en/zpd/) (ZPD), [University of Würzburg](https://www.uni-wuerzburg.de/en/).
from src.types import XMLType

# pagexml
Python package for working with PageXML files.

## Installation
```bash
git clone https://github.com/jahtz/pagexml.git
pip3 install -r ./pagexml/requirements.txt
```

## Usage
#### Required imports
```python
from pagexml import PageXML, Page, Element, XMLType
```
#### Create a PageXML object
```python
# Method 1: Create a new PageXML
pxml = PageXML.new('yourname')

# Method 2: Load a PageXML file
pxml = PageXML.from_xml('path/to/file.xml')

# Method 3: Load a lxml etree:
pxml = PageXML.from_etree(etree)
```

#### Pages
```python
# Create a new Page and add it to the PageXML object (attributes are passed as named arguments):
page1 = pxml.create_page(imageFilename='image.jpg', imageWidth=1000, imageHeight=1000, ...)

# Create a new Page
page2 = Page.new(imageFilename='image.jpg', imageWidth=1000, imageHeight=1000, ...)
pxml.add_page(page2)  # add manually

# Get all regions
regions = page3.get_regions()

# Get all regions of a specific type:
regions = page3.get_regions(xmltype=XMLType.TextRegion)

# Get a regions (or child element by index):
child = page3[0]

# Loop over childs:
for child in page:
    ...

# Access attributes
print(child['someAttribute'])
child['someAttribute'] = 'newValue'
```

#### Elements
```python
# Create a new Region or child Element (alternative to new() method)
textregion = page1.create_element(XMLType.TextRegion, id='r1', ...)
textline = textregion.create_element(XMLTYPE.TextLine, id='l1', ...)

# set text:
textline.text = 'hello world'

# get Coords element
textline.get_coords()

# get Baseline element
textline.get_baseline()
```

#### Output PageXML object
```python
# Method 1: Convert PageXML object to lxml.etree object
tree = pxml.to_etree()

# Method 2: Write PageXML object to file
pxml.to_xml('path/to/file.xml')
```

## ZPD
Developed at Centre for [Philology and Digitality](https://www.uni-wuerzburg.de/en/zpd/) (ZPD), [University of Würzburg](https://www.uni-wuerzburg.de/en/).

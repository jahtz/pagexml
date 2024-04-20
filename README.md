# pagexml
Python package for working with PageXML files.

## Installation
```bash
git clone https://github.com/jahtz/pagexml.git
pip3 install -r ./pagexml/requirements.txt
```

## Usage
```python
from pagexml import PageXML, Page, Element, ElementType

# Create a PageXMl object
pxml = PageXML.new('your name or institution')  # new PageXML without any content
pxml = PageXML.from_xml('path/to/file.xml')  # load PageXML from file
pxml = PageXML.from_etree(etree)  # load PageXML from lxml.etree object

# Pages
page1 = pxml.create_page(imageFilename='image.jpg', width=1000, height=1000, ...)  # create a new Page
page2 = Page.new(**{'imageFilename': 'image.jpg', 'width': 1000, 'height': 1000, ...})  # create a new Page (without directly adding it to a PageXML object)
pxml.add_page(page2)  # add a Page to the PageXML object manually


# Regions and Elements (Regions and Elements interchangeable)
region = page1.create_element(ElementType.TextRegion, **{'id': 'r1', 'more_attrs':'attribute', ...})  # create a new Region, automatically added to ReadingOrder. Prevent with 'reading_order=False' argument
line = Element.new(ElementType.TextLine, id='l1')  # create a new Element (without directly adding it to a Region object)
region.add_element(line)  # add an Element to a Region object manually

# Access data
line.text = 'Hello World!'  # add text to an Element
line.text = None  # remove text from an Element

page1.set_attribute('imageFilename', 'new_image.jpg')  # set an attribute
page1['imageFilename'] = 'new_image.jpg'  # same as above

del page1.attributes['imageFilename']  # remove an attribute
page1.attributes.pop('imageFilename', None)  # same as above (prevents KeyError)

region_at_0 = page1[0]  # access Pages, Regions and Elements by index

for page in pxml:  # iterate over Pages
    print(len(page))  # print number of Regions and Elements

print('imageFilename' in page1)  # check for attribute
print(region in page1)  # check for Region or Element

# Convert PageXML object to lxml.etree object
tree = pxml.to_etree()

# Write PageXML object to file
pxml.to_xml('path/to/file.xml')
```

## ZPD
Developed at Centre for [Philology and Digitality](https://www.uni-wuerzburg.de/en/zpd/) (ZPD), [University of Würzburg](https://www.uni-wuerzburg.de/en/).

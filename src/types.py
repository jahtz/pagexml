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

from enum import Enum


class XMLType(Enum):
    """
    https://ocr-d.de/de/gt-guidelines/pagexml/pagecontent_xsd_Complex_Type_pc_PcGtsType.html#PcGtsType_Page
    """

    # ReadingOrder
    ReadingOrder = "ReadingOrder"
    OrderedGroup = "OrderedGroup"
    RegionRefIndexed = "RegionRefIndexed"

    # Regions
    AdvertRegion = "AdvertRegion"
    ChartRegion = "ChartRegion"
    ChemRegion = "ChemRegion"
    CustomRegion = "CustomRegion"
    GraphicRegion = "GraphicRegion"
    ImageRegion = "ImageRegion"
    LineDrawingRegion = "LineDrawingRegion"
    MapRegion = "MapRegion"
    MathsRegion = "MathsRegion"
    MusicRegion = "MusicRegion"
    NoiseRegion = "NoiseRegion"
    SeparatorRegion = "SeparatorRegion"
    TableRegion = "TableRegion"
    TextRegion = "TextRegion"
    UnknownRegion = "UnknownRegion"

    # Elements
    AlternativeImage = "AlternativeImage"
    Baseline = "Baseline"
    Border = "Border"
    Coords = "Coords"
    Glyph = "Glyph"
    GraphemeGroup = "GraphemeGroup"
    Graphemes = "Graphemes"
    Grid = "Grid"
    Label = "Label"
    Labels = "Labels"
    Layers = "Layers"
    Metadata = "Metadata"
    NonPrintingChar = "NonPrintingChar"
    PlainText = "PlainText"
    PrintSpace = "PrintSpace"
    Relations = "Relations"
    Roles = "Roles"
    TextEquiv = "TextEquiv"
    TextLine = "TextLine"
    TextStyle = "TextStyle"
    Unicode = "Unicode"
    UserAttribute = "UserAttribute"
    UserDefined = "UserDefined"
    Word = "Word"
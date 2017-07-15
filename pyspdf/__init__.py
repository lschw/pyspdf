# pyspdf - a small and simple pdf renderer based on pygtk
# Copyright (C) 2017 Lukas Schwarz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""a small and simple pdf renderer based on pygtk"""
from .error import RenderError
from .pdf import PDF
from .line import LineFormat, Line
from .text import TextFormat, Text
from .image import ImageFormat, Image
from .table import TableFormat, Table

__version__ = "1.0.0"
__all__ = ["RenderError", "PDF", "LineFormat", "Line", "TextFormat", "Text",
    "ImageFormat", "Image", "TableFormat", "Table"]

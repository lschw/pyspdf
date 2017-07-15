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

import copy
import gtk
import pango
import gobject
from error import RenderError

class TextFormat:
    """
    Definition of text format
    Parameters
    ----------
    font : font family
    size : font size
    style : font style "normal", "italic", "oblique"
    font_descr : pango.FontDescription object
    line_spacing : line spacing
    wrap : wrap mode, pango.WRAP_WORD, pango.WRAP_WORD_CHAR, pango.WRAP_CHAR
    justify : bool, whether to justify (true) or not (false)
    align : text align, pango.ALIGN_LEFT, pango.ALIGN_CENTER, pango.ALIGN_RIGHT
    color : font color
    width : maximum width of text, enables text wrapping
    
    """
    def __init__(self, font="Arial", size=10, style="", font_descr=None,
            line_spacing=1, wrap=pango.WRAP_WORD, justify=False,
            align=pango.ALIGN_LEFT, color="#000000", width=None):
        self.font = font
        self.size = size
        self.style = style
        self.font_descr = font_descr
        self.line_spacing = line_spacing
        self.wrap = wrap
        self.justify = justify
        self.align = align
        self.color = color
        self.width = width
    
    
    def __deepcopy__(self, memo):
        """
        Implemented because default deepcopy of pango.FontDescription fails
        """
        fmt = TextFormat()
        memo[id(self)] = fmt
        for k, v in self.__dict__.items():
            setattr(fmt, k, copy.deepcopy(v, memo))
        if self.font_descr:
            fmt.font_descr = pango.FontDescription(self.font_descr.__str__())
        return fmt


class Text:
    """
    Text item
    """
    
    def __init__(self, ctx, text, fmt):
        """
        Parameters
        ----------
        ctx : gtk.PrintContext
        fmt : TextFormat
        text : str
               text can be formatted with the Pango markup language, see
               https://developer.gnome.org/pango/stable/PangoMarkupFormat.html
        """
        self.ctx = ctx
        self.fmt = fmt
        self.text = text
        
        font_descr = self.fmt.font_descr
        if not font_descr:
            font_descr = pango.FontDescription("{} {} {}".format(
                self.fmt.font, self.fmt.style, self.fmt.size))
        self.layout = ctx.create_pango_layout()
        self.layout.set_font_description(font_descr)
        self.layout.set_alignment(self.fmt.align)
        self.layout.set_justify(self.fmt.justify)
        self.layout.set_spacing(self.fmt.line_spacing*pango.SCALE)
        self.layout.set_wrap(self.fmt.wrap)
        text = '<span foreground="{}">{}</span>'.format(self.fmt.color,
            self.text)
        if self.fmt.width:
            self.layout.set_width(int(self.fmt.width*pango.SCALE))
        try:
            attrs, markup_text, accel = pango.parse_markup(text)
            self.layout.set_attributes(attrs)
            self.layout.set_text(markup_text)
        except Exception as e:
            raise RenderError("PANGO_MARKUP_PARSE_ERROR", e.args[0], 
                gobject.markup_escape_text(self.text))
        
        self.w = self.layout.get_pixel_size()[0]
        self.h = self.layout.get_pixel_size()[1]
        self.lines = self.layout.get_line_count()
    
    
    def draw(self, x, y):
        """
        Parameters
        ----------
        x,y : float
            Absolute position to draw text
        """
        cctx = self.ctx.get_cairo_context()
        cctx.move_to(x, y)
        cctx.show_layout(self.layout)
    
    
    def split(self, max_height):
        """
        Split text into multiple texts in order to fit in given `max_height`
        
        Note: xml tags with whitespaces cause trouble
        
        Parameters
        ----------
        max_height : float, list<float>
            Maximum height of text. Can be a list of heights, so different 
            text parts can have different sizes. Last height will be repeated
            if required
        """
        if isinstance(max_height, float):
            max_height = [max_height]
        
        if self.h <= max_height[0]:
            return [copy.copy(self)]
        
        texts = []
        i_h = 0
        
        # create list of words
        # @todo handle xml tags while splitting for words
        # @todo handle newlines as word splitter
        words = self.text.split(" ")
        
        # loop through all words and create text blocks of such a length that
        # the resulting height is less than `max_height`
        while words:
            text_new = Text(self.ctx, words[0], self.fmt)
            i_w = 1
            while text_new.h < max_height[i_h] and i_w < len(words):
                text_new = Text(self.ctx, " ".join(words[:i_w]), self.fmt)
                i_w += 1
            
            # check whether line is full
            if i_w < len(words):
                text_new2 = Text(self.ctx, " ".join(words[:i_w+1]), self.fmt)
                lines1 = text_new.layout.get_line_count()
                lines2 = text_new2.layout.get_line_count()
                if lines1 == lines2:
                    # line is not full
                    # -> remove words until line count decreases
                    i_w2 = i_w-1
                    while lines2 == lines1:
                        if i_w2 == 0:
                            # first word reached -> revert
                            i_w2 = i_w1
                            break
                        text_new2 = Text(self.ctx, " ".join(words[:i_w2]), self.fmt)
                        lines2 = text_new2.layout.get_line_count()
                        i_w2 -= 1
                    i_w = i_w2
                
            text_new = Text(self.ctx, " ".join(words[:i_w]), self.fmt)
            texts.append(text_new)
            words = words[i_w:]
            if i_h+1 < len(max_height):
                i_h += 1
        
        return texts
        

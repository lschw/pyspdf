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

import gtk
import cairo
import math

class LineFormat:
    """
    Definition of line format
    """
    
    def __init__(self, width=0.1, style="solid", color="#000000", dl=None):
        """
        Parameters
        ----------
        width : float
        style : string ("solid", "double", "dotted", "dashed")
        color : string (rgb color in hex decimal representation)
        dl : None, float
            Can be used to set explicitly the distance between the lines of the
            "double" style
        """
        self.width = width
        self.style = style
        self.color = color
        self.dl = dl


class Line:
    """
    Line item
    """
    
    def __init__(self, ctx, dx=0, dy=0, fmt=LineFormat()):
        """
        Parameters
        ----------
        ctx : gtk.PrintContext
        fmt : LineFormat
        dx,dy : float
            Position of line end regarding render position
        """
        self.ctx = ctx
        self.fmt = fmt
        self.dx = dx
        self.dy = dy
    
    
    def draw(self, x, y):
        """
        Parameters
        ----------
        x,y : float
            Absolute start position of line
        """
        
        cctx = self.ctx.get_cairo_context()
        
        # save current cairo context to be able to reset it after the 
        # line rendering
        cctx.save()
        
        cctx.set_line_width(self.fmt.width)
        cctx.set_source_color(gtk.gdk.Color(self.fmt.color))
        if self.fmt.style == "double":
            # calculate position of double lines
            if self.fmt.dl:
                dl = self.fmt.dl
            else:
                # auto calculate a "good" distance depending on line width
                dl = self.fmt.width*(1.5-0.3*math.log(self.fmt.width))
            dlx = dl*self.dy/math.sqrt(self.dx**2 + self.dy**2)
            dly = dl*self.dx/math.sqrt(self.dx**2 + self.dy**2)
            
            cctx.move_to(x-dlx, y+dly)
            cctx.line_to(x+self.dx-dlx, y+self.dy+dly)
            cctx.stroke()
            cctx.move_to(x+dlx, y-dly)
            cctx.line_to(x+self.dx+dlx, y+self.dy-dly)
            cctx.stroke()
        else:
            if self.fmt.style == "dotted":
                # auto calculate a "good" distance depending on line width
                cctx.set_dash([0, self.fmt.width*(2+1./self.fmt.width)])
                cctx.set_line_cap(cairo.LINE_CAP_ROUND)
            elif self.fmt.style == "dashed":
                # auto calculate a "good" distance depending on line width
                cctx.set_dash([self.fmt.width*(2+1./self.fmt.width)])
            cctx.move_to(x, y)
            cctx.line_to(x+self.dx, y+self.dy)
            cctx.stroke()
        cctx.restore()

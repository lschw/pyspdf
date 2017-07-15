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
from error import RenderError

class ImageFormat:
    """
    Definition of image format
    """
    def __init__(self, width, height, center=False, dots_per_unit=20):
        """
        Parameters
        ----------
        width : width of image bounding box
        height : height of image bounding box
        center : whether to center image inside bounding box
        dots_per_unit : resolution of loaded image, how many dots per unit
        """
        self.width = width
        self.height = height
        self.center = center
        self.dots_per_unit = dots_per_unit
    

class Image:
    """
    Image item
    """
    
    def __init__(self, ctx, filename, fmt):
        """
        Parameters
        ----------
        ctx : gtk.PrintContext
        fmt : ImageFormat
        filename : str
        """
        self.ctx = ctx
        self.fmt = fmt
        self.filename = filename
        
        try:
            self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.filename,
                int(self.fmt.dots_per_unit*self.fmt.width),
                int(self.fmt.dots_per_unit*self.fmt.height))
        except Exception as e:
            raise RenderError("LOADING_IMAGE_FAILED", self.filename, e.args[0])
        
        self.pb_w = self.pixbuf.get_width()
        self.pb_h = self.pixbuf.get_height()
        self.scale_x = self.fmt.width/float(self.pb_w)
        self.scale_y = self.fmt.height/float(self.pb_h)
        self.scale_xy = min(self.scale_x, self.scale_y)
    
    
    def draw(self, x, y):
        """
        Parameters
        ----------
        x,y : float
            Absolute position of image to draw
        """
        cctx = self.ctx.get_cairo_context()
        cctx.save()
        
        if self.fmt.center:
            # center image inside bounding box
            x += (self.fmt.width-self.pb_w*self.scale_xy)/2
            y += (self.fmt.height-self.pb_h*self.scale_xy)/2
        
        # scale whole cairo context to preserve quality
        # x and y positions have to be scaled now as they are defined unscaled
        cctx.scale(self.scale_xy, self.scale_xy)
        pos_x = x/self.scale_xy
        pos_y = y/self.scale_xy
        
        cctx.rectangle(pos_x, pos_y, self.pb_w, self.pb_h)
        cctx.set_source_pixbuf(self.pixbuf, pos_x, pos_y)
        cctx.fill()
        cctx.restore()

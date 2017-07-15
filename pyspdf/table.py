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
from error import RenderError
from text import TextFormat, Text
from line import LineFormat, Line

class TableFormat:
    """
    Definition of table format
    """
    
    def __init__(self, cols):
        """
        Parameters
        ----------
        cols : [str,...]
            list of column names
        """
        self.cols = cols
        self.pad_l = 2 # cell padding left
        self.pad_r = 2 # cell padding right
        self.pad_t = 2 # cell padding top
        self.pad_b = 2 # cell padding bottom
        self.skip_pad_l = False
        self.skip_pad_r = False
        self.skip_pad_t = False
        self.skip_pad_b = False
        self.w_type = "auto"
        self.w = None # table width if `w_type` is "fixed"
        self.w_type_col = "auto"
        self.w_col = None # column width if `w_type_col` is fixed
        self.fmt_h = {col:TextFormat() for col in self.cols}
        self.fmt_b = {col:TextFormat() for col in self.cols}
        self.fmt_f = {col:TextFormat() for col in self.cols}
        self.hline_t = None # horizontal line top
        self.hline_m = None # horizontal line middle
        self.hline_b = None # horizontal line bottom
        self.hline_h = None # horizontal line between head and body
        self.hline_f = None # horizontal line between body and foot
        self.vline_l = None # vertical line left
        self.vline_m = None # vertical line middle
        self.vline_r = None # vertical line right
    
    
    def set_padding(self, pad, loc=None):
        """
        Set padding of cells
        
        Parameters
        ----------
        pad: float
        loc = None, "left", "right", "top", "bottom"
        """
        if isinstance(loc, str):
            loc = [loc]
        if loc == None or not isinstance(loc, list):
            loc = ["left", "right", "top", "bottom"]
        if "left" in loc: self.pad_l = pad
        if "right" in loc: self.pad_r = pad
        if "top" in loc: self.pad_t = pad
        if "bottom" in loc: self.pad_b = pad
    
    
    def set_skip_padding(self, skip, loc=None):
        """
        Set whether at table border the padding should be skipped
        
        Parameters
        ----------
        skip: True, False
        loc = None, "left", "right", "top", "bottom"
        """
        if isinstance(loc, str):
            loc = [loc]
        if loc == None or not isinstance(loc, list):
            loc = ["left", "right", "top", "bottom"]
        if "left" in loc: self.skip_pad_l = skip
        if "right" in loc: self.skip_pad_r = skip
        if "top" in loc: self.skip_pad_t = skip
        if "bottom" in loc: self.skip_pad_b = skip
    
    
    def set_width(self, width_type, width=None):
        """
        Set table width
        
        Parameters
        ----------
        width_type : "auto", "fixed"
        width : None, float
        """
        self.w_type = width_type
        self.w = width
    
    
    def set_col_width(self, width_type, width=None):
        """
        Set column width
        
        Parameters
        ----------
        width_type : "auto", "equal", "fixed"
        width : None, float
        """
        if self.w_type == "fixed" and width_type == "fixed":
            raise ValueError("Column width type can not be 'fixed' if table " +
                "width type is 'fixed'")
        self.w_type_col = width_type
        self.w_col = width
    
    
    def set_fmt(self, fmt):
        """
        Set cell format for all cells
        
        Parameters
        ----------
        fmt : TextFormat
        """
        for col in self.cols:
            self.fmt_h[col] = copy.deepcopy(fmt)
            self.fmt_b[col] = copy.deepcopy(fmt)
            self.fmt_f[col] = copy.deepcopy(fmt)
    
    
    def set_fmt_col(self, col, fmt, value=None):
        """
        Set format of all cells for given column
        OR
        Set format property of all cells for given column
        
        Parameters
        ----------
        col : str
        fmt : TextFormat / str
            Either a text format or the name of a text property
        value : None / mixed
        """
        if isinstance(fmt, str):
            setattr(self.fmt_h[col], fmt, value)
            setattr(self.fmt_b[col], fmt, value)
            setattr(self.fmt_f[col], fmt, value)
        else:
            self.fmt_h[col] = copy.deepcopy(fmt)
            self.fmt_b[col] = copy.deepcopy(fmt)
            self.fmt_f[col] = copy.deepcopy(fmt)
    
    
    def set_fmt_tpart(self, tpart, fmt, value=None):
        """
        Set format of all cells for given table part
        OR
        Set format property of all cells for given table part
        
        Parameters
        ----------
        tpart : "head", "body", "foot"
        fmt : TextFormat / str
            Either a text format or the name of a text property
        value : None / mixed
        """
        if isinstance(fmt, str):
            if tpart == "head":
                for col in self.cols:
                    setattr(self.fmt_h[col], fmt, value)
            if tpart == "body":
                for col in self.cols:
                    setattr(self.fmt_b[col], fmt, value)
            if tpart == "foot":
                for col in self.cols:
                    setattr(self.fmt_f[col], fmt, value)
        else:
            if tpart == "head":
                for col in self.cols:
                    self.fmt_h[col] = copy.deepcopy(fmt)
            if tpart == "body":
                for col in self.cols:
                    self.fmt_b[col] = copy.deepcopy(fmt)
            if tpart == "foot":
                for col in self.cols:
                    self.fmt_f[col] = copy.deepcopy(fmt)
    
    
    def set_hline(self, fmt, pos=None):
        """
        Set format of horizontal lines
        
        Parameters
        ----------
        fmt : LineFormat
        pos : None, list, "top", "middle", "bottom", "head", "foot", "bottom"
        """
        if isinstance(pos, str):
            pos = [pos]
        if pos == None or not isinstance(pos, list):
            pos = ["top", "middle", "bottom", "head", "foot"]
        if "top" in pos: self.hline_t = fmt
        if "middle" in pos: self.hline_m = fmt
        if "bottom" in pos: self.hline_b = fmt
        if "head" in pos: self.hline_h = fmt
        if "foot" in pos: self.hline_f = fmt
    
    
    def set_vline(self, fmt, pos=None):
        """
        Set format of vertical lines
        
        Parameters
        ----------
        fmt : LineFormat
        pos : None, list, "left", "middle", "right"
        """
        if isinstance(pos, str):
            pos = [pos]
        if pos == None or not isinstance(pos, list):
            pos = ["left", "middle", "right"]
        if "left" in pos: self.vline_l = fmt
        if "middle" in pos: self.vline_m = fmt
        if "right" in pos: self.vline_r = fmt


class Table:
    """
    Table item
    """
    
    def __init__(self, ctx, fmt, data_h=[], data_b=[], data_f=[]):
        """
        Parameters
        ----------
        ctx : gtk.PrintContext
        fmt : TableFormat
        data_h, data_b, data_f : [{col1:value1, col2:value2, ...}, ...]
            Table data (rows) of head, body and foot
        """
        self.ctx = ctx
        self.fmt = fmt
        self.cols = self.fmt.cols
        
        # total width and height of table (inclusive padding)
        self.w = 0
        self.h = 0
        
        # height of (head, body, foot) parts (inclusive padding)
        self.h_h = 0
        self.h_b = 0
        self.h_f = 0
        
        # width of columns (exclusive padding)
        self.w_cols = []
        
        # height of (head, body, foot) rows (exclusive padding)
        self.h_rows_h = []
        self.h_rows_b = []
        self.h_rows_f = []
        
        # cells (Text objects) of (head, body, foot) parts
        # format: [[cell1, cell2, ...], ...]
        self.cells_h = []
        self.cells_b = []
        self.cells_f = []
        
        
        # first rendering of cells without width restriction to get required
        # space. This is needed for some table format descriptions
        self.w_cols = None # (set to None for second rendering)
        if (self.fmt.w_type == "auto" and self.fmt.w_type_col == "equal") or \
                (self.fmt.w_type == "fixed" and self.fmt.w_type_col == "auto"):
            
            # render head, body and foot cells
            w_cols_h = self._render(data_h, self.fmt.fmt_h)[1]
            w_cols_b = self._render(data_b, self.fmt.fmt_b)[1]
            w_cols_f = self._render(data_f, self.fmt.fmt_f)[1]
            
            # required space of each column is the maximum out of the
            # head, body and foot columns
            self.w_cols = []
            for i in range(len(self.cols)):
                self.w_cols.append(max(w_cols_h[i], w_cols_b[i], w_cols_f[i]))
        
        
        # calculate correct column widths depending on table format and
        # required space from the first rendering
        
        # table total width is variable
        if self.fmt.w_type == "auto":
        
            # all columns should have the same width
            # (width of the broadest column)
            if self.fmt.w_type_col == "equal":
                self.w_cols = [max(self.w_cols)]*len(self.cols)
            
            # all columns should have the predefined fixed width
            elif self.fmt.w_type_col == "fixed":
                self.w_cols = [self.fmt.w_col]*len(self.cols)
        
        # table width is fixed
        elif self.fmt.w_type == "fixed":
            
            # calculate available space for columns. available space is table
            # width minus padding
            space_avail = self.fmt.w
            
            # subtract inter column padding
            space_avail -= (len(self.cols)-1)*(self.fmt.pad_l + self.fmt.pad_r)
            
            # subtract left and right padding
            if not self.fmt.skip_pad_l:
                space_avail -= self.fmt.pad_l
            if not self.fmt.skip_pad_t:
                space_avail -= self.fmt.pad_t
            
            # column widths are determined "intelligently".
            # wider columns get more space, smaller columns less space
            if self.fmt.w_type_col == "auto":
            
                # distribute available space proportional to required space
                # @todo ensure that column width gets not too small
                space_required = 0
                for i in range(len(self.cols)):
                    space_required += self.w_cols[i]
                for i in range(len(self.cols)):
                    self.w_cols[i] = space_avail * self.w_cols[i]/space_required
            
            # all columns should have the same width
            # (available space is distributed equally)
            if self.fmt.w_type_col == "equal":
                self.w_cols = [space_avail/len(self.cols)]*len(self.cols)
        
        
        # render cells with correct column widths
        self.cells_h, w_cols_head, self.h_rows_h = self._render(
            data_h, self.fmt.fmt_h, self.w_cols)
        self.cells_b, w_cols_body, self.h_rows_b = self._render(
            data_b, self.fmt.fmt_b, self.w_cols)
        self.cells_f, w_cols_foot, self.h_rows_f = self._render(
            data_f, self.fmt.fmt_f, self.w_cols)
        
        
        # calculate total table width
        self.w = self.fmt.w
        if self.fmt.w_type != "fixed":
            
            # sum up all column widths
            self.w = sum(self.w_cols)
            
            # add inter column padding
            self.w += (len(self.cols)-1)*(self.fmt.pad_l + self.fmt.pad_r)
            
            # add left and right padding
            if not self.fmt.skip_pad_l:
                self.w += self.fmt.pad_l
            if not self.fmt.skip_pad_t:
                self.w += self.fmt.pad_t
        
        # calculate height of head
        if len(self.cells_h) > 0:
            
            # sum up all row heights
            self.h_h = sum(self.h_rows_h)
            
            # add inter row padding
            self.h_h += (len(self.cells_h)-1)*(self.fmt.pad_t + self.fmt.pad_b)
            
            # add top and bottom padding
            if not self.fmt.skip_pad_t:
                self.h_h += self.fmt.pad_t
            if len(self.cells_b) != 0 or len(self.cells_f) != 0 or \
                    not self.fmt.skip_pad_b:
                self.h_h += self.fmt.pad_b
        
        # calculate height of body
        if len(self.cells_b) > 0:
            self.h_b = sum(self.h_rows_b)
            self.h_b += (len(self.cells_b)-1)*(self.fmt.pad_t + self.fmt.pad_b)
            if len(self.cells_h) != 0 or not self.fmt.skip_pad_t:
                self.h_b += self.fmt.pad_t
            if len(self.cells_f) != 0 or not self.fmt.skip_pad_b:
                self.h_b += self.fmt.pad_b
        
        # calculate height of foot
        if len(self.cells_f) > 0:
            self.h_f = sum(self.h_rows_f)
            self.h_f += (len(self.cells_f)-1)*(self.fmt.pad_t + self.fmt.pad_b)
            if len(self.cells_h) != 0 or len(self.cells_b) != 0 or \
                    not self.fmt.skip_pad_t:
                self.h_f += self.fmt.pad_t
            if not self.fmt.skip_pad_b:
                self.h_f += self.fmt.pad_b
        
        # calculate total table height
        self.h = self.h_h + self.h_b + self.h_f
    
    
    def _render(self, data, fmt, w_fix=None):
        """
        Render cells of given data and format
        
        Parameters
        ----------
        w_fix : None, [float, float, ...]
            Predefined width of each column
        """
        cells = [] # rendered cells (Text objects)
        w_cols = [0]*len(self.cols) # width of each column
        h_rows = [] # height of each row
        for d in data:
            row = []
            h_row = 0
            for i, col in enumerate(self.cols):
                fmt[col].width = w_fix[i] if w_fix else None
                row.append(Text(self.ctx, d[col], fmt[col]))
                
                # determine maximum width of column out of all rows
                if row[i].w > w_cols[i]:
                    w_cols[i] = row[i].w
                
                # determine maximum height of row out of all rows
                if row[i].h > h_row:
                    h_row = row[i].h
            cells.append(row)
            h_rows.append(h_row)
        return cells, w_cols, h_rows
    
    
    def draw(self, x, y):
        """
        Parameters
        ----------
        x,y : float
            Absolute position of table to draw
        """
        offset_x = 0
        offset_y = 0
        
        # draw head
        for i in range(len(self.cells_h)):
            if i != 0 or not self.fmt.skip_pad_t:
                offset_y += self.fmt.pad_t
            offset_x = 0
            for j in range(len(self.cols)):
                if j != 0 or not self.fmt.skip_pad_l:
                    offset_x += self.fmt.pad_l
                self.cells_h[i][j].draw(x+offset_x, y+offset_y)
                offset_x += self.w_cols[j] + self.fmt.pad_r
            offset_y += self.h_rows_h[i] + self.fmt.pad_b
        
        # draw body
        for i in range(len(self.cells_b)):
            if offset_y != 0 or i != 0 or not self.fmt.skip_pad_t:
                offset_y += self.fmt.pad_t
            offset_x = 0
            for j in range(len(self.cols)):
                if j != 0 or not self.fmt.skip_pad_l:
                    offset_x += self.fmt.pad_l
                self.cells_b[i][j].draw(x+offset_x, y+offset_y)
                offset_x += self.w_cols[j] + self.fmt.pad_r
            offset_y += self.h_rows_b[i] + self.fmt.pad_b
        
        # draw foot
        for i in range(len(self.cells_f)):
            if offset_y != 0 or i != 0 or not self.fmt.skip_pad_t:
                offset_y += self.fmt.pad_t
            offset_x = 0
            for j in range(len(self.cols)):
                if j != 0 or not self.fmt.skip_pad_l:
                    offset_x += self.fmt.pad_l
                self.cells_f[i][j].draw(x+offset_x, y+offset_y)
                offset_x += self.w_cols[j] + self.fmt.pad_r
            offset_y += self.h_rows_f[i] + self.fmt.pad_b
        
        # draw vertical lines
        if self.fmt.vline_l:
            Line(self.ctx, dy=self.h, fmt=self.fmt.vline_l).draw(x, y)
        if self.fmt.vline_r:
            Line(self.ctx, dy=self.h, fmt=self.fmt.vline_r).draw(x+self.w, y)
        if self.fmt.vline_m:
            offset_x = 0
            line = Line(self.ctx, dy=self.h, fmt=self.fmt.vline_m)
            for i in range(len(self.cols)-1):
                if i != 0 or not self.fmt.skip_pad_l:
                    offset_x += self.fmt.pad_l
                offset_x += self.w_cols[i] + self.fmt.pad_r
                line.draw(x + offset_x, y)
        
        # draw horizontal lines
        if self.fmt.hline_t:
            Line(self.ctx, dx=self.w, fmt=self.fmt.hline_t).draw(x, y)
        if self.fmt.hline_b:
            Line(self.ctx, dx=self.w, fmt=self.fmt.hline_b).draw(x, y+self.h)
        if self.fmt.hline_h and self.cells_h and (self.cells_b):
            Line(self.ctx, dx=self.w, fmt=self.fmt.hline_h).draw(x,y+self.h_h)
        if self.fmt.hline_f and self.cells_f and (self.cells_h or self.cells_b):
            Line(self.ctx, dx=self.w, fmt=self.fmt.hline_f).draw(x,
                y+self.h_h+self.h_b)
        if self.fmt.hline_m:
            line = Line(self.ctx, dx=self.w, fmt=self.fmt.hline_m)
            offset_y = 0
            for i in range(len(self.cells_h)-1):
                if i != 0 or not self.fmt.skip_pad_t:
                    offset_y += self.fmt.pad_t
                offset_y += self.h_rows_h[i] + self.fmt.pad_b
                line.draw(x, y+offset_y)
            
            offset_y = self.h_h
            for i in range(len(self.cells_b)-1):
                if len(self.cells_h) != 0 or i != 0 or not self.fmt.skip_pad_t:
                    offset_y += self.fmt.pad_t
                offset_y += self.h_rows_b[i] + self.fmt.pad_b
                line.draw(x, y+offset_y)
            
            offset_y = self.h_h + self.h_b
            for i in range(len(self.cells_f)-1):
                if i != 0 or not self.fmt.skip_pad_t:
                    offset_y += self.fmt.pad_t
                offset_y += self.h_rows_f[i] + self.fmt.pad_b
                line.draw(x, y+offset_y)
    
    
    def split(self, max_height, repeat_header=False):
        """
        Split table into multiple tables in order to fit in given `max_height`
        
        Parameters
        ----------
        max_height : float, list<float>
            Maximum height of table. Can be a list of heights, so different 
            table parts can have different sizes. Last height will be repeated
            if required
        repeat_header, repeat_foot : bool
            Whether header should be repeated in each part
        """
        if isinstance(max_height, float):
            max_height = [max_height]
        i_h = 0
        
        if self.h_h > max_height[i_h] or self.h_f > max_height[i_h]:
            raise RenderError("Can not split table with head or foot height " +
                "greater than maximum height")
        
        for i in range(len(self.cells_h)):
            if self.h_rows_h[i] > max_height[i_h]:
                raise RenderError("Can not split table with head rows " +
                "heigher than maximum height")
        
        for i in range(len(self.cells_b)):
            if self.h_rows_b[i] > max_height[i_h]:
                raise RenderError("Can not split table with body rows " +
                "heigher than maximum height")
        
        for i in range(len(self.cells_f)):
            if self.h_rows_f[i] > max_height[i_h]:
                raise RenderError("Can not split table with foot rows " +
                "heigher than maximum height")
        
        tables = []
        row_cnt = 0
        foot = False
        while row_cnt < len(self.cells_b) or not foot:
            size_avail = max_height[i_h]
            if i_h+1 < len(max_height):
                i_h += 1
            
            table_new = copy.copy(self)
            
            # handle header
            if len(tables) == 0 or repeat_header:
                size_avail -= self.h_h
            else:
                table_new.cells_h = []
                table_new.h_h = 0
                table_new.h_rows_h = 0
            
            # handle body
            cells_b = []
            h_b = 0
            h_rows_b = []
            for i in range(row_cnt, len(self.cells_b)):
                h_row = self.h_rows_b[i]
                if i != 0 or table_new.cells_h or not self.fmt.skip_pad_t:
                    h_row += self.fmt.pad_t
                
                if i != len(self.cells_b)-1 or table_new.cells_f or \
                        not self.fmt.skip_pad_b:
                    h_row += self.fmt.pad_b
                
                if size_avail - h_row < 0:
                    break
                row_cnt += 1
                cells_b.append(self.cells_b[i])
                h_b += h_row
                h_rows_b.append(self.h_rows_b[i])
                size_avail -= h_row
            table_new.cells_b = cells_b
            table_new.h_b = h_b
            table_new.h_rows_b = h_rows_b
            
            # handle foot
            if row_cnt != len(self.cells_b) or size_avail < self.h_f:
                table_new.cells_f = []
                table_new.h_f = 0
                table_new.h_rows_f = 0
            else:
                foot = True
            
            table_new.h = table_new.h_h + table_new.h_b + table_new.h_f
            tables.append(table_new)
        return tables

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

class PDF:
    """
    Abstract PDF document class providing an interface for either saving or 
    printing a PDF document. The class uses gtk.PrintOperation internally.
    """
    
    def __init__(self, unit=gtk.UNIT_MM, size=gtk.PAPER_NAME_A4,
            orientation=gtk.PAGE_ORIENTATION_PORTRAIT):
        """
        Parameters
        ----------
        unit : gtk unit constant
        size : gtk paper name constant
        orientation : gtk page orientation constant
        
        see http://www.pygtk.org/pygtk2reference/gtk-constants.html
        for available constantes
        """
        self.op = None
        self.page_setup = gtk.PageSetup()
        self.page_setup.set_orientation(orientation)
        self.page_setup.set_paper_size(gtk.PaperSize(size))
        self.unit = unit
        self.w = self.page_setup.get_paper_size().get_width(unit)
        self.h = self.page_setup.get_paper_size().get_height(unit)
        
        # Workaround:
        # Variable `self.error` keeps track of exceptions raised during print
        # operation in the methods `PDF._paginate()` or `PDF._draw_page()`. To
        # catch the exceptions, the calls of these methods are encapsulated
        # within `PDF.__paginate()` or `PDF.__draw_page()`, where this variable
        # is set to the exception and the print operation is canceled via
        # `op.cancel()`.
        # The reason for this is that exceptions thrown during the run of the
        # print operation are caught internally and can not be handled further.
        # This leads to fatal uncaught exception error.
        self.error = None
    
    
    def save_to_file(self, filename):
        """
        Save pdf to file
        
        Parameters
        ----------
        filename : string
        """
        self.__render("save", filename)
    
    
    def show_print_dialog(self):
        """
        Show print dialog
        """
        self.__render("print")
    
    
    def _paginate(self, op, ctx):
        """
        Method is called before the rendering process starts. It has to 
        calculate the required page count and save it via 
        `PDF.set_page_count(page_cnt)`
        
        Parameters
        ----------
        op : gtk.PrintOperation
        ctx : gtk.PrintContext
        """
        raise NotImplementedError("Method `_paginate()` is not implemented")
    
    
    def _draw_page(self, op, ctx, no):
        """
        Method is called for each page to draw. The method has to render the 
        page content onto the print context `ctx`
        
        Parameters
        ----------
        op : gtk.PrintOperation
        ctx : gtk.PrintContext
        no : number of the currently printed page
        """
        raise NotImplementedError("Method `_draw_page()` is not implemented")
    
    
    def _set_page_count(self, page_cnt):
        """
        Set page count. Call this method from within the `PDF._paginate()`
        method
        
        Parameters
        ----------
        page_cnt : total count of pages
        """
        self.op.set_n_pages(page_cnt)
    
    
    def _get_page_count(self):
        """
        Return page count set by `_set_page_count()`
        """
        return self.op.get_n_pages_to_print()
    
    
    def __render(self, action, filename=None):
        """
        Render page and either save or print result
        
        Parameters
        ----------
        action : string ("save", "print")
        filename : string
        """
        
        # create print operation
        self.op = gtk.PrintOperation()
        self.op.set_default_page_setup(self.page_setup)
        self.op.set_use_full_page(True)
        self.op.set_unit(self.unit)
        self.op.connect("begin-print", self.__paginate)
        self.op.connect("draw-page", self.__draw_page)
        self.op.set_show_progress(True)
        self.op.set_allow_async(True)
        
        # run print operation
        if action == "save":
            self.op.set_export_filename(filename)
            res = self.op.run(gtk.PRINT_OPERATION_ACTION_EXPORT, None)
        else:
            res = self.op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, None)
        
        # check for exceptions during print operation
        # see comment about workaround in `__init__()` method
        if self.error != None:
            raise self.error
        
        if res == gtk.PRINT_OPERATION_RESULT_ERROR:
            raise RenderError("UNKNOWN_ERROR")
    
    
    def __paginate(self, op, ctx):
        """
        Wrapper around the `_paginate()` method to catch RenderErrors
        see comment about workaround in `__init__()` method
        
        Parameters
        ----------
        op : gtk.PrintOperation
        ctx : gtk.PrintContext
        """
        try:
            self._paginate(op, ctx)
            if op.get_n_pages_to_print() == 0:
                raise RenderError("NO_PAGES")
        except RenderError as e:
            op.cancel()
            self.error = e
    
    
    def __draw_page(self, op, ctx, no):
        """
        Wrapper around the `_draw_page()` method to catch RenderErrors
        see comment about workaround in `__init__()` method
        
        Parameters
        ----------
        op : gtk.PrintOperation
        ctx : gtk.PrintContext
        """
        try:
            self._draw_page(op, ctx, no)
        except RenderError as e:
            op.cancel()
            self.error = e

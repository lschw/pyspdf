# pyspdf
a small and simple pdf renderer based on pygtk

## Installation
Download the latest release from [/releases/latest](https://github.com/lschw/pyspdf/releases/latest).

Either copy the *pyspdf/* directory to your desired location or install via

    cd /path/to/extracted/files
    pip install .


## Features
* pdf creation
* direct printing from pygtk GUI application
* rendering of images
* rendering of lines
* rendering of text (autosplitting of text on multiple pages possible)
* rendering of tables (autosplitting of table on multiple pages possible)


## Usage
The general usage is as following. Derive a class from pyspdf.PDF and implement the methods *_paginate()* and *_draw_page()*. The former method can prepare content for rendering and MUST set the page count via *_set_page_count()*. The latter is called for each page to render and has to draw all the content.

To render the pdf call the method *save_to_file(%filename%)*. Inside a pygtk GUI application you can also call the method *show_print_dialog()*, which shows the default print dialog to directly print the rendered content.


### Example
    
    import pyspdf as pdf

    class SamplePDF(pdf.PDF):
    
        def _paginate(self, op, ctx):
            self._set_page_count(1)
        
        def _draw_page(self, op, ctx, no):
        
            pdf.Line(ctx, dx=self.w-20, dy=0,
                fmt=pdf.LineFormat(width=1, style="solid"),
            ).draw(10,10)
            
            pdf.Text(ctx,
                "This is a sample text",
                fmt=pdf.TextFormat(size=20),
            ).draw(10,40)
        
    try:
        samplepdf = SamplePDF()
        samplepdf.save_to_file("example_line.pdf")
    except pdf.RenderError as e:
        print(e.code, e.args)


For more detailed examples see the example files in the [example/](example/) folder.

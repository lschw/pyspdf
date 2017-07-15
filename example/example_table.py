import sys
sys.path.append("../")
import pyspdf as pdf
import random
import string

class SamplePDF(pdf.PDF):
    
    def __init__(self):
        pdf.PDF.__init__(self)
        self.tables = []
        
        # define table
        self.table_cols = ["abc", "def", "foo", "bar"]
        self.table_head = [{col:col.upper() for col in self.table_cols}]
        self.table_foot = [{col:col.upper() for col in self.table_cols}]
        self.table_body = []
        
        # add random table data
        for i in range(50):
            row = {}
            for col in self.table_cols:
                row[col] = random.randint(1,1e6)
            self.table_body.append(row)
        
        # define table format
        self.margin=10
        self.table_fmt = pdf.TableFormat(self.table_cols)
        self.table_fmt.set_padding(2)
        self.table_fmt.set_width("fixed", self.w-2*self.margin)
        self.table_fmt.set_col_width("equal")
        self.table_fmt.set_fmt(pdf.TextFormat(size=9))
        self.table_fmt.set_fmt_tpart("head", "style", "bold")
        self.table_fmt.set_fmt_col("foo", "align", "right")
        self.table_fmt.set_hline(pdf.LineFormat(style="dashed"), "head")
        self.table_fmt.set_hline(pdf.LineFormat(width=0.5), "foot")
        self.table_fmt.set_vline(pdf.LineFormat())
    
    
    def _paginate(self, op, ctx):
        
        # divide table onto multiple pages
        self.tables = pdf.Table(
            ctx,
            self.table_fmt, self.table_head, self.table_body, self.table_foot
        ).split(self.h-2*self.margin, repeat_header=True)
        
        # total page number = number of splitted table + 1(for extra test data)
        self._set_page_count(len(self.tables))
    
    
    def _draw_page(self, op, ctx, no):
        
        # show page number
        page_no = pdf.Text(ctx, 
            "{} / {}".format(no+1, self._get_page_count()),
            pdf.TextFormat(size=8)
        )
        page_no.draw((self.w-page_no.w)/2, self.h-self.margin)
        
        self.tables[no].draw(self.margin, self.margin)

try:
    samplepdf = SamplePDF()
    samplepdf.save_to_file("example_table.pdf")
except pdf.RenderError as e:
    print(e.code, e.args)



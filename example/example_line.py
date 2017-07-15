import sys
sys.path.append("../")
import pyspdf as pdf

class SamplePDF(pdf.PDF):
    
    def _paginate(self, op, ctx):
        self._set_page_count(1)
    
    
    def _draw_page(self, op, ctx, no):
        
        pdf.Line(ctx, dx=self.w-20, dy=0,
            fmt=pdf.LineFormat(width=1, style="solid"),
        ).draw(10,10)
        
        pdf.Line(ctx, dx=self.w-20, dy=0,
            fmt=pdf.LineFormat(width=1, style="double"),
        ).draw(10,30)
        
        pdf.Line(ctx, dx=self.w-20, dy=0,
            fmt=pdf.LineFormat(width=1, style="dotted"),
        ).draw(10,50)
        
        pdf.Line(ctx, dx=self.w-20, dy=0,
            fmt=pdf.LineFormat(width=1, style="dashed"),
        ).draw(10,70)
        
        pdf.Line(ctx, dx=self.w-20, dy=0,
            fmt=pdf.LineFormat(width=0.1, style="solid", color="red"),
        ).draw(10,90)
        
        pdf.Line(ctx, dx=self.w-20, dy=0,
            fmt=pdf.LineFormat(width=0.1, style="double", color="blue"),
        ).draw(10,100)
        
        pdf.Line(ctx, dx=self.w-20, dy=0,
            fmt=pdf.LineFormat(width=3, style="dotted", color="#ff00ff"),
        ).draw(10,110)
        
        pdf.Line(ctx, dx=self.w-20, dy=0,
            fmt=pdf.LineFormat(width=0.1, style="dashed", color="orange"),
        ).draw(10,120)
        
        
        pdf.Line(ctx, dx=0, dy=self.h-130-10).draw(10,130)
        pdf.Line(ctx, dx=60, dy=self.h-130-10).draw(20,130)
        pdf.Line(ctx, dx=60, dy=self.h-130-10,
            fmt=pdf.LineFormat(width=0.4, style="double")
        ).draw(40,130)
        pdf.Line(ctx, dx=60, dy=self.h-130-10,
            fmt=pdf.LineFormat(width=0.4, style="dashed", color="#ffff00")
        ).draw(60,130)
        pdf.Line(ctx, dx=60, dy=self.h-130-10,
            fmt=pdf.LineFormat(width=0.4, style="dotted")
        ).draw(80,130)
        pdf.Line(ctx, dx=-30, dy=50,
            fmt=pdf.LineFormat(width=0.4, style="dotted")
        ).draw(self.w-10,130)
        pdf.Line(ctx, dx=-30, dy=50,
            fmt=pdf.LineFormat(width=0.4, style="dotted")
        ).draw(self.w-20,130)


try:
    samplepdf = SamplePDF()
    samplepdf.save_to_file("example_line.pdf")
except pdf.RenderError as e:
    print(e.code, e.args)

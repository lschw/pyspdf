import sys
sys.path.append("../")
import pyspdf as pdf

class SamplePDF(pdf.PDF):
    
    def _paginate(self, op, ctx):
        self._set_page_count(1)
    
    def _draw_page(self, op, ctx, no):
        
        pdf.Image(
            ctx,
            filename="test.jpg",
            fmt=pdf.ImageFormat(self.w-20,100,center=True,dots_per_unit=5),
        ).draw(10,10)
        
        pdf.Image(
            ctx,
            filename="test.png",
            fmt=pdf.ImageFormat(100,50,dots_per_unit=5),
        ).draw(50,130)
        
        pdf.Image(
            ctx,
            filename="test.svg",
            fmt=pdf.ImageFormat(60,50,dots_per_unit=10),
        ).draw(50,90)


try:
    samplepdf = SamplePDF()
    samplepdf.save_to_file("example_image.pdf")
except pdf.RenderError as e:
    print(e.code, e.args)

import sys
sys.path.append("../")
import pango
import pyspdf as pdf

text1 = "The quick brown fox jumps over the lazy dog"

text2 = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed doeiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enimad minim veniam, quis nostrud exercitation ullamco laboris nisi utaliquip ex ea commodo consequat. <b>Duis</b> aute irure dolor inreprehenderit in voluptate velit esse cillum dolore eu fugiat nullapariatur. Excepteur sint occaecat cupidatat non proident, sunt inculpa qui officia deserunt mollit anim id est laborum.
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed doeiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enimad minim veniam, quis nostrud exercitation ullamco laboris nisi utaliquip ex ea commodo consequat. Duis aute irure dolor inreprehenderit in <u>voluptate</u> velit esse cillum dolore eu fugiat nullapariatur. Excepteur sint occaecat cupidatat non proident, sunt inculpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur <i>adipisicing</i> elit, sed doeiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enimad minim veniam, quis nostrud exercitation ullamco laboris nisi utaliquip ex ea commodo consequat.
Duis aute irure dolor inreprehenderit in voluptate velit esse cillum dolore eu fugiat nullapariatur. Excepteur sint occaecat cupidatat non proident, sunt inculpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed doeiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enimad minim veniam, quis nostrud exercitation."""

text3 = " ".join([text2]*10)

class SamplePDF(pdf.PDF):
    
    def __init__(self):
        pdf.PDF.__init__(self)
        self.text_list = []
    
    def _paginate(self, op, ctx):
        
        # create multiple text elements for long text
        self.text_list = pdf.Text(ctx,
            text3,
            fmt=pdf.TextFormat(size=10, justify=True, line_spacing=2,
                width=self.w-20),
        ).split(max_height=[100,self.h-30])
        
        self._set_page_count(len(self.text_list))
    
    
    def _draw_page(self, op, ctx, no):
        
        # show page number
        page_no = pdf.Text(ctx,
            "{} / {}".format(no+1, self._get_page_count()),
            pdf.TextFormat(size=8)
        )
        page_no.draw((self.w-page_no.w)/2, self.h-10)
        
        # first page
        if no == 0:
            pdf.Text(ctx,
                text1,
                fmt=pdf.TextFormat(size=20),
            ).draw(10,10)
            
            pdf.Text(ctx,
                text1,
                fmt=pdf.TextFormat(font="monospace", size=10, style="italic",
                    color="#ff0000"),
            ).draw(50,50)
            
            pdf.Text(ctx,
                text2,
                fmt=pdf.TextFormat(font="CMU Sans Serif", size=10,
                line_spacing=2, wrap=pango.WRAP_WORD, justify=True,
                width=self.w-20),
            ).draw(10,70)
            
            self.text_list[no].draw(10,self.h-20-100)
        
        # all other pages
        else:
            self.text_list[no].draw(10,10)


try:
    samplepdf = SamplePDF()
    samplepdf.save_to_file("example_text.pdf")
except pdf.RenderError as e:
    print(e.code, e.args)


from itertools import chain
import os

def html_tag_maker(tag):
    def html_tag(func):
        def wrapped(*args, **kwargs):
            yield "<%s>" % tag
            for item in func(*args, **kwargs):
                yield item
            yield "</%s>" % tag
        return wrapped
    return html_tag

class WebView(object):
    doctype = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'

    def __init__(self, description, histo_names, picture_format='png'):
        self._description = description
        self._pictures = ["%s.%s" % (histo_name, picture_format) for histo_name in histo_names]

    @html_tag_maker("html")
    def html_code(self):
        return chain(self.header(), self.body())

    @html_tag_maker("head")
    def header(self):
        yield '<title>%s</title>' % (self._description)
        
    @html_tag_maker("body")
    def body(self):
        yield '<h1>Description: %s</h1>' % (self._description)
        for picture in self._pictures:
            yield '<img src="%s"/>' % (picture)
        
    def create_web_view(self, filename="index.html"):
        with open(os.path.join(self._description, filename) ,'w') as f:
            f.write(self.doctype)
            f.writelines(self.html_code())

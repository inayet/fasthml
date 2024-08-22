from fasthtml.common import *

# Add the HighlightJS built-in header
hdrs = (HighlightJS(langs=["python", "javascript", "html", "css"]),)

app, rt = fast_app(hdrs=hdrs)

code_example = """
import datetime
import time

for i in range(10):
    print(f"{datetime.datetime.now()}")
    time.sleep(1)
"""


@rt("/")
def get(req):
    return Titled(
        "Markdown rendering example",
        Div(
            # The code example needs to be surrounded by
            # Pre & Code elements
            Pre(Code(code_example))
        ),
    )


serve()

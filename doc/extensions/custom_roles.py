from docutils import nodes
from matplotlib import rcParamsDefault

RC_TUTORIAL = "https://matplotlib.org/stable/tutorials/introductory/customizing.html"


def rcparam_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    rendered = nodes.Text(f"rcParams['{text}']")
    refuri = RC_TUTORIAL + f"?highlight={text}#matplotlibrc-sample"
    ref = nodes.reference(rawtext, rendered, refuri=refuri)
    node_list = [nodes.literal("", "", ref)]
    # The default backend would be printed as "agg", but that's not
    # correct (as the default is actually determined by fallback).
    if text in rcParamsDefault and text != "backend":
        node_list.extend(
            [
                nodes.Text(" (default: "),
                nodes.literal("", repr(rcParamsDefault[text])),
                nodes.Text(")"),
            ],
        )
    return node_list, []


def setup(app):
    app.add_role("rc", rcparam_role)
    return {"parallel_read_safe": True, "parallel_write_safe": True}

import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="/")

templateEnv = jinja2.Environment(loader=templateLoader)

TEMPLATE_FILE = "./template.jinja"

template = templateEnv.get_template(TEMPLATE_FILE)

templateVars = {"title": "Test Example",
                "description": "A simple inquiry of function."}

outputText = template.render(templateVars)

print outputText

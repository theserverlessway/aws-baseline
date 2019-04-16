from awscli.compat import six
from awscli.formatter import TableFormatter
from awscli.table import MultiTable, ColorizedStyler
import sys
import json


class Object(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.query = None


stream = six.StringIO()
styler = ColorizedStyler()
table = MultiTable(initial_section=False,
                   column_separator='|', styler=styler)
formatter = TableFormatter(Object(color='on'))
formatter.table = table


DATA = []

for line in sys.stdin.readlines():
    if line.strip():
        DATA.append(json.loads(line))

formatter(sys.argv[1], DATA, stream=stream)
output = stream.getvalue()
if output:
    print(output)

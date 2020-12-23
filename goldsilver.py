import core.module
import core.widget
import core.event
import core.decorators
import util.cli
import json
import requests
from requests.exceptions import RequestException

def get_data(type):
    try:
        request = requests.post("https://www.thesilvermountain.nl/nl/rates/ajax/rate", { "type": type, "limit": 7, "cur": "eur", "unit": "ozt", })
        data = json.loads(request.text)
    except (RequestException, Exception):
        return "???"
    if not "rates" in data:
        return "???"

    return str("€{:.2f}".format(float(data["rates"][0]["val"])))

class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.status))
        self.background = True
        widget = self.widget()

    def status(self, widget):
        goldprice = get_data("gold")
        silverprice = get_data("silver")
        return "Gold {} Silver {}".format(goldprice, silverprice)


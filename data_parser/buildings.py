from collections import OrderedDict
from datetime import datetime

import requests

from data_parser.base_parser import BaseParser


class BuildingsParser(BaseParser):
    link = "http://map.utoronto.ca"

    # currently a little redundant
    campus_map = {
        "utsg": "St. George",
        "utm": "Mississauga",
        "utsc": "Scarborough"
    }

    def __init__(self):
        super().__init__(
            file="../data/buildings.json"
        )

    def process(self):
        for campus in BuildingsParser.campus_map:
            page = requests.get(f"{BuildingsParser.link}/data/map/{campus}", headers={"Referer": BuildingsParser.link})
            response = page.json()
            for el in response['buildings']:
                building = OrderedDict()
                building['id'] = self.process_field(el, 'id')
                building['code'] = self.process_field(el, 'code')
                building['tags'] = self.process_field(el, 'tags')
                building['name'] = self.process_field(el, 'title')
                building['short_name'] = self.process_field(el, 'short_name')

                address = OrderedDict()
                address['street'] = self.process_field(el, 'street')
                address['city'] = self.process_field(el, 'city').title() if self.process_field(el, 'city') else None
                address['province'] = self.process_field(el, 'province')
                address['country'] = self.process_field(el, 'country')
                address['postal'] = self.process_field(el, 'postal')
                building['address'] = address

                coordinates = OrderedDict()
                coordinates['latitude'] = self.process_field(el, 'lat')
                coordinates['longitude'] = self.process_field(el, 'lng')
                building['coordinates'] = coordinates

                date = datetime.now()
                building['last_updated'] = date.isoformat()

                self.add_item(building)

    @staticmethod
    def process_field(el, field):
        if field in el:
            return el[field]
        return None


if __name__ == "__main__":
    p = BuildingsParser()
    p.run()

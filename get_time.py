#!/Users/juan/.pyenv/shims/python
# encoding: utf-8

import sys
from datetime import datetime
from geopy.geocoders import Nominatim

from workflow import Workflow, web

geolocator = Nominatim(user_agent="alfred workflow")


def main(wf):
    # Your imports go here if you want to catch import errors (not a bad idea)
    # or if the modules/packages are in a directory added via `Workflow(libraries=...)`
    # import somemodule
    # import anothermodule

    # Get args from Workflow, already in normalized Unicode
    args = wf.args

    if len(args[0]) == 0:
        return

    api_key = args[0]
    search_words = " ".join(args[1:])
    
    location = geolocator.geocode(search_words)

    base_url = f"https://api.ipgeolocation.io/timezone?apiKey={api_key}"

    response_here = web.get(base_url).json()
    date_here = response_here["date"]
    dst_here = response_here["dst_savings"]
    if dst_here:
        timezone_offset_here = response_here["timezone_offset_with_dst"]
    else:
        timezone_offset_here = response_here["timezone_offset"]
    
    response_at_place = web.get(f"{base_url}&lat={location.latitude}&long={location.longitude}").json()
    timezone_at_place = response_at_place["timezone"]
    time_at_place = response_at_place["time_24"]
    date_at_place = response_at_place["date"]
    dst_at_place = response_at_place["dst_savings"]
    if dst_at_place:
        timezone_offset_at_place = response_at_place["timezone_offset_with_dst"]
    else:
        timezone_offset_at_place = response_at_place["timezone_offset"]

    hours_diff = float(timezone_offset_at_place) - float(timezone_offset_here)
    if not hours_diff % 1:
        hours_diff = round(hours_diff)

    formated_title = time_at_place
    
    if date_at_place != date_here:
        # say that it is not the same day
        days_diff = (datetime.strptime(date_at_place, "%Y-%m-%d") - datetime.strptime(date_here, "%Y-%m-%d")).days
        formated_title += f"  ({days_diff:+} day)"

    formated_title += f"\t\t({timezone_at_place}, UTC{timezone_offset_at_place:+})\t\t\t\t({hours_diff:+}h)"

    wf.add_item(
        title=formated_title,
        subtitle=location.address,
        valid=True
        )

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but Alfred won't be listening
    # any more...
    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow()
    # Call your entry function via `Workflow.run()` to enable its helper
    # functions, like exception catching, ARGV normalization, magic
    # arguments etc.
    sys.exit(wf.run(main))

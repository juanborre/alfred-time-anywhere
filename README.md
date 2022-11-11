# alfred-time-anywhere

[Alfred](https://www.alfredapp.com/) workflow that will show you the time anywhere in the planet.

![Alfred Time Anywhere gif](https://github.com/juanborre/alfred-time-anywhere/blob/main/alfred-time-anywhere.gif)

You can search for any country/city/village/address. 

The information displayed is:
```
Time    (Timezone, UTC offset)  (hours difference with local time)
Adress
```

![Alfred Time Anywhere img](https://github.com/juanborre/alfred-time-anywhere/blob/main/alfred-time-anywhere.jpg)

## How it works

The script uses the Python [Geopy](https://pypi.org/project/geopy/) package in order to find the GPS coordinates of the place you type.

Then, it will do a query to the [ipgeolocation API](https://ipgeolocation.io/) in order to find the time and the timezone.

There are other approaches using other Python packages but either the workflow size was too big or the response time was too long. This solution seems to find a sweetspot between the two.

## Configuration

The workflow works out of the box with a default API_KEY for the [ipgeolocation API](https://ipgeolocation.io/).

The API is rate limited so, if you stick with using the workflow, I suggest that you make your own to free space for other people and not to be rate limited yourself.

Making an API_KEY is free of charge as of today.

Enjoy! 👋
# Quick Start Guide - Leaflet - a JavaScript library for interactive maps

Created: Feb 15, 2020 8:22 AM
URL: https://leafletjs.com/examples/quick-start/

This step-by-step guide will quickly get you started on Leaflet basics, including setting up a Leaflet map, working with markers, polylines and popups, and dealing with events.

[Untitled](Quick%20Start%20Guide%20-%20Leaflet%20-%20a%20JavaScript%20library%2034abae4121e74559802c946664107c5f/Untitled%20Database%20fa332699d13d4c6cb09f68b5e8a9e01b.csv)

### Preparing your page

Before writing any code for the map, you need to do the following preparation steps on your page:

- 

    Include Leaflet CSS file in the head section of your document:

    ```
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
       integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
       crossorigin=""/>
    ```

- 

    Include Leaflet JavaScript file **after** Leaflet’s CSS:

    ```
    <!-- Make sure you put this AFTER Leaflet's CSS -->
     <script src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js"
       integrity="sha512-gZwIG9x3wUXg2hdXF6+rVkLF/0Vi9U8D2Ntg4Ga5I5BZpVkVxlJWbSQtXPSiUTtC0TjtGOmxa1AJPuV0CPthew=="
       crossorigin=""></script>
    ```

- 

    Put a `div` element with a certain `id` where you want your map to be:

    ```
    <div id="mapid"></div>
    ```

- 

    Make sure the map container has a defined height, for example by setting it in CSS:

    ```
    #mapid { height: 180px; }
    ```

Now you’re ready to initialize the map and do some stuff with it.

### Setting up the map

Let’s create a map of the center of London with pretty Mapbox Streets tiles. First we’ll initialize the map and set its view to our chosen geographical coordinates and a zoom level:

```
var mymap = L.map('mapid').setView([51.505, -0.09], 13);
```

By default (as we didn’t pass any options when creating the map instance), all mouse and touch interactions on the map are enabled, and it has zoom and attribution controls.

Note that `setView` call also returns the map object — most Leaflet methods act like this when they don’t return an explicit value, which allows convenient jQuery-like method chaining.

Next we’ll add a tile layer to add to our map, in this case it’s a Mapbox Streets tile layer. Creating a tile layer usually involves setting the [URL template](https://leafletjs.com/reference.html) for the tile images, the attribution text and the maximum zoom level of the layer. In this example we’ll use the `mapbox/streets-v11` tiles from [Mapbox’s Static Tiles API](https://docs.mapbox.com/api/maps/#static-tiles) (in order to use tiles from Mapbox, you must also [request an access token](https://www.mapbox.com/studio/account/tokens/)). Because this API returns 512x512 tiles by default (instead of 256x256), we will also have to explicitly specify this and offset our zoom by a value of -1.

```
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'your.mapbox.access.token'
}).addTo(mymap);
```

Make sure all the code is called after the `div` and `leaflet.js` inclusion. That’s it! You have a working Leaflet map now.

It’s worth noting that Leaflet is provider-agnostic, meaning that it doesn’t enforce a particular choice of providers for tiles. You can try replacing `mapbox/streets-v11` with `mapbox/satellite-v9`, and see what happens. Also, Leaflet doesn’t even contain a single provider-specific line of code, so you’re free to use other providers if you need to (we’d suggest Mapbox though, it looks beautiful).

Whenever using anything based on OpenStreetMap, an *attribution* is obligatory as per the [copyright notice](https://www.openstreetmap.org/copyright). Most other tile providers (such as [Mapbox](https://docs.mapbox.com/help/how-mapbox-works/attribution/), [Stamen](http://maps.stamen.com/) or [Thunderforest](https://www.thunderforest.com/terms/)) require an attribution as well. Make sure to give credit where credit is due.

### Markers, circles and polygons

Besides tile layers, you can easily add other things to your map, including markers, polylines, polygons, circles, and popups. Let’s add a marker:

```
var marker = L.marker([51.5, -0.09]).addTo(mymap);
```

Adding a circle is the same (except for specifying the radius in meters as a second argument), but lets you control how it looks by passing options as the last argument when creating the object:

```
var circle = L.circle([51.508, -0.11], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: 500
}).addTo(mymap);
```

Adding a polygon is as easy:

```
var polygon = L.polygon([
    [51.509, -0.08],
    [51.503, -0.06],
    [51.51, -0.047]
]).addTo(mymap);
```

### Working with popups

Popups are usually used when you want to attach some information to a particular object on a map. Leaflet has a very handy shortcut for this:

Try clicking on our objects. The `bindPopup` method attaches a popup with the specified HTML content to your marker so the popup appears when you click on the object, and the `openPopup` method (for markers only) immediately opens the attached popup.

You can also use popups as layers (when you need something more than attaching a popup to an object):

Here we use `openOn` instead of `addTo` because it handles automatic closing of a previously opened popup when opening a new one which is good for usability.

### Dealing with events

Every time something happens in Leaflet, e.g. user clicks on a marker or map zoom changes, the corresponding object sends an event which you can subscribe to with a function. It allows you to react to user interaction:

Each object has its own set of events — see [documentation](https://leafletjs.com/reference.html) for details. The first argument of the listener function is an event object — it contains useful information about the event that happened. For example, map click event object (`e` in the example above) has `latlng` property which is a location at which the click occurred.

Let’s improve our example by using a popup instead of an alert:

Try clicking on the map and you will see the coordinates in a popup. [View the full example →](https://leafletjs.com/examples/quick-start/example.html)

Now you’ve learned Leaflet basics and can start building map apps straight away! Don’t forget to take a look at the detailed [documentation](https://leafletjs.com/reference.html) or [other examples](https://leafletjs.com/examples.html).
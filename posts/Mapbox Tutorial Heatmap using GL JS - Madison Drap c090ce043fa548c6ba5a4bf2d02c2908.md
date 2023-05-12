# Mapbox Tutorial: Heatmap using GL JS - Madison Draper - Medium

Created: Feb 20, 2020 9:02 AM
URL: https://medium.com/@mzdraper/mapbox-tutorial-heatmap-using-gl-js-bc2e5199d630

![1*Un83np6gXvUEialrlXo2pA.png](Mapbox%20Tutorial%20Heatmap%20using%20GL%20JS%20-%20Madison%20Drap%20c090ce043fa548c6ba5a4bf2d02c2908/1Un83np6gXvUEialrlXo2pA.png)

Heatmaps, or isorhythmic maps, display dense amounts of points as a painted cluster. It’s visually stimulating and shows gradients of concentrations. One of the most common heat maps is a meteorological map. [Here](https://www.mapbox.com/help/make-a-heatmap-with-mapbox-gl-js/) is Mapbox’s original tutorial for another point of reference.

1. Mapbox account and access token.
2. Mapbox GL JS, a Javascript Library.
3. Text Editor, either Sublime or Atom works great.
4. GeoJSON [data](https://github.com/mzdraper/how-to-map/blob/master/trees.geojson) of the street trees in Pittsburgh from the Western Pennsylvania Regional Data Center.
5. [This](https://github.com/mzdraper/how-to-map/blob/master/heat.html) extensively commented code. I won’t give you all the answers throughout the tutorial, but reference this if you get stuck!

Let’s start by setting up a web page with an empty blank map. This will be our canvas.

1. Open a new document in your text editor and save it as `index.html`.
2. Create a skeleton HTML document.

```
<!DOCtype html><html><head>    <meta charset='utf-8' />    <title></title>    <style> /* CSS here */ </style></head><body>    <script> /* JavaScript here */ </script><body></html>
```

3. **Add Mapbox GL JS** between the `<head>` tags.

```
<link href='https://api.tiles.mapbox.com/mapbox-gl-js/v0.44.1/mapbox-gl.css' rel='stylesheet' />
```

4. Between the `<head>` tags, add **CSS styling** for your map.

```
<style>         body {        margin: 0;        padding: 0;      }      #map {        position: absolute;        top: 0;        bottom: 0;        width: 100%;      }</style>
```

5. Add your **map container** between the `<body>` tags.

```
<div id='map'></div>
```

6. Between the `<script>` tags, add **your access token** and initiate the map. In your map variable, you can set the container, style, center and zoom.

```
==new-
```

Open your map in the browser. If you don’t see it come up, that’s okay. Go through the steps again and try to troubleshoot yourself before looking at the provided code.

1. Use the `.on` function to initiate an event listener for `load`, then give it a function to fire.
2. Add the data source with `.addSource()`. Declare an id, type and path.

```
/* add heatmap layer here */add circle layer here */
```

4. Add the **source** to the map as a layer using `.addLayer()`. Declare the id, type, source, zoom and details.

5. Add a JSON to `paint` to adjust heat map properties. Add stops for zoom adjustments. [This](https://www.mapbox.com/help/make-a-heatmap-with-mapbox-gl-js/#heatmap-paint-properties) describes the heat-map properties thoroughly.

```
// increase weight as diameter breast height increases// increase intensity as zoom level increases// assign color values be applied to points depending on their density// increase radius as zoom increases// decrease opacity to transition into the circle layer
```

6. Add a JSON to `paint` to adjust circle properties. Add stops for zoom adjustments.

```
// increase the radius of the circle as the zoom level and dbh value increases
```

1. Use `.on` again to listen for `click` on the specified type `trees-point`.

```
map.on('click', 'trees-point', function (e) {    /* add functionality here */});
```

2. When this occurs, the function will create a new pop-up using `new mapboxgl.Popup()`

3. Set properties to the map, such as its coordinates and HTML styling, and add it to the map

```
new mapboxgl.Popup()    .setLngLat(e.features[0].geometry.coordinates)    .setHTML('<b>DBH:</b> '+ e.features[0].properties.dbh)    .addTo(map);
```

Good job! Refresh your page and try zooming in and out of the area to watch the heatmap and circles switch as you zoom closer. If you’re having some trouble, try to troubleshoot it yourself. Or, you can view [the code](https://github.com/mzdraper/how-to-map/blob/master/heat.html) with extensive comments on the different parts of the code. Hope you learned a lot, let me know how it went!
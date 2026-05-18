# Regional Coverage

Spatial footprint of each tidal hindcast location. Each polygon shows the exact exterior boundary of the FVCOM unstructured triangular mesh used for that location's simulation. Click a region in the legend to zoom to it.

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<style>
#coverage-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 16px;
  margin: 6px 0 1em 0;
  padding: 8px 12px;
  background: rgba(255,255,255,0.94);
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: calc(0.78rem - 2px);
  line-height: 1;
}
.tidal-legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 4px;
  transition: background 0.12s;
}
.tidal-legend-item:hover { background: rgba(0,0,0,0.06); }
.tidal-legend-all { font-weight: 700; color: #444; letter-spacing: 0.03em; }
.tidal-legend-swatch {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 2px;
  flex-shrink: 0;
  opacity: 0.85;
}
/* Persistent region label tooltips */
.tidal-region-tooltip {
  background: rgba(255,255,255,0.93) !important;
  border-width: 1.5px !important;
  border-radius: 4px !important;
  font-size: calc(0.78rem - 2px) !important;
  font-weight: 600 !important;
  padding: 3px 7px !important;
  box-shadow: 0 1px 5px rgba(0,0,0,0.12) !important;
  white-space: nowrap !important;
  color: #222 !important;
}
</style>

<div id="coverage-map" style="height: 420px; width: 100%; border-radius: 6px; border: 1px solid #e0e0e0; margin: 1em 0 0 0;"></div>
<div id="coverage-legend"></div>

<script>
(function () {
  var regions = [
    {
      key: "AK_aleutian_islands",
      label: "Aleutian Islands, Alaska",
      shortLabel: "Aleutian Islands",
      gridPoints: "797,978",
      period: "2010-06-03 – 2011-06-02",
      sampling: "Hourly",
      labelPos: "bottom"
    },
    {
      key: "AK_cook_inlet",
      label: "Cook Inlet, Alaska",
      shortLabel: "Cook Inlet",
      gridPoints: "392,002",
      period: "2005-01-01 – 2005-12-31",
      sampling: "Hourly",
      labelPos: "top"
    },
    {
      key: "NH_piscataqua_river",
      label: "Piscataqua River, New Hampshire",
      shortLabel: "Piscataqua River",
      gridPoints: "292,927",
      period: "2007-01-01 – 2007-12-31",
      sampling: "Half-Hourly",
      labelPos: "bottom"
    },
    {
      key: "WA_puget_sound",
      label: "Salish Sea, Washington",
      shortLabel: "Salish Sea",
      gridPoints: "1,734,765",
      period: "2015-01-01 – 2015-12-30",
      sampling: "Half-Hourly",
      labelPos: "top"
    },
    {
      key: "ME_western_passage",
      label: "Western Passage, Maine",
      shortLabel: "Western Passage",
      gridPoints: "231,208",
      period: "2017-01-01 – 2017-12-31",
      sampling: "Half-Hourly",
      labelPos: "top"
    }
  ];

  // Seaborn deep palette (first 5)
  var colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"];

  // Inject per-color tooltip border/caret styles dynamically
  var styleEl = document.createElement("style");
  colors.forEach(function (color, i) {
    styleEl.textContent +=
      ".tidal-tt-" + i + "{border-color:" + color + "!important}" +
      ".tidal-tt-" + i + ".leaflet-tooltip-top::before{border-top-color:" + color + "!important}" +
      ".tidal-tt-" + i + ".leaflet-tooltip-bottom::before{border-bottom-color:" + color + "!important}";
  });
  document.head.appendChild(styleEl);

  var map = L.map("coverage-map", { center: [45, -105], zoom: 3, minZoom: 2 });

  L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: "abcd",
    maxZoom: 19
  }).addTo(map);

  map.on("click", function () {
    if (expandedMarker) {
      expandedMarker.getTooltip().setContent(expandedMarker._tidalShortLabel);
      expandedMarker._tidalExpanded = false;
      expandedMarker = null;
    }
  });

  var layerBoundsMap = {};
  var loadedLayers = [];
  var loadCount = 0;
  var expandedMarker = null;

  // Legend
  var legendEl = document.getElementById("coverage-legend");

  var allBtn = document.createElement("div");
  allBtn.className = "tidal-legend-item tidal-legend-all";
  allBtn.innerHTML = "All";
  allBtn.addEventListener("click", function () {
    if (loadedLayers.length > 0)
      map.fitBounds(L.featureGroup(loadedLayers).getBounds().pad(0.02), { animate: true, duration: 0.6 });
  });
  legendEl.appendChild(allBtn);

  var sep = document.createElement("div");
  sep.style.cssText = "width:1px;background:#ddd;margin:4px 0;align-self:stretch;";
  legendEl.appendChild(sep);

  regions.forEach(function (region, i) {
    var color = colors[i % colors.length];
    var item = document.createElement("div");
    item.className = "tidal-legend-item";
    item.innerHTML =
      '<span class="tidal-legend-swatch" style="background:' + color + ';border:1.5px solid ' + color + '"></span>' +
      region.label;
    item.addEventListener("click", function () {
      var bounds = layerBoundsMap[region.key];
      if (bounds) map.fitBounds(bounds.pad(0.15), { animate: true, duration: 0.6 });
    });
    legendEl.appendChild(item);
  });

  var assetBase = window.location.origin + "/assets/tidal/";

  regions.forEach(function (region, i) {
    var color = colors[i % colors.length];
    fetch(assetBase + region.key + "_boundary.geojson")
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var props = data.features[0].properties;

        // Boundary polygon
        var layer = L.geoJSON(data, {
          style: { color: color, weight: 1, opacity: 0.9, fillColor: color, fillOpacity: 0.15 }
        });
        layer.addTo(map);

        // Persistent label marker at top-right of bbox (or below for bottom-positioned regions)
        var isBottom = region.labelPos === "bottom";
        var labelLat = isBottom ? props.lat_min : props.lat_max;
        var labelLon = isBottom
          ? (props.lon_min + props.lon_max) / 2
          : props.lon_max;

        var labelMarker = L.marker([labelLat, labelLon], {
          icon: L.divIcon({ className: "", html: "", iconSize: [0, 0], iconAnchor: [0, 0] }),
          interactive: false
        });
        labelMarker._tidalShortLabel = region.shortLabel;
        labelMarker.bindTooltip(region.shortLabel, {
          permanent: true,
          direction: isBottom ? "bottom" : "top",
          className: "tidal-region-tooltip tidal-tt-" + i,
          offset: [0, 0]
        });
        labelMarker.addTo(map);

        var expandedContent =
          "<strong>" + region.shortLabel + "</strong>" +
          "<div style='margin-top:5px;font-weight:400;line-height:1.7'>" +
          "<span style='color:#666'>Grid Points:</span> " + region.gridPoints + "<br>" +
          "<span style='color:#666'>Period:</span> " + region.period + "<br>" +
          "<span style='color:#666'>Sampling:</span> " + region.sampling +
          "</div>";

        layer.on("click", function (e) {
          L.DomEvent.stopPropagation(e);
          if (expandedMarker && expandedMarker !== labelMarker) {
            expandedMarker.getTooltip().setContent(expandedMarker._tidalShortLabel);
            expandedMarker._tidalExpanded = false;
          }
          if (labelMarker._tidalExpanded) {
            labelMarker.getTooltip().setContent(region.shortLabel);
            labelMarker._tidalExpanded = false;
            expandedMarker = null;
          } else {
            labelMarker.getTooltip().setContent(expandedContent);
            labelMarker._tidalExpanded = true;
            expandedMarker = labelMarker;
          }
        });

        layerBoundsMap[region.key] = layer.getBounds();
        loadedLayers.push(layer);
        loadCount++;
        if (loadCount === regions.length) {
          map.fitBounds(L.featureGroup(loadedLayers).getBounds().pad(0.08));
        }
      })
      .catch(function (err) {
        console.warn("Could not load boundary for " + region.key, err);
        loadCount++;
      });
  });
})();
</script>

## Locations

| Location | Grid Points | Hindcast Period | Sampling |
| -------- | ----------- | --------------- | -------- |
| Aleutian Islands, Alaska | 797,978 | 2010-06-03 – 2011-06-02 | Hourly |
| Cook Inlet, Alaska | 392,002 | 2005-01-01 – 2005-12-31 | Hourly |
| Piscataqua River, New Hampshire | 292,927 | 2007-01-01 – 2007-12-31 | Half-Hourly |
| Salish Sea, Washington | 1,734,765 | 2015-01-01 – 2015-12-30 | Half-Hourly |
| Western Passage, Maine | 231,208 | 2017-01-01 – 2017-12-31 | Half-Hourly |

--8<-- "docs/tidal/high_resolution_hindcast/\_cite-widget.md"

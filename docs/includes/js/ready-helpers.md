function runWhenReady(fn) {
  if (typeof document$ !== "undefined") {
    document$.subscribe(fn);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fn);
  } else {
    fn();
  }
}

function resolveAssetBase(subpath) {
  var base = JSON.parse(document.getElementById("__config").textContent).base;
  return base.replace(/\/$/, "") + "/" + subpath.replace(/^\/+|\/+$/g, "") + "/";
}

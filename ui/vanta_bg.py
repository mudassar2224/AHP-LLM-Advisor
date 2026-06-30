"""
vanta_bg.py  —  Vanta Birds animated background
Injects a full-screen Vanta.js Birds canvas pinned behind Streamlit at z-index -1.

Usage in app.py:
    from ui.vanta_bg import inject_vanta_birds
    inject_vanta_birds()   # call once, near top, after st.markdown(get_css())
"""
import streamlit.components.v1 as components

_DEFAULTS = dict(
    backgroundColor = 0x0d0b1e,
    backgroundAlpha = 1.0,
    color1          = 0x7c3aed,
    color2          = 0xf0abfc,
    colorMode       = "varianceGradient",
    quantity        = 4,
    birdSize        = 1.50,
    wingSpan        = 22.0,
    speedLimit      = 5.0,
    separation      = 30.0,
    alignment       = 60.0,
    cohesion        = 35.0,
    mouseControls   = True,
    touchControls   = True,
    gyroControls    = False,
    minHeight       = 200.0,
    minWidth        = 200.0,
    scale           = 1.0,
    scaleMobile     = 1.0,
)


def _py_to_js(v) -> str:
    if isinstance(v, bool):  return "true" if v else "false"
    if isinstance(v, str):   return f'"{v}"'
    return str(v)


def inject_vanta_birds(**kwargs) -> None:
    cfg      = {**_DEFAULTS, **kwargs}
    js_pairs = ",\n            ".join(f"{k}: {_py_to_js(v)}" for k, v in cfg.items())

    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:100%; height:100%; overflow:hidden; background:#0d0b1e; }}
  #vanta-bg  {{ position:fixed; top:0; left:0; width:100vw; height:100vh; }}
</style>
</head>
<body>
  <div id="vanta-bg"></div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.birds.min.js"></script>
  <script>
    VANTA.BIRDS({{ el:"#vanta-bg", {js_pairs} }});

    // Pin this iframe to cover the full parent viewport at z-index -1
    (function() {{
      try {{
        var me = window.frameElement;
        if (!me) return;
        me.style.cssText = [
          "position:fixed","top:0","left:0",
          "width:100vw","height:100vh",
          "border:none","z-index:-1",
          "pointer-events:none","display:block",
        ].join("!important; ") + "!important;";
        var el = me.parentElement;
        while (el && el !== document.body) {{
          el.style.setProperty("background","transparent","important");
          el.style.setProperty("overflow",  "visible",    "important");
          el.style.setProperty("height",    "0px",        "important");
          el = el.parentElement;
        }}
      }} catch(e) {{}}
    }})();
  </script>
</body>
</html>"""
    components.html(html, height=1, scrolling=False)

<!DOCTYPE html>
<html>
<head>
<style>
  body, html {
    margin: 0;
    padding: 0;
    width: 100%;
    min-height: 100vh;
    overflow-x: hidden;
  }
  .fullpage-container {
    width: 100%;
    max-width: 100%;
    padding: 0;
    margin: 0;
    text-align: center;
  }
  .fullwidth-image {
    width: 100%;
    height: auto;
    max-width: none;
    display: block;
    margin: 0;
    padding: 0;
  }
  .clickable-area {
    position: absolute;
    /* background-color: rgba(255, 0, 0, 1); */
    cursor: pointer;
  }

</style>
</head>
<body>
    <div class="fullpage-container" style="position: relative; width: 100%; height: auto;">
        <img class="fullwidth-image" src="assets/HACKATON_3DIFY.png" alt="Fullpage image example">
        <a href="https://example.com/area1" class="clickable-area" style="top: 23%; left: 7%; width: 85%; height: 2%;"></a>
        <a href="https://example.com/area1" class="clickable-area" style="top: 44%; left: 7%; width: 85%; height: 2%;"></a>
        <a href="https://example.com/area1" class="clickable-area" style="top: 46.8%; left: 7%; width: 85%; height: 2%;"></a>
        <a href="https://example.com/area1" class="clickable-area" style="top: 96.25%; left: 7%; width: 85%; height: 2%;"></a>
    </div>
</body>
</html>
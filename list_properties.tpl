<!DOCTYPE html>
<html>
    <head>
        <title>Prosa Project Management</title>
        <link type="text/css" rel="stylesheet" href="/prosa/static/styles.css" />
        <script src="/prosa/static/functions.js" defer></script>
    </head>
    <body class="no-flex">
        <select id="properties" size=10 class="list-select" multiple>
            {{!properties}}
        </select>
        <br>
        <a href="#" class="button-blue" onclick="sendSelectedItemsToParent('properties')">Ok</a>
    </body>
</html>

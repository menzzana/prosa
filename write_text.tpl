<!DOCTYPE html>
<html>
    <head>
        <title>Prosa Project Management</title>
        <link type="text/css" rel="stylesheet" href="/prosa/static/styles.css" />
        <script src="/prosa/static/functions.js" defer></script>
    </head>
    <body class="no-flex">
        <textarea  id="project_txt" rows="10" cols="50">{{!text_data}}</textarea>
        <br>
        <a href="#" class="button-blue" onclick="sendSelectedItemsToParent('project_txt')">Save</a>
    </body>
</html>

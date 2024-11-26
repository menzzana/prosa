<html>
    <head>
        <title>Prosa Project Management</title>
        <link type="text/css" rel="stylesheet" href="/prosa/static/styles.css" />
    </head>
    <body>
        {{!menu}}
        <div class="div2">
            <h1>Tags</h1>
            {{!rows}}
            <hr>
            <form action="tags.py/add_tag" method="post">
                Tag: <input name="tag" type="text" /><br><br>
                <input value="Add tag" type="submit" />
            </form>
            <hr>
            <form action="tags.py/add_value" method="post">
                <select name="tags" size=10 class="list-select">
                    {{!tags}}
                </select><br><br>
                Tag value: <input name="tagvalue" type="text" /><br><br>
                <input value="Add tag value" type="submit" />
            </form>
            <hr>
        </div>
    </body>
</html>

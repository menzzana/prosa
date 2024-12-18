<html>
    <head>
        <title>Prosa Project Management</title>
        <link type="text/css" rel="stylesheet" href="/prosa/static/styles.css" />
    </head>
    <body>
        {{!menu}}
        <div class="div2">
            <h1>Properties</h1>
            {{!rows}}
            <hr>
            <form action="props.py/add_property" method="post">
                Property: <input name="property" type="text" /><br><br>
                <input value="Add property" type="submit" />
            </form>
            <hr>
            <form action="props.py/add_value" method="post">
                <select name="props" size=10 class="list-select">
                    {{!props}}
                </select><br><br>
                Property value: <input name="property_value" type="text" /><br><br>
                <input value="Add property value" type="submit" />
            </form>
            <hr>
        </div>
    </body>
</html>

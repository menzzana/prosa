<html>
    <head>
        <title>Prosa Project Management</title>
        <link type="text/css" rel="stylesheet" href="/prosa/static/styles.css" />
    </head>
    <body>
        {{!menu}}
        <div class="div2">
            <h1>Projects</h1>
            <select name="projects" size=10 class="list-select">
                {{!projects}}
            </select><br><br>
            <form action="projects.py/add_project" method="post">
                Project: <input name="project" type="text" /><br><br>
                Description:<br>
                <textarea name="description" rows="10" cols="50"></textarea><br>
                <input value="Add project" type="submit" />
            </form>
            <hr>
        </div>
    </body>
</html>

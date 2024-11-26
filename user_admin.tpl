<html>
    <head>
        <title>Prosa Project Management</title>
        <link type="text/css" rel="stylesheet" href="/prosa/static/styles.css" />
    </head>
    <body>
        {{!menu}}
        <div class="div2">
            <h1>Users</h1>
            <form action="user_admin.py/delete_user" method="post">
                <select name="users" size=10 class="list-select">
                    {{!users}}
                </select><br><br>
                <input value="Delete" type="submit" />
            </form>
            <hr>
            <form action="user_admin.py/add_user" method="post">
                E-mail: <input name="email" type="text" /><br><br>
                Full name: <input name="full_name" type="text" /><br><br>
                Password: <input name="password" type="password" /><br><br>
                Administrator: <input name="administrator" type="checkbox"><br><br>
                <input value="Create" type="submit" />
            </form>
        </div>
    </body>
</html>

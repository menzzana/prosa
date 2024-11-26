<html>
    <head>
        <title>Prosa Project Management</title>
        <link type="text/css" rel="stylesheet" href="/prosa/static/styles.css" />
        <script src="/prosa/static/functions.js" defer></script>
    </head>
    <body>
        {{!menu}}
        <div class="div2">
            <b>Group by:</b>
            <select name="groupby" class="dropdown-select" onchange="navigateToUrl('{{!baseurlgroup}}',this)">
                {{!groupby}}
            </select>
            <b>Order by:</b>
            <select name="orderby" class="dropdown-select" onchange="navigateToUrl('{{!baseurlorder}}',this)">
                {{!orderby}}
            </select>
            <br><br>

            {{!rows}}
        </div>
    </body>
</html>

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
                <option value=0>None</option>
                {{!groupby}}
            </select>
            <b>Order by:</b>
            <select name="orderby" class="dropdown-select" onchange="navigateToUrl('{{!baseurlorder}}',this)">
                <option value=0>None</option>
                {{!orderby}}
            </select>
            <b>Add property:</b>
            <select name="property" class="dropdown-select" onchange="navigateToUrl('{{!baseurlproperty}}',this)">
                <option value=0>None</option>
                {{!propertyby}}
            </select>
            <br><br>
            {{!rows}}
        </div>
    </body>
</html>

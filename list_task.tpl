<html>
    <head>
        <title>Prosa Project Management</title>
        <link type="text/css" rel="stylesheet" href="/prosa/static/styles.css" />
        <script src="/prosa/static/functions.js" defer></script>
    </head>
    <body>
        {{!menu}}
        <div class="div2">
            <b>Project:</b>
            <select name="projectby" class="dropdown-select" onchange="navigateToUrl('{{!baseurlproject}}',this)">
                <option value=0>All</option>
                {{!projectby}}
            </select>        
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
            <a href="#" class="button-blue" onclick="openWindowAtPointer(event, '{{!baseurlproperty}}','list_properties.py?property=', 200, 400);return false;">Properties</a>
            <br><br>
            {{!rows}}
        </div>
    </body>
</html>

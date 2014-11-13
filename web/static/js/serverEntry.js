var serverEntrySource = "" +
    "<div class='server panel panel-default'>" +
        "<div class='server-title panel-heading'>" +
            "<h3 class='panel-title'>Server</h3>" +
        "</div>" +
        "<div class='panel-body'>" +
            "<div class='form-group'>" +
                "<label for='servername' class='col-lg-2 control-label'>Server Name</label>" +
                "<div class='col-lg-10'>" +
                    "<input type='text' class='form-control' name='servername' placeholder='Freenode' value='{{server.name}}'>" +
                "</div>" +
            "</div>" +
            "" +
            "<div class='form-group'>" +
                "<label for='serveraddress' class='col-lg-2 control-label'>Server Address</label>" +
                "<div class='col-lg-10'>" +
                    "<input type='text' class='form-control' name='serveraddress' placeholder='irc.freenode.net' value='{{server.address}}'>" +
                "</div>" +
            "</div>" +
            "" +
            "<div class='form-group'>" +
                "<label for='nickname' class='col-lg-2 control-label'>Nickname</label>" +
                "<div class='col-lg-10'>" +
                    "<input type='text' class='form-control' name='nickname' value='{{nickname}}'>" +
                "</div>" +
            "</div>" +
            "" +
            "<div class='form-group'>" +
                "<label for='ident' class='col-lg-2 control-label'>Ident</label>" +
                "<div class='col-lg-10'>" +
                    "<input type='text' class='form-control' name='ident' value='{{ident}}'>" +
                "</div>" +
            "</div>" +
        "</div>" +
    "</div>" +
"";
var serverEntryTemplate = Handlebars.compile(serverEntrySource);

function addServer(serverEntryData, serversListElement) {
    var serverContainer = document.createElement('div');
    serverContainer.className = 'server-container-initial';

    var serverEntry = serverEntryTemplate(serverEntryData);

    serverContainer.innerHTML = serverEntry;
    serversListElement.appendChild(serverContainer);
    setTimeout(function() {
        serverContainer.className += ' server-container-transition';
    }, 100);
}

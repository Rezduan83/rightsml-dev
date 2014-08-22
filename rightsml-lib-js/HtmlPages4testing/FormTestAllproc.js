﻿/// <reference path="../ODRLclasses.ts"/>
/// <reference path="../ODRLvocabs.ts"/>
/// <reference path="../RightsMLvocabs.ts"/>
/**
* development timestamp: 2014-06-24
* development by Michael W. Steidl (www.linkedin.com/in/michaelwsteidl)
*
* This module provides functions for processing the FormTest HTML pages
*
*/
function processForm() {
    var policy1 = new Odrl.Policy("http://iptc.org/std/RightsML/demos/policy007", "set");
    var perm1 = new Odrl.Permission();
    var action = getRBvalueTestAll("relinput1", "grAction");
    var targetAsset = document.forms["relinput1"]["targetasset"].value;
    var assigner = document.forms["relinput1"]["assignerParty"].value;
    var assignee = document.forms["relinput1"]["assigneeParty"].value;
    perm1.setAction(action).addAsset(targetAsset, Odrl.AssetRelationsCV.target).addParty(assigner, Odrl.PartyRolesCV.assigner, Odrl.PartyRoleScopesCV.individual).addParty(assignee, Odrl.PartyRolesCV.assignee, Odrl.PartyRoleScopesCV.individual);

    policy1.addPermission(perm1);

    // make the object ready for display: in XML first
    var xmlStr = policy1.serializeXml();
    xmlStr = xmlStr.replace(/</g, "&lt;").replace(/>/g, "&gt;");

    // xmlStr = xmlStr.replace(/>/g, "&gt;");
    var outStr = "<pre>" + xmlStr + "</pre>";
    var xel = document.getElementById('content1');
    xel.innerHTML = "<h2>Example in XML</h2>" + outStr;

    // ... and now in JSON
    var jel = document.getElementById('content2');
    outStr = policy1.serializeJson();
    jel.innerHTML = "<h2>Example in JSON</h2><pre>" + outStr + "</pre>";
}

function getRBvalueTestAll(form, rbgroup) {
    var rbvalue = "";
    var len = document.forms[form][rbgroup].length;
    var i;
    for (i = 0; i < len; i++) {
        if (document.forms[form][rbgroup][i].checked) {
            rbvalue = document.forms[form][rbgroup][i].value;
            break;
        }
    }
    return rbvalue;
}
//# sourceMappingURL=FormTestAllproc.js.map

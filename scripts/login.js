const fetch = require('node-fetch');
const fs = require('fs');
const personal = require('./personal.js');
const parse = require('node-html-parser').parse;
const he = require('he');
/*
    Must have a personal.js in the scripts directory.
    Example:

        module.exports = { username: "email", password: "password" };
*/
fetch("https://api.turnitin.com/login_page.asp?lang=en_us", {
    "headers": {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": "\"Chromium\";v=\"85\", \"\\\\Not;A\\\"Brand\";v=\"99\", \"Microsoft Edge\";v=\"85\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    },
    "referrer": "https://api.turnitin.com/login_page.asp?lang=en_us",
    "referrerPolicy": "no-referrer-when-downgrade",
    "body": `javascript_enabled=0&email=${personal.username}&user_password=${personal.password}&submit=Log+in`,
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
}).then(response => {
    return response.text().then(text => {
        const document = parse(text);
        const classes = document.querySelectorAll(".class_name");
        classes.forEach(link => {
            link = link.querySelectorAll("a")[0];
            if (link == null || link.innerHTML == null || link.attributes.href == null) {
                return;
            }
            link = {
                title: he.decode(link.innerHTML),
                url: link.attributes.href
            };
            console.log(link);
        });
    });
});
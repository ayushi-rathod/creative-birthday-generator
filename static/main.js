// let serverx = 'http://127.0.0.1:5001'
var serverx = ''
/**
 * 
 * @param {string} fileName (album + filename) filename to save as, wrapped in folder. where album is uniquelink
 * @param {string} AWSAccessKeyId pass as is from get signed url
 * @param {string} policy pass as is from get signed url
 * @param {string} signature pass as is from signed url
 * @param {File} fileInput FileObject
 */
function uploadPhoto(fileName, AWSAccessKeyId, policy, signature, fileInput) {
    if (fileName === undefined || AWSAccessKeyId === undefined || policy === undefined || signature === undefined || fileInput === undefined) {
        console.log("uploadPhoto FOUND EMPTY", fileName, AWSAccessKeyId, policy, signature, fileInput);
        console.log(fileInput);
        return;
    }
    return new Promise((resolve, reject) => {
        // console.log(fileInput)
    
        var form = new FormData();
        form.append("acl", "public-read");
        form.append("key", fileName);
        form.append("AWSAccessKeyId", AWSAccessKeyId);
        form.append("policy", policy);
        form.append("signature", signature);
        form.append("file", fileInput);

        var settings = {
            url: "https://birthday-engine.s3.amazonaws.com/",
            method: "POST",
            processData: false,
            contentType: false,
            data: form,
            statusCode: {
                204: function (data) {
                    console.log("Request completed 204");
                    resolve(data || { statusCode: 204});
                }
            }
        };

        $.ajax(settings)
    });
}

function getSignUrl(name) {
    return new Promise((resolve, reject) => {
        getUrl = {
            url: serverx+"/signed-url-s3",
            method: "GET",
            data: {
                "name": name
            },
            statusCode: {
                200: function (data) {
                    console.log("Request completed 200");
                    resolve(data || {statusCode: 200});
                }
            }
        }
        
        $.ajax(getUrl)
    });
}

function getUniqueLink(
    bday_email, bday_name, bday_date, bday_photo, user_name, user_email, user_greetings, user_photo
) {
    return new Promise((resolve, reject) => {
        var settings = {
                "url": serverx+"/genlink",
                "method": "POST",
                "timeout": 0,
                "headers": {
                "Content-Type": "application/json"
                },
            "data": JSON.stringify({
                "bday_email": bday_email,
                "bday_name": bday_name,
                "bday_date": bday_date,
                "bday_photo": bday_photo,
                "user_name": user_name,
                "user_email": user_email,
                "greeting": user_greetings,
                "user_photo": user_photo
            }),
            "statusCode": {
                200: function (data) {
                    console.log("Request completed 200");
                    resolve(data || {statusCode: 200});
                }, 
                201: function (data) {
                    console.log("Request completed 201: Birthday user already has a link.");
                    resolve(data || {statusCode: 201});
                }
            }
        };

        $.ajax(settings).done( function (data) {
            console.log("Generated unique link dataL:", data)
        });
    });
}

function saveUserInfo(url, bday_photo, user_name, user_email, greeting, user_photo) {
    return new Promise((resolve, reject) => {
        var set = {
            "url": url,
            "method": "POST",
            "timeout": 0,
            "headers": {
            "Content-Type": "application/json"
            },
            "data": JSON.stringify(
                {
                    "bday_photo": bday_photo,
                    "user_name": user_name,
                    "user_email": user_email,
                    "greeting": greeting,
                    "user_photo": user_photo
                }),
        };

        $.ajax(set);
    }); 
}

function triggerUrl(name) {
    
    return new Promise((resolve, reject) => {
        getUrl = {
            url: serverx+"/trigger",
            method: "GET",
            data: {
                "name": name
            },
            statusCode: {
                200: function (data) {
                    console.log("Request completed 200");
                    $("#greetingUrl").text('');
                    $("#greetingUrl").append(
                        "<a style=\" color: brown\; font-size: medium\; border: blueviolet solid 4px\;\" href=\""+ data['link'] +"\">Click here for the awesomeness!!! </a>"
                    )
                    $('#greetingGif').attr('src', data['link']);
                    resolve(data || {statusCode: 200});
                }
            }
        }
        
        $.ajax(getUrl)
        coolStuffRoll('#send_btn')
        

    });
}


function coolStuffRoll(id) {
    // $(id).attr('Value', "Creating.");
    // $(id).attr('Value', "Some..");
    // $(id).attr('Value', "Charm...");
    setTimeout(function(){
        $(id).attr('Value', "Creating.");
    }, 10);
    setTimeout(function(){
        $(id).attr('Value', "Some..");
    }, 10);
    setTimeout(function(){
        $(id).attr('Value', "Charm...");
    }, 10);

}

/**
 * @example usage
 * getUrlParam.get('paramname')
 */
function getUrlParam() {
    return new window.URLSearchParams(window.location.search);
}

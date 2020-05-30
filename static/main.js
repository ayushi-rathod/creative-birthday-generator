
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
        console.log(fileInput)
    
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
            url: "http://127.0.0.1:5001/signed-url-s3",
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
                url: "http://127.0.0.1:5001/genlink",
                method: "POST",
                timeout: 0,
                headers: {
                contentType: "application/json"
            },
            data: JSON.stringify({
                "bday_email": bday_email,
                "bday_name": bday_name,
                "bday_date": bday_date,
                "bday_photo": bday_photo,
                "user_name": user_name,
                "user_email": user_email,
                "greeting": user_greetings,
                "user_photo": user_photo
            }),
            statusCode: {
                200: function (data) {
                    console.log("Request completed 200");
                    resolve(data || {statusCode: 200});
                }
            }
        };

        $.ajax(settings);
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
/**
 * @example usage
 * getUrlParam.get('paramname')
 */
function getUrlParam() {
    return new window.URLSearchParams(window.location.search);
}
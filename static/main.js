
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

/**
 * @example usage
 * getUrlParam.get('paramname')
 */
function getUrlParam() {
    return new window.URLSearchParams(window.location.search);
}
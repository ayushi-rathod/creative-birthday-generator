
/**
 * 
 * @param {string} fileName (album + filename) filename to save as, wrapped in folder. where album is uniquelink
 * @param {string} AWSAccessKeyId pass as is from get signed url
 * @param {string} policy pass as is from get signed url
 * @param {string} signature pass as is from signed url
 * @param {File} fileInput FileObject
 */
function uploadPhoto(fileName, AWSAccessKeyId, policy, signature, fileInput) {
    var form = new FormData();
    form.append("acl", "public-read");
    form.append("key", fileName);
    form.append("AWSAccessKeyId", AWSAccessKeyId);
    form.append("policy", policy);
    form.append("signature", signature);
    form.append("file", fileInput.files);

    var settings = {
    url: "https://birthday-engine.s3.amazonaws.com/",
    method: "POST",
    processData: false,
    contentType: false,
    data: form
    };

    $.ajax(settings).done(function (response) {
    console.log(response);
    });
    
}

/**
 * @example usage
 * getUrlParam.get('paramname')
 */
function getUrlParam() {
    return new window.URLSearchParams(window.location.search);
}
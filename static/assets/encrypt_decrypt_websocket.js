function send_data(data, key, encrypt) {
    $.ajax({
        type: "POST",
        url: "/api/" + (encrypt == true ? "encrypt" : "decrypt"),
        data: '{"data":"' + btoa(data) + '", "key":"' + btoa(key) + '", "method":"' + (encrypt == true ? "encrypt" : "decrypt") + '"}',
        contentType: "application/json; charset=utf-8",
        dataType: "json"
      }).done(done).fail(fail);
}

function done(data) {
    $("#data-to-encrypt").val(data["result"]);
}

function fail(data) {
    console.log("Error details: " + data);
    $("#error-message").text(data.responseText);
}
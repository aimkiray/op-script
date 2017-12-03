var form = $("<form></form>");
form.attr('action', '/cloud/open');
form.attr('method', 'post');
var params = {
    "vm_id": 70360,
    "x": 11,
    "y": 11
};
for (var key in params) {
    var input = $("<input type='hidden' name='" + key + "' />");
    input.attr('value', params[key]);
    form.append(input);
}
form.appendTo("body");
form.css('display', 'none');
form.submit();


        var form = $("<form></form>");
        form.attr('action', '/cloud/open');
        form.attr('method', 'post');
        form.attr('onsubmit', 'ShowLoading()');
        var params = {
            "plan": "Plan 01",
            "csrf_token": b857c52ea6e6019932c910250d55b34fbc2c7163,
            "vm_id": 70360,
            "location": local,
            "os": "linux-centos-7.1503.01-x86_64-minimal-gen2-v1",
            "hostname": "cat.neko",
            "root": ""
        };
        for (var key in params) {
            var input = $("<input type='hidden' name='" + key + "' />");
            input.attr('value', params[key]);
            form.append(input);
        }
        form.appendTo("body");
        form.css('display', 'none');
        form.submit();
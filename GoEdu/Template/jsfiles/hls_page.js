function chatroom_connect() {
    if (window.s) {
        window.s.close()
    }
    /*创建socket连接*/
    addr = "ws://"+window.location.host+"/GoLearing/hls/echo/{{schoolname}}/{{classname}}/"
    /*addr = "ws://"+window.location.host+"/GoLearing/hls/echo/"*/
    var socket = new WebSocket(addr);
    socket.onopen = function () {
        console.log('WebSocket open');//成功连接上Websocket
    };
    socket.onmessage = function (e) {
        console.log('message: ' + e.data);//打印出服务端返回过来的数据
        $('#messagecontainer').prepend('<p>' + e.data + '</p>');
    };
    // Call onopen directly if socket is already open
    if (socket.readyState == WebSocket.OPEN) socket.onopen();
    window.s = socket;
}

function chatroom_send() {
    //如果未连接到websocket
    if (!window.s) {
        alert("websocket未连接.");
    } else {
        window.s.send($('#message').val());//通过websocket发送数据
    }
}

function chatroom_close() {
    if (window.s) {
        window.s.close();//关闭websocket
        console.log('websocket已关闭');
    }
}


function file_upload(is_index)
{
    var form_data = new FormData();
    if (is_index == "no")
    {
        var file_name = document.getElementById('file_upload').files[0];
        form_data.append('filename',file_name);
    }
    $.ajax({
        type:'POST',
        url :'/GoLearing/hls/{{schoolname}}/{{classname}}/',
        data:form_data, 
        contentType:false,
        processData:false,
        mimeType:"multipart/form-data",
        error:function()
        {
            alert('请求失败');
        },
        success:function(arg)
        {
            val = JSON.parse(arg).Courseware_name;
            $('#upul').empty();
            for (var inode=0; inode<val.length; inode++)
            {
                $('#upul').append('<li id="upli"><a href="/GoLearing/hls/download/{{schoolname}}/{{classname}}/'+val[inode]+'/" >'+val[inode]+'</a></li>');	
            }
        }
    });
}

$(document).ready(function()
    {
        file_upload("yes");
        $('#connect_websocket').click(function () {
            chatroom_connect();
    });
        $('#send_message').click(function () {
            chatroom_send();
    });
        $('#close_websocket').click(function () {
            chatroom_close();
    });
})

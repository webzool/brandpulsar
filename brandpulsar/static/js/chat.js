// Written with JS and jQuery. Gets socket data and appends to the template
// Author : Arzu Hussein.

const user = JSON.parse(document.getElementById('user').textContent);

// Socket connection function. 
// dynamic routing
// 
function startSocket(socket) {
    socket.onopen = function (e) {
        console.info('Access granted');
    };
    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data['type'] === 'chat_user_list_response') {
            cleanUserList();
            let groups = data.data.groups;
            for (let group in groups) {
                getUserList(groups[group]);
            }
        };
        if (data['type'] === 'group_messages_response') {
            cleanRoomMessages();
            getMessageList(data.data);
        };
        if (data.message) {
            let type = 'sent';
            if (data.message[0].fields.user === user) {
                type = 'replies';
            }
            newMessage(message = data.message[0].fields.body, type = type);
        };
    };
    socket.onclose = function (e) {
        console.error('Chat socket closed');
    };
    $('.submit').on('click', function () {
        const messageInputDom = $(".message-input input");
        const message = messageInputDom.val();
        socket.send(JSON.stringify({
            'type': 'chat_message_send',
            'data': message,
        }));
        socket.send(JSON.stringify({
            'type': 'chat_user_list_response'
        }));
    });
}

// Helper functions
//

function newMessage(message, type, animate = true) {
    if ($.trim(message) == '') {
        return false;
    }
    $(`<li class="${type}">
        <img src="http://emilcarlsson.se/assets/mikeross.png"alt=""/>
        <p>${message}</p>
        </li>`).appendTo($('.messages ul'));

    $('.message-input input').val(null);
    $('.contact.active .preview').html(`${message}`);
    if (animate) {
        $(".messages").animate({ scrollTop: $(document).height() }, "slow");
    }
};

function getMessageList(list) {
    if (user === list.owner.pk) {
        $('.contact-profile').html(`<p>${list.member.full_name}</p>`);
    } else {
        $('.contact-profile').html(`<p>${list.owner.full_name}</p>`);
    }
    for (let message in list.messages) {
        let data = list.messages[message];
        let type = 'sent';
        if (data.user_pk === user) {
            type = 'replies'
        }
        newMessage(data.body, type, animate = false);
    }
    $(".messages").animate({ scrollTop: $(document).height() }, "slow");
}


// jQuery functions
//
function getUserList(args) {
    const data = args['data'];
    console.log(`${data.latest_message} - debug`);
    let contact = '';
    if (user === data.owner.pk) {
        contact = data.member;
    } else {
        contact = data.owner;
    }

    let unreads = '';
    if (args['unread_messages_count'] > 0) {
        unreads = `<span id="unreads">${args['unread_messages_count']}</span>`;
    }

    $(`<li member="${data.member.pk}" room="${data.domain[0].fields.slug}" onclick="SocketConn()" class="contact">
        <div class="wrap d-flex align-items-center">
            <img src="http://emilcarlsson.se/assets/louislitt.png" alt="" />
            <div class="meta">
                <p class="name text-white">${contact.full_name} for ${data.domain[0].fields.name}
                    ${unreads}
                </p>
                <p class="preview text-white"><small>12/12/2020</small> ${data.latest_message}</p>
            </div>
        </div>
    </li>`).appendTo($('#contacts ul'));
};

function cleanUserList() {
    $('#contacts ul').empty();
}

function cleanRoomMessages() {
    $('.messages ul').empty();
}

function toggleActive(c) {
    $(c).addClass('active');
    $(c).siblings().removeClass('active');
}

function cleanUnreads(c) {
    $(c).find('#unreads').hide();
}

function activateInputs() {
    $(".wrap input").prop('disabled', false);
    $(".wrap button").prop('disabled', false);
}

$('.message-input input').focus();
$('.message-input input').keyup(function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('.submit').click();
    }
});


$(window).on('keydown', function (e) {
    if (e.which == 13) {
        newMessage();
        return false;
    }
});

// Start
let homeSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
);

startSocket(homeSocket);

// Updates Socket Connection to group layers (chat rooms)
function SocketConn() {
    member = $(event.currentTarget).attr('member');
    room = $(event.currentTarget).attr('room');

    toggleActive(event.currentTarget);
    cleanUnreads(event.currentTarget);
    activateInputs();

    homeSocket.send(JSON.stringify({
        'type': 'assign_chat_room',
        'data': {
            'room': room,
            'member': member,
        },
    }))
};
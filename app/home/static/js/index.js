$(document).ready(function() {
  // SOCKETS //
  function init() {
    socket = io.connect("http://127.0.0.1:5000");
  }

  function connect() {
    // on connection to socket
    socket.on("connect", function() {
      socket.emit("connect user", { datetime: datetime() });
    });
  }

  function receive_messages() {
    // receives messages from server
    socket.on("message", function(msg) {
      $("#messageDisplay > ul").append("<li>" + msg + "</li>");
    });
  }

  init();
  connect();
  receive_messages();

  // if user hits enter key, then triggers submit button
  $("#message").keypress(function(e) {
    if ((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13)) {
      $("#send-message").click();
      return false;
    } else {
      return true;
    }
  });

  // if user clicks submit button
  $("#send-message").on("click", function() {
    var msg = $("#message");
    if (msg.val() && msg.val() != "Message cannot be empty!") {
      socket.emit("message", { message: msg.val(), datetime: datetime() });
      msg.val("");
      scrollBottom();
    } else {
      // adds message below to input to notify user
      msg.val("Message cannot be empty!");
    }
  });

  // END SOCKETS //

  // DATETIME //
  function datetime() {
    var datetime = moment().format("MM/DD/YYYY hh:mm a");

    return datetime;
  }

  // auto scroll to bottom of message display //
  function scrollBottom() {
    $("#messageDisplay").scrollTop(
      $("#messageDisplay")[0].scrollHeight
    );
  }
});

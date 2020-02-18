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

    // callback
    socket.on("on connect", function(response) {
      let user = response["user"];
      let message = response["message"];
      let datetime = response["dt"];
      $("#messageDisplay > ul").append(
        "<li>" +
          "<span class='li-user'>" +
          user + " " +
          "</span>" +
          message +
          " - " +
          "<span class='li-dt'>" +
          datetime +
          "</span>" +
          "</li>"
      );
    });
  }

  function receive_messages() {
    // receives messages from server
    socket.on("receive message", function(response) {
      let user = response["user"];
      let message = response["message"];
      let datetime = response["dt"];

      $("#messageDisplay > ul").append(
        "<li>" +
          "<span class='li-user'>" +
          user +
          "</span>" +
          ": " +
          message + " - " +
          "<span class='li-dt'>" +
          datetime +
          "</span>" +
          "</li>"
      );
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
    $("#messageDisplay").scrollTop($("#messageDisplay")[0].scrollHeight);
  }
});

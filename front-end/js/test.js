(function () {
  "use strict";

  /**
   * Test the user API.
   * @private
   */
  function testUserAPI() {
    console.log("Test User API");
    $.ajax({
      url: "http://localhost:5000/user/",
      type: "POST",
      data: JSON.stringify({
        "client_id": createClientId()
      }),
      contentType: "application/json",
      dataType: "json",
      success: function (data) {
        console.log(data);
      },
      error: function (xhr) {
        console.error(xhr);
      }
    });
  }

  /**
   * Create a client ID.
   * @private
   * @returns {string} - the created unique client ID.
   */
  function createClientId() {
    return "custom.cid." + new Date().getTime() + "." + Math.random().toString(36).substring(2);
  }

  /**
   * Initialize the page.
   * @private
   */
  function init() {
    $("#test-user-api").on("click", function () {
      testUserAPI();
    });
  }
  $(init);
})();
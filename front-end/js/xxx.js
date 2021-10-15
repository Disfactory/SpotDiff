(function () {
  "use strict";

  /**
   * Callback function when the XXX is ready.
   * @callback ready
   * @param {Object} xxxObj - XXX object (in xxx.js).
   */

  /**
   * Callback function when the XXX is failing.
   * @callback fail
   * @param {string} message - the reason why the XXX is failing.
   */

  /**
   * Class for XXX (this is a template for a class).
   * @public
   * @class
   * @param {Object.<string, *>} [settings] - XXX settings.
   * @param {ready} [settings.ready] - callback function when the XXX is ready.
   * @param {fail} [settings.fail] - callback function when the XXX is failing.
   */
  var XXX = function (settings) {
    settings = safeGet(settings, {});
    var ready = settings["ready"];
    var fail = settings["fail"];
    var thisObj = this;

    /**
     * A helper for getting data safely with a default value.
     * @private
     * @param {*} v - the original value.
     * @param {*} defaultVal - the default value to return when the original one is undefined.
     * @returns {*} - the original value (if not undefined) or the default value.
     */
    function safeGet(v, defaultVal) {
      if (typeof defaultVal === "undefined") defaultVal = "";
      return (typeof v === "undefined") ? defaultVal : v;
    }

    /**
     * Example of a private function.
     * @private
     */
    function privateFunction() {
      console.log("private function");
    }

    /**
     * Example of a public function.
     * @public
     */
    this.publicFunction = function () {
      console.log("public function");
    };

    /**
     * Example of another public function.
     * @public
     */
    var anotherPublicFunction = function () {
      console.log("another public function");
    };
    this.anotherPublicFunction = anotherPublicFunction;

    /**
     * Class constructor.
     * @constructor
     * @private
     */
    function XXX() {
      privateFunction();
      anotherPublicFunction();
      if (typeof ready === "function") ready(thisObj);
      if (typeof fail === "function") fail("XXX initialization error.");
    }
    XXX();
  };

  // Register the class to window
  if (window.project) {
    window.project.XXX = XXX;
  } else {
    window.project = {};
    window.project.XXX = XXX;
  }
})();
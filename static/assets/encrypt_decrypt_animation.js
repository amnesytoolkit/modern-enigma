/*
    Copy and pasted from some StackOverflow answer. We are not the author of this.
    Credit goes to the respective author.
*/

jQuery.fn.decodeEffect = (function ($) {
  var defaultOptions = {
      duration:      500,
      stepsPerGlyph: 5,
      codeGlyphs:    "ABCDEFGHIJKLMNOPQRSTUWVXYZ1234567890abcdefghijkmlnopqrstuvxyz~`+-/|=_.,!@#$%^&*><?",
      className:     "code"
  };
  
  // get a random string from the given set,
  // or from the 33 - 125 ASCII range
  function randomString(set, length) {
      var string = "", i, glyph;
      for(i = 0 ; i < length ; i++) {
          glyph = Math.random() * set.length;
          string += set[glyph | 0];
      }
      return string;
  }
  
  // this function starts the animation. Basically a closure
  // over the relevant vars. It creates a new separate span
  // for the code text, and a stepper function that performs
  // the animation itself
  function animate(element, options) {
      var text = element.text(),
          span = $("<span/>").addClass(options.className).insertAfter(element),
          interval = options.duration / (text.length * options.stepsPerGlyph),
          step = 0,
          length = 0,
          stepper = function () {
              if(++step % options.stepsPerGlyph === 0) {
                  length++;
                  element.text(text.slice(0, length));
              }
              if(length <= text.length) {
                  span.text(randomString(options.codeGlyphs, text.length - length));
                  setTimeout(stepper, interval);
              } else {
                  span.remove();
              }
          };
      element.text("");
      stepper();
  }
  
  // Basic jQuery plugin pattern
  return function (options) {
      options = $.extend({}, defaultOptions, (options || {}));
      return this.each(function () {
          animate($(this), options);
      });
  };
}(jQuery));

$("#insert-text").decodeEffect();
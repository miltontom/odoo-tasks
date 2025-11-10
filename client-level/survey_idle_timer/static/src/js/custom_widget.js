import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CustomWidget = publicWidget.Widget.extend({
  selector: ".o_survey_form",
  events: { "click .btn-primary[value='start']": "_func" },

  start: function () {
    this.options = this.$("form").data();
  },

  _func: function () {
    var timeLimit = this.options.questionTimeLimitSeconds;
    var timeLimitCopy = timeLimit;
    var timer = $(document).find(".o_survey_timer_container");

    setInterval(function () {
      if (timeLimit < 0) {
        timeLimit = timeLimitCopy;

        var start = $(".btn-primary[value='start']");
        var next = $(".btn-primary[value='next']");
        var finish = $(".btn-secondary[value='finish']");

        if (start.length) {
          start.trigger("click");
        } else if (next.length) {
          next.trigger("click");
        } else if (finish.length) {
          finish.trigger("click");
        }
      }
      timer.html(timeLimit);
      timeLimit--;
    }, 1000);
  },
});

export default publicWidget.registry.CustomWidget;

$(function () {
  $("#createNewUser").submit(function () {
    event.preventDefault();
    $("button").attr("disabled", true);
    $("button", this).html(
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span><span class="sr-only">Uploading...</span>'
    );
    $.ajax({
      url: "/api/exercise/new-user",
      type: "post",
      data: getFormDataObject("createNewUser"),
      success: function (result) {
        displayResult(result);
        $("#createNewUser button").html("POST");
        $("button").removeAttr("disabled");
      },
    });
  });

  $("#getAllUsers").submit(function () {
    event.preventDefault();
    $("button").attr("disabled", true);
    $("button", this).html(
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span><span class="sr-only">Uploading...</span>'
    );
    $.ajax({
      url: "/api/exercise/users",
      type: "get",
      success: function (result) {
        displayResult(result);
        $("#getAllUsers button").html("GET");
        $("button").removeAttr("disabled");
      },
    });
  });

  $("#addExercise").submit(function () {
    event.preventDefault();
    $("button").attr("disabled", true);
    $("button", this).html(
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span><span class="sr-only">Uploading...</span>'
    );
    $.ajax({
      url: "/api/exercise/add",
      type: "post",
      data: getFormDataObject("addExercise"),
      success: function (result) {
        displayResult(result);
        $("#addExercise button").html("POST");
        $("button").removeAttr("disabled");
      },
    });
  });

  $("#getLog").submit(function () {
    event.preventDefault();
    $("button").attr("disabled", true);
    $("button", this).html(
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span><span class="sr-only">Uploading...</span>'
    );
    $.ajax({
      url: "/api/exercise/log?" + $("#getLog").serialize(),
      type: "get",
      success: function (result) {
        displayResult(result);
        $("#getLog button").html("GET");
        $("button").removeAttr("disabled");
      },
    });
  });

  function getFormDataObject(formId) {
    return $("#" + formId)
      .serializeArray()
      .reduce(function (object, item) {
        object[item.name] = item.value;
        return object;
      }, {});
  }

  function displayResult(result) {
    $("#apiOutput").text(JSON.stringify(result, null, 2));
    hljs.highlightBlock(document.getElementById("apiOutput"));
    $("#apiOutputModal").modal("show");
  }
});

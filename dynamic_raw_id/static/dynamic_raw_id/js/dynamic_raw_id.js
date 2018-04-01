// Overwrite Django's `dismissRelatedLookupPopup` to trigger a change event
// on the value change, so dynamic_raw_id can catch it and update the associated
// label.
function dismissRelatedLookupPopup(win, chosenId) {
  var name = windowname_to_id(win.name);
  var elem = document.getElementById(name);
  if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
    elem.value += ',' + chosenId;
  } else {
    elem.value = chosenId;
  }
  django.jQuery(elem).trigger('change');
  win.close();
}

(function($) {
  $(document).ready(function($) {

    function update_dynamic_raw_id_label(element, multi) {
      var name = element.next("a").attr("data-name"),
        app = element.next("a").attr("data-app"),
        model = element.next("a").attr("data-model"),
        value = element.val(),
        ADMIN_URL = window.DYNAMIC_RAW_ID_MOUNT_URL || "/admin/",
        MOUNT_URL = ADMIN_URL + "dynamic_raw_id",
        admin_url_parts = window.location.pathname.split("/").slice(1, 4);

      var url = MOUNT_URL;
      if (multi === true) {
        url = url + "/" + app + "/" + model + "/multiple/";
      } else {
        url = url + "/" + app + "/" + model + "/";
      }
      try {
        // only fire the ajax call if we have all the required info
        if ((name !== undefined) &&
          (url !== undefined) &&
          (value !== undefined) && (value !== "")) {
          // Handles elements added via the TabularInline add row functionality
          if (name.search(/__prefix__/) != -1) {
            name = element.attr("id").replace("id_", "");
          }

          $.ajax({
            url: url,
            data: {"id": value},
            success: function(data) {
              $("#" + name + "_dynamic_raw_id_label").html(" " + data);
            }
          });
        }
      } catch (e) {
        console.log("Oups, we have a problem" + e);
      }
    }

    $(".vForeignKeyRawIdAdminField").change(function(e) {
      var $this = $(this);
      update_dynamic_raw_id_label($this, multi = false);
      e.stopPropagation();
    });

    // Handle ManyToManyRawIdAdminFields.
    $(".vManyToManyRawIdAdminField").change(function(e) {
      var $this = $(this);
      update_dynamic_raw_id_label($this, multi = true);
      e.stopPropagation();
    });

    // Clear both the input field and the labels
    $(".dynamic_raw_id-clear-field").click(function(e) {
      var $this = $(this);
      $this.parent().find('.vForeignKeyRawIdAdminField, .vManyToManyRawIdAdminField').val("").trigger('change');
      //$this.parent().find(".dynamic_raw_id_label").empty();
      $this.parent().find(".dynamic_raw_id_label").html("&nbsp;");
    });

    // Open up the pop up window and set the focus in the input field
    $(".dynamic_raw_id-related-lookup").click(function(e) {
      // Actual Django javascript function
      showRelatedObjectLookupPopup(this);

      // Set the focus into the input field
      $(this).parent().find('input').focus();
      return false;
    });

    // Fire the event to update the solmonella fields on loads
    // $(".vManyToManyRawIdAdminField").trigger('change');
    // $(".vForeignKeyRawIdAdminField").trigger('change');

    // Update the dynamic_raw_id fields on loads
    $(".vManyToManyRawIdAdminField").each(function() {
      update_dynamic_raw_id_label($(this), multi = true);
    });
    $(".vForeignKeyRawIdAdminField").each(function() {
      update_dynamic_raw_id_label($(this), multi = false);
    });

  });
})(django.jQuery);

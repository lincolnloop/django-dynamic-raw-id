// Overwrite Django's `dismissRelatedLookupPopup` to trigger a change event
// on the value change, so Salmonella can catch it and update the associated label.
// if an image is to be inserted call the .
function dismissRelatedLookupPopup(win, chosenId, chosenObj) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);

    if (name === 'id_image_embed' && chosenObj){
      insertAssetIntoMDE(name, chosenObj);
    }
    else {
      if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
      } else {
        elem.value = chosenId;
      }
      django.jQuery(elem).trigger('change');
    }

    win.close();
}

(function($) {
    $(document).ready(function($) {

        function update_salmonella_label(element, multi){
            var name = element.next("a").attr("data-name"),
                app = element.next("a").attr("data-app"),
                model = element.next("a").attr("data-model"),
                value = element.val(),
                MOUNT_URL = window.SALMONELLA_MOUNT_URL || "/admin/salmonella",
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
                    if (name.search(/__prefix__/) != -1){
                        name = element.attr("id").replace("id_", "");
                    }

                    $.ajax({
                        url: url,
                        data: {"id": value},
                        success: function(data){
                            $("#" + name + "_salmonella_label").html(" " + data);
                        }
                    });
                }
            } catch (e) {
                console.log("Oups, we have a problem" + e);
            }
        }

        $(".vForeignKeyRawIdAdminField").change(function(e){
            var $this = $(this);
            update_salmonella_label($this, mutli=false);
            e.stopPropagation();
        });

        // Handle ManyToManyRawIdAdminFields.
        $(".vManyToManyRawIdAdminField").change(function(e){
            var $this = $(this);
            update_salmonella_label($this, multi=true);
            e.stopPropagation();
        });

        // Clear both the input field and the labels
        $(".salmonella-clear-field").click(function(e){
            var $this = $(this);
            $this.parent().find('.vForeignKeyRawIdAdminField, .vManyToManyRawIdAdminField').val("");
            $this.parent().find(".salmonella_label").empty();
        });

        // Open up the pop up window and set the focus in the input field
        $(".salmonella-related-lookup").click(function(e){
            // Actual Django javascript function
            showRelatedObjectLookupPopup(this);

            // Set the focus into the input field
            $(this).parent().find('input').focus();
            return false;
        });

        // Fire the event to update the solmonella fields on loads
        $(".vManyToManyRawIdAdminField").trigger('change');
        $(".vForeignKeyRawIdAdminField").trigger('change');
    });
})(django.jQuery);

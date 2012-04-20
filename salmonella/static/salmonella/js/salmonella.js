(function($) {
    $(document).ready(function($) {
        function update_salmonella_label(element, multi){
            var name = element.next("a").attr("data-name"),
                app = element.next("a").attr("data-app"),
                model = element.next("a").attr("data-model"),
                value = element.val(),
                MOUNT_URL = "/admin/salmonella",
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

        // A big of a workaround to fire the change event on
        // blur because 'showRelatedObjectLookupPopup'
        // doesn't set the value in a way that trigger 'change'
        $(".vForeignKeyRawIdAdminField, .vManyToManyRawIdAdminField").blur(function(e){
            $(this).trigger('change');
            e.stopPropagation();
        });

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
            $this.parent().find('input').val("");
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
        django.jQuery(".vManyToManyRawIdAdminField").trigger('change');
        django.jQuery(".vForeignKeyRawIdAdminField").trigger('change');
    });
})(django.jQuery);

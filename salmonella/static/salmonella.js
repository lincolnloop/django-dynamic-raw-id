function popup_wrapper(triggerLink, app_name, model_name){
    // Actual Django javascript function
    showRelatedObjectLookupPopup(triggerLink);
    
    // Set the focus into the input field
    django.jQuery("#"+triggerLink.id).parent().find('input').focus();
        
    return false;
}



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
                console.log("Oups, we have a problem" + e)
            }
        }

        // A big of a workaround.  The goal here was to use
        // 'change' but 'showRelatedObjectLookupPopup' above
        // doesn't set the value in a way that 'change'
        // is triggered so using blur instead.
        $(".vForeignKeyRawIdAdminField").blur(function(e){
            $this = $(this);
            update_salmonella_label($this, mutli=false);
        });

        // Handle ManyToManyRawIdAdminFields.
        $(".vManyToManyRawIdAdminField").blur(function(e){
            $this = $(this);
            update_salmonella_label($this, multi=true);
        });
        
        $(".clean_field").click(function(e){
            $this = $(this);
            $this.parent().find('input').val("")
            $this.parent().find(".salmonella_label").empty()
            
        });

        
        django.jQuery(".vManyToManyRawIdAdminField").trigger('blur');
        django.jQuery(".vForeignKeyRawIdAdminField").trigger('blur');
        
        
        


    });
})(django.jQuery);
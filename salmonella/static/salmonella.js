function popup_wrapper(triggerLink, app_name, model_name){
    var name = triggerLink.id.replace(/^lookup_/, '');
    name = id_to_windowname(name);

    // Actual Django javascript function
    showRelatedObjectLookupPopup(triggerLink);

    // Sets focus on input field so event is 
    // fired correctly.
    document.getElementById(name).focus();
    
    return false;
}

jQuery.noConflict();

jQuery(document).ready(function($) {
    function update_salmanella_label(element, url){
        var name = element.next("a").attr("data-name");
        var value = element.val();

        $.ajax(url, {
            data: {"id": value},
            success: function(data){
                $("#" + name + "_salmonella_label").html(" " + data);
            }
        });
    }
    
    // A big of a workaround.  The goal here was to use
    // 'change' but 'showRelatedObjectLookupPopup' above
    // doesn't set the value in a way that 'change'
    // is triggered so using blur instead.
    $(".vForeignKeyRawIdAdminField").blur(function(e){
        $this = $(this);
        var app = $this.next("a").attr("data-app");
        var model = $this.next("a").attr("data-model");
        var url = "/salmonella/" + app + "/" + model + "/";
        
        update_salmanella_label($this, url);
    });
    
    // Handle ManyToManyRawIdAdminFields.
    $(".vManyToManyRawIdAdminField").blur(function(e){
        $this = $(this);
        var app = $this.next("a").attr("data-app");
        var model = $this.next("a").attr("data-model");
        var url = "/salmonella/" + app + "/" + model + "/multiple/";
        
        update_salmanella_label($this, url);
    });
});

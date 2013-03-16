/*
Equal height columns with jQuery
by Dave Dash, http://spindrop.us/author/admin/

> $("#col1, #col2").equalizeCols();

will equalize the columns as expected

> $("#col1, #col2").equalizeCols("p,p");

will equalize the columns and add the extra space after the p tag in #col1 or
#col2 (whichever is shorter).
*/
jQuery.fn.equalizeCols = function(children) {
    var child = Array(0);
    if (children) {
        child = children.split(",");
    }
    var maxH = 0;
    this.each(
        function(i) {
            if (this.offsetHeight>maxH) maxH = this.offsetHeight;
        }
    ).css("height", "auto").each(
        function(i) {
            var gap = maxH-this.offsetHeight;
            if (gap > 0) {
                t = document.createElement('div');
                $(t).attr("class","fill").css("height",gap+"px");
                if (child.length > i) {
                    $(this).find(child[i]).children(':last-child').after(t);
                } else {
                    $(this).children(':last-child').after(t);
                }
            }
        }
    );
};

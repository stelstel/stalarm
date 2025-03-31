$(document).ready(function() {
    // Find the index of the column by its header name
    var columnIndex = $("#stockTable th").filter(function() {
        return $(this).text().trim() === "Dec. lim. reached";
    }).index(); // Get the index of the column
    
    // Loop through the table rows and check the specific column value
    $("#stockTable tbody tr").each(function() {
        var value = $(this).find("td").eq(columnIndex).text().trim(); // Use the found index
        if (value === "True") {
            $(this).addClass("table-warning-custom"); // Add Bootstrap class
        }
    });

    console.log("highlightAlarmRows.js is loaded!"); /////////////////////////////////////
    console.log("jQuery version:", $.fn.jquery);  // Check if jQuery is loaded ///////////////////////////
});



var refreshIntervalId;
$(document).ready(function()
{
    refreshMonitor();
    clearInterval(refreshIntervalId);
    refreshIntervalId = setInterval(function () { refreshMonitor(); }, 5000);	

   
});


$(document).on('click','.btnDeleteLectura', function(e){
    
    e.preventDefault();
    var si = confirm("Seguro que deseas eliminar esta lectura??");
    if(si)
    {
        $.ajax({
            type: 'POST',
            url: '/ajx-delete',
            data: { id: $(this).attr('rel'), "csrf_token": $(this).attr('wl-csrf') },
            success: function (json) {
                console.log(json);
            }
        }); 
    }
  
});


function refreshMonitor() {
    $.get('/data', {}, function (data) {
        $("#monitorData").html(data);
    });


}
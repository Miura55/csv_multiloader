$(document).on('change', ':file', function() {
    var input = $(this),
    numFiles = input.get(0).files ? input.get(0).files.length : 1,
    label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    var filelist = "";
    for (i = 0; i < input.get(0).files.length; i++) {
        if (i != 0){
            filelist += ", " + input.get(0).files[i].name;
        }else{
            filelist += input.get(0).files[0].name;
        }        
    }
    console.log(numFiles);
    input.parent().parent().next(':text').val(filelist);
});
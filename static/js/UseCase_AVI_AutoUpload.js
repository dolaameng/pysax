$(function(){
	console.log('>>> jQuery is ready');
	var FileUploadInput = $('#FileUploadInput');
	var FileUploadList = $('#FileUploadList');

	FileUploadInput.on('change', function(){
		// call form submit here
		console.log('>>> File is uploading...');
		
		// clear selected file list
		FileUploadList.empty();

		// append selected files into list
		var files = FileUploadInput[0].files;
		for (var i = 0; i < files.length; i++) {
			var fileName = files[i].name;
			var appendContent = '<option value="' + fileName + '">' + fileName +'</option>';
			FileUploadList.append(appendContent);
		}
	});
});

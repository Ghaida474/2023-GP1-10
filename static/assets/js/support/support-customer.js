$(function(e){
	'use strict';

	// Data Table
	$('#support-customerlist').DataTable({
		"order": [
			[ 0, "desc"]
		],
		order: [],
		columnDefs: [ 
			{ orderable: false, targets: '_all' } ,
			{ orderable: true, targets: [1] } 
		],
		language: {
			searchPlaceholder: 'Search...',
			sSearch: '',
			
		}
	});

	// Select2
	$('.select2').select2({
		minimumResultsForSearch: Infinity,
		width:'100%'
	});

 });

 
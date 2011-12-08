
function clear() {
	$('div.stickynote').remove();
}

function getBoard() {
	return $('input[name=board]:checked').val();
}

function getBoardCount(id, data) {
	var count = 0;
	for(var i in data.notes) {
		if(data.notes[i].board == id) {
			count++;
		}
	}
	return count;
}

function updateBoards(data) {
	var selected = getBoard();
	if(!selected) {
		selected = data.boards[0];
	}
	var boardsDiv = $('#boards');
	boardsDiv.empty();
	data.boards.sort();
	for(var i in data.boards) {
		var board = data.boards[i];
		var count = getBoardCount(board, data);
		var label = board;
		if(count) {
			label += ' (' + count + ')';
		}
		boardsDiv.append('<input type="radio" name="board" value="' + board + '"' + (board == selected ? ' checked' : '') +'>' + label + '</input>');
	}
	$('input[name=board]').change(showBoard);
}

function showBoard() {
	var board = getBoard();
	$('#content div.stickynote').each(function(index, element) {
		element = $(element);
		if(element.data('stickstick.board') == board) {
			element.show();
		} else {
			element.hide();
		}
	});
}

function show(data) {
	clear();
	for(var i in data.notes) {
		var stickynote = $('#content').stickynote.create({
			containment: 'content',
			x: data.notes[i].x,
			y: data.notes[i].y,
			size: data.notes[i].size == 2 ? 'large' : 'small',
			content: data.notes[i].content,
			ontop: true,
			ondelete: destroy,
			onstop: move
		})
		.data('stickstick.id', data.notes[i].id)
		.data('stickstick.board', data.notes[i].board).
		hide();
	}
	updateBoards(data);
	showBoard();
}

function create(note, text) {
	var pos = note.position();
	text = text.replace(/\n/g, '<br />'); // JSON is unhappy with newlines
	$.ajax({
		type: 'put',
		url: 'data/',
		dataType: 'json',
		contentType: 'application/json',
		data: JSON.stringify({
			board: getBoard(),
			x: pos.left,
			y: pos.top,
			size: note.hasClass('stickynote-large') ? 2 : 1,
			content: text
		}),
		success: show,
		error: fail
	});
}

function move(event, note) {
	var id = note.helper.data('stickstick.id');
	if(id) {
		var pos = note.position;
		$.ajax({
			type: 'post',
			url: 'data/note/' + id +'/',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({x: pos.left, y: pos.top}),
			success: refresh,
			error: fail
		});
	}
}

function destroy(note) {
	var id = $(note).parent().data('stickstick.id');
	if(id) {
		$.ajax({
			type: 'delete',
			url: 'data/note/' + id + '/',
			success: refresh,
			error: fail
		});
	}
}

function refresh() {
	$.ajax({
		url: 'data/',
		dataType: 'json',
		contentType: 'application/json',
		success: show,
		error: fail
	});
}

function forceRefresh() {
	$.ajax({
		cache: false,
		url: 'data/',
		dataType: 'json',
		contentType: 'application/json',
		success: show,
		error: fail
	});
}

function fail(request, status, error) {
	var dialog = $('<div title="Error"></div>').html(error || 'There was a communication error.');
	$(dialog).dialog({modal: true, resizable: false});
}

$(function() {
	if($.browser.msie) {
		// Caching breaks Internet Explorer
		$.ajaxSetup({
			cache: false
		});
	}

	// jQuery Loading plugin
	$('#content').loading({
		onAjax: true,
		align: {top: 2, left: 2},
		text: 'Please wait...'
	});
	
	$('#new-small').stickynote({
		containment: 'content',
		size: 'small',
		oncreate: create,
		onstop: move,
		x: 50
	});

	$('#new-large').stickynote({
		containment: 'content',
		size: 'large',
		oncreate: create,
		onstop: move,
		x: 50
	});

	$('#refresh').click(refresh);
	
	forceRefresh();
});

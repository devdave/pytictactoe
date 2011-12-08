/*

This source code, and its related CSS and images, were modified
by Tal Liron based on the work of Paul Bakaus.

Below is the original license (MIT).

---

Copyright (c) 2009 Paul Bakaus, http://jqueryui.com/

This software consists of voluntary contributions made by many
individuals (AUTHORS.txt, http://jqueryui.com/about) For exact
contribution history, see the revision history and logs, available
at http://jquery-ui.googlecode.com/svn/

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*/

(function($) {
	
	$.fn.stickynote = function(options) {
		var options = $.extend({}, $.fn.stickynote.defaults, options);
		return this.each(function() {
			$this = $(this);
			var these_options = $.meta ? $.extend({}, options, $this.data()) : options;
			switch(these_options.event) {
				case 'dblclick':
					$this.dblclick(function() { $.fn.stickynote.create(these_options); })
					break;
				case 'click':
					$this.click(function() { $.fn.stickynote.create(these_options); })
					break;
			}		
		});
	};
	
	$.fn.stickynote.defaults = {
		size 	: 'small',
		event	: 'click',
		color	: '#000000',
		x		: 0,
		y		: 0
	};
	
	$.fn.stickynote.create = function(options) {
		var div_wrap = $(document.createElement('div'))
			.addClass('stickynote')
			.addClass('stickynote-' + options.size)
			.css({'position': 'absolute', 'left': options.x, 'top': options.y});

		var div_note = $(document.createElement('div'))
			.addClass('stickynote-note')
			.css('cursor','move');
		div_wrap.append(div_note);
		
		if(!options.content) {
			var note_content = $(document.createElement('textarea'));
		
			div_note.append(note_content);

			var div_create = $(document.createElement('div'))
				.addClass('stickynote-create');
			div_wrap.append(div_create);

			div_create.click(function(e) {
				var wrapper = $(this).parent();
				var textarea = wrapper.find('textarea');
				var text = textarea.val();
				
				var p_note_text = $(document.createElement('p'))
					.css('color', options.color)
					.html(text);
				
				textarea
					.before(p_note_text)
					.remove();
				
				$(this).remove();
				
				if(options.oncreate) {
					options.oncreate(wrapper, text);
				}
			});
		}	
		else {
			div_note.append('<p style="color: ' + options.color + '">' + options.content + '</p>');
		}
		
		var div_delete = $(document.createElement('div'))
			.addClass('stickynote-delete');
		div_wrap.append(div_delete);
		
		if(!options.ondelete) {
			div_delete.click(function(e) {
				$(this).parent().remove();
			});
		}
		else {
			div_delete.click(function(e) {
				options.ondelete(this);
			});
		}
		
		function totop(event, ui) {
			$(ui).parent().append($(ui));
		}
		
		if(options.containment) {
			div_wrap.draggable({
				containment: '#' + options.containment,
				scroll: false,
				start: options.ontop ? totop : null,
				stop: options.onstop
			});	
			$('#' + options.containment).append(div_wrap);
		}
		else {
			div_wrap.draggable({
				scroll: false,
				start: options.ontop ? totop : null,
				stop: options.onstop
			});
			$('body').append(div_wrap);
		}
		
		return div_wrap;
	};
})(jQuery);
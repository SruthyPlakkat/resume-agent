(function () {
  var COL = 'chat-col';
  var BTN = 'chat-toggle-btn';

  function applyCollapse(col, btn, collapsed) {
    if (collapsed) {
      col.classList.add('chat-collapsed');
      btn.textContent = '▶';
    } else {
      col.classList.remove('chat-collapsed');
      btn.textContent = '◀';
    }
  }

  function init() {
    var col = document.getElementById(COL);
    var btn = document.getElementById(BTN);
    if (!col || !btn) { setTimeout(init, 400); return; }

    var saved = localStorage.getItem('chatCollapsed') === 'true';
    applyCollapse(col, btn, saved);

    btn.addEventListener('click', function () {
      var nowCollapsed = !col.classList.contains('chat-collapsed');
      applyCollapse(col, btn, nowCollapsed);
      localStorage.setItem('chatCollapsed', nowCollapsed);
    });

    var handle = document.createElement('div');
    handle.className = 'chat-resize-handle';
    handle.title = 'Drag to resize';
    col.insertBefore(handle, col.firstChild);

    var resizing = false, startX = 0, startW = 0;

    handle.addEventListener('mousedown', function (e) {
      if (col.classList.contains('chat-collapsed')) return;
      resizing = true;
      startX = e.clientX;
      startW = col.offsetWidth;
      handle.classList.add('dragging');
      document.body.style.cssText += ';cursor:ew-resize;user-select:none';
      e.preventDefault();
    });

    document.addEventListener('mousemove', function (e) {
      if (!resizing) return;
      var w = Math.max(260, Math.min(700, startW + (startX - e.clientX)));
      col.style.cssText += ';width:' + w + 'px;min-width:' + w + 'px;max-width:' + w + 'px;flex-basis:' + w + 'px';
    });

    document.addEventListener('mouseup', function () {
      if (!resizing) return;
      resizing = false;
      handle.classList.remove('dragging');
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    setTimeout(init, 500);
  }
})();

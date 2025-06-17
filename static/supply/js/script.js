// script.js
function confirmDelete(name, url) {
    document.getElementById('deleteName').textContent = name;
    document.getElementById('deleteUrl').href = url;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}

// 页面加载后执行
document.addEventListener('DOMContentLoaded', function() {
    // 为所有删除按钮添加点击事件处理（使用 data-* 属性）
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const name = this.getAttribute('data-name');
            const url = this.getAttribute('data-url');
            confirmDelete(name, url);
        });
    });
});
// 二级菜单的收缩
$('.multi-menu .title').click(function () {
    alert('test');
    $(this).next().css('display', 'none');
});

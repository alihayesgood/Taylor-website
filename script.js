document.addEventListener('DOMContentLoaded', () => {
    const albumCards = document.querySelectorAll('.album-card');

    albumCards.forEach(card => {
        card.addEventListener('click', () => {
            // 获取当前点击的专辑的 Era 标识
            const selectedEra = card.getAttribute('data-era');
            
            // 将标识写到 body 的 data-theme 属性上，从而触发 CSS 变量的瞬间切换
            document.body.setAttribute('data-theme', selectedEra);
            
            // 可以在这里添加一些音效或者额外的震动反馈
            console.log(`Switched to Taylor's Era: ${selectedEra}`);
        });
    });
});
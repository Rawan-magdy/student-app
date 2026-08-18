document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('darkModeToggle');
    const body = document.body;

    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark');
        if (toggleBtn) toggleBtn.textContent = '☀️';
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function () {
            body.classList.toggle('dark');

            if (body.classList.contains('dark')) {
                localStorage.setItem('theme', 'dark');   
                toggleBtn.textContent = '☀️';
            } else {
                localStorage.setItem('theme', 'light');
                toggleBtn.textContent = '🌙';
            }
        });
    }
});
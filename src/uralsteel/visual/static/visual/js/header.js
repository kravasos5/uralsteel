window.addEventListener("load", (event) => {
    let nav_profile_div = document.getElementsByClassName('nav-profile')[0];
    let dropdown = document.getElementsByClassName('header-dropdown')[0];
    let img = document.querySelector('div.nav-profile img');

    if (dropdown) {
        img.addEventListener('click', () => {
            dropdown.style.display = 'block';
        });

        nav_profile_div.addEventListener('mouseleave', () => {
            dropdown.style.display = 'none';
        });
    } else {
        img.addEventListener('click', () => {
            window.location.href = login_html;
        });
    };
});
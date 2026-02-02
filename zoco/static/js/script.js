function login_Toast() {
    const toast = document.getElementById('loginToast');
    if (!toast) return;
    toast.classList.add('active');
    setTimeout(() => {
        toast.classList.remove('active');
    }, 2000);
}

function loginToast() {
    login_Toast();
}

function showToast() {
    const toast = document.getElementById('successToast');
    if (!toast) return;
    toast.classList.add('active');
    setTimeout(() => {
        toast.classList.remove('active');
    }, 2000);
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('loginToast')) {
        loginToast();
    }
});




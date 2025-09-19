// Check if user is logged in
document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('isLoggedIn')) {
        window.location.href = '/';
    }
});

// Logout function
function logout() {
    localStorage.removeItem('isLoggedIn');
    window.location.href = '/';
}
// static/js/menu.js - Gestion du menu mobile et interactions

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation du menu hamburger mobile
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('nav');
    
    if (menuToggle && nav) {
        // Bascule du menu à la click sur le bouton hamburger
        menuToggle.addEventListener('click', function() {
            menuToggle.classList.toggle('active');
            nav.classList.toggle('active');
        });
        
        // Fermeture du menu au clic sur un lien
        const navLinks = nav.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                menuToggle.classList.remove('active');
                nav.classList.remove('active');
            });
        });
        
        // Fermeture du menu au clic en dehors
        document.addEventListener('click', function(event) {
            const isClickInsideNav = nav.contains(event.target);
            const isClickInsideToggle = menuToggle.contains(event.target);
            
            if (!isClickInsideNav && !isClickInsideToggle) {
                menuToggle.classList.remove('active');
                nav.classList.remove('active');
            }
        });
    }
    
    // Support du clavier pour la navigation (Escape ferme le menu)
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && menuToggle && nav) {
            menuToggle.classList.remove('active');
            nav.classList.remove('active');
        }
    });
    
    // Validation des formulaires côté client avec messages personnalisés
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const passwordFields = form.querySelectorAll('input[type="password"]');
            
            // Vérification basique : les mots de passe sensibles ne doivent pas être trop courts
            for (let field of passwordFields) {
                if (field.value && field.value.length < 8) {
                    e.preventDefault();
                    alert('Le mot de passe doit faire au minimum 8 caractères pour la sécurité.');
                    field.focus();
                    return false;
                }
            }
        });
    });
    
    // Affichage des messages Flash (notifications temporaires)
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Les alertes de succès disparaissent après 5 secondes
        if (alert.classList.contains('alert-success')) {
            setTimeout(() => {
                alert.style.transition = 'opacity 0.3s ease';
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }, 5000);
        }
    });
    
    // Détection de la navigation / marquage du lien actif
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            link.classList.add('active');
        }
    });
});

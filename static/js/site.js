document.addEventListener('DOMContentLoaded', () => {
    const profileToggle = document.getElementById('profileBtn');
    const profileDropdown = document.getElementById('profileDropdown');
    const mobileToggle = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileIcon = document.getElementById('mobileMenuIcon');

    if (profileToggle && profileDropdown) {
        profileToggle.addEventListener('click', () => {
            profileDropdown.classList.toggle('hidden');
        });
        document.addEventListener('click', (event) => {
            if (!profileToggle.contains(event.target) && !profileDropdown.contains(event.target)) {
                profileDropdown.classList.add('hidden');
            }
        });
    }

    if (mobileToggle && mobileMenu && mobileIcon) {
        mobileToggle.addEventListener('click', () => {
            const expanded = mobileToggle.getAttribute('aria-expanded') === 'true';
            mobileToggle.setAttribute('aria-expanded', String(!expanded));
            mobileMenu.classList.toggle('hidden');
            mobileIcon.classList.toggle('fa-bars');
            mobileIcon.classList.toggle('fa-xmark');
        });
    }

    document.querySelectorAll('#mobileMenu a').forEach((link) => {
        link.addEventListener('click', () => {
            if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('hidden');
                mobileToggle?.setAttribute('aria-expanded', 'false');
                mobileIcon?.classList.add('fa-bars');
                mobileIcon?.classList.remove('fa-xmark');
            }
        });
    });

    document.querySelectorAll('[data-toggle-upload-form]').forEach((button) => {
        button.addEventListener('click', () => {
            const formBlock = document.getElementById('uploadFormBlock');
            if (!formBlock) return;
            formBlock.classList.toggle('hidden');
            const addText = button.dataset.openText || 'Upload Resume';
            const label = button.querySelector('.toggle-label');
            if (label) {
                label.textContent = formBlock.classList.contains('hidden') ? addText : 'Close';
            }
        });
    });

    const coverLetterTextarea = document.querySelector('textarea[name="cover_letter"]');
    const charCount = document.getElementById('coverLetterCount');
    if (coverLetterTextarea && charCount) {
        const maxLength = 1000;
        const updateCount = () => {
            const remaining = maxLength - coverLetterTextarea.value.length;
            charCount.textContent = `${remaining} characters remaining`;
            charCount.classList.toggle('text-red-500', remaining < 0);
        };
        coverLetterTextarea.addEventListener('input', updateCount);
        updateCount();
    }

    const employerRadio = document.querySelector('input[name="user_type"][value="employer"]');
    const seekerRadio = document.querySelector('input[name="user_type"][value="job_seeker"]');
    const companyField = document.getElementById('company_field');

    if (companyField) {
        const updateCompanyField = () => {
            if (employerRadio?.checked) {
                companyField.classList.remove('hidden');
            } else {
                companyField.classList.add('hidden');
            }
        };
        employerRadio?.addEventListener('change', updateCompanyField);
        seekerRadio?.addEventListener('change', updateCompanyField);
        updateCompanyField();
    }

    const revealElements = document.querySelectorAll('.scroll-fade-in');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    revealElements.forEach((element) => revealObserver.observe(element));

    const colorSchemeMedia = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');
    const applyColorScheme = (dark) => {
        if (dark) {
            document.documentElement.classList.add('dark');
            document.body.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
            document.body.classList.remove('dark');
        }
    };
    if (colorSchemeMedia) {
        applyColorScheme(colorSchemeMedia.matches);
        colorSchemeMedia.addEventListener('change', (event) => applyColorScheme(event.matches));
    }
});

globalThis.toggleUploadForm = () => {
    const formBlock = document.getElementById('uploadFormBlock');
    if (!formBlock) return;
    formBlock.classList.toggle('hidden');
};


 function updateStatus(applicationId, status) {
        fetch(`/update-status/${applicationId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `status=${status}`
        }).then(response => {
            if (response.ok) {
                location.reload();
            }
        });
    }
    
    function openMessageModal(userId, userName) {
        let message = prompt(`Send a message to ${userName}:`);
        if (message) {
            alert(`Message sent to ${userName}!`);
        }
    }
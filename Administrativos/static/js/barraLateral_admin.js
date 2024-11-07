document.addEventListener("DOMContentLoaded", function () {
    var sidebar = document.getElementById('sidebar');

    sidebar.classList.add("closed");

    document.getElementById('menu-toggle').addEventListener('click', function () {
        sidebar.classList.toggle('closed');
    });

    document.getElementById('profile-btn').addEventListener('click', function () {
        var profileContent = document.getElementById('profile-content');
        var profileIcon = document.getElementById('profile-icon');

        if (profileContent.style.display === "block") {
            profileContent.style.display = "none";
            profileIcon.innerHTML = '<i class="fas fa-plus"></i>';
        } else {
            profileContent.style.display = "block";
            profileIcon.innerHTML = '<i class="fas fa-minus"></i>';
        }
    });

    document.getElementById('project-btn').addEventListener('click', function () {
        var projectContent = document.getElementById('project-content');
        var projectIcon = document.getElementById('project-icon');

        if (projectContent.style.display === "block") {
            projectContent.style.display = "none";
            projectIcon.innerHTML = '<i class="fas fa-plus"></i>';
        } else {
            projectContent.style.display = "block";
            projectIcon.innerHTML = '<i class="fas fa-minus"></i>';
        }
    });

    document.querySelectorAll('.sidebar a').forEach(function(link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();

            sidebar.classList.add('closed');

            setTimeout(() => {
                window.location.href = this.href;
            }, 300);
        });
    });

    document.addEventListener("click", function (event) {
        const profileBtn = document.getElementById("profile-btn");
        const projectBtn = document.getElementById("project-btn");
        const profileContent = document.getElementById("profile-content");
        const projectContent = document.getElementById("project-content");

        if (!profileBtn.contains(event.target) && !profileContent.contains(event.target)) {
            profileContent.style.display = "none";
            document.getElementById("profile-icon").innerHTML = '<i class="fas fa-plus"></i>';
        }

        if (!projectBtn.contains(event.target) && !projectContent.contains(event.target)) {
            projectContent.style.display = "none";
            document.getElementById("project-icon").innerHTML = '<i class="fas fa-plus"></i>';
        }

        if (!sidebar.contains(event.target) && !document.getElementById('menu-toggle').contains(event.target)) {
            sidebar.classList.add('closed');
        }
    });
});
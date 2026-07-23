/** @odoo-module **/

async function loadVersion() {
    const moduleName = 'api_mitienda_peru';
    const element = document.getElementById(`module-version.${moduleName}`);

    if (!element) return;
    if (element.dataset.loaded === "1") return;

    try {
        const res = await fetch(`/api/${moduleName}/version`, {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        });
        const data = await res.json();

        element.dataset.loaded = "1";

        let el = document.getElementById('module-version.version');
        el.textContent = data.version;

        el = document.getElementById('module-version.status');
        el.textContent = data.status;

        el = document.getElementById('module-version.release-div');
        if (data.status == 'Production/Stable') {
            el.style.display = 'none';
        } else {
            el.style.display = 'block';

            el = document.getElementById('module-version.release');
            el.textContent = data.release;
        }

    } catch (err) {
        console.error(err);
    }
}

function startObserver() {
    const observer = new MutationObserver(() => {
        loadVersion();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true,
    });

    loadVersion();
}

if (document.body) {
    startObserver();
} else {
    document.addEventListener('DOMContentLoaded', startObserver);
}
// CONTENT:
// 1. Settings Panels
// 2. Reading And Study Mode
// 3. Filter
// 4. Chapter & Verse Navigation
// 5. Expanded Version
// 6. Highlight Readings
// 7. Dark And Light Theme


/* ////////////////// */
/* 1. Settings Panels */
/* ////////////////// */

// Open Settings Panels Desktop 
const settingsIcon = document.getElementById('settingsIcon');
const panelLeft = document.getElementById('panel-left');
const panelRight = document.getElementById('panel-right');

let panelsOpen = false;

function closePanels() {

    panelLeft.classList.remove('panel-open');
    panelRight.classList.remove('panel-open');

    panelLeft.classList.add('panel-closing');
    panelRight.classList.add('panel-closing');

    settingsIcon.src = 'images/settings.svg';

    setTimeout(() => {

        panelLeft.style.display = 'none';
        panelRight.style.display = 'none';

        panelLeft.classList.remove('panel-closing');
        panelRight.classList.remove('panel-closing');

    }, 400);

    panelsOpen = false;
}

settingsIcon.addEventListener('click', () => {
    if (panelsOpen) {
		closePanels();
	} else {

		panelLeft.style.display = 'block';
		panelRight.style.display = 'block';

		panelLeft.classList.add('panel-open');
		panelRight.classList.add('panel-open');

		settingsIcon.src = 'images/close.svg';

		panelsOpen = true;
	}
});

document.addEventListener('click', (event) => {

    if (!panelsOpen) return;

    const clickedInsideLeft = panelLeft.contains(event.target);
    const clickedInsideRight = panelRight.contains(event.target);
    const clickedSettingsIcon = settingsIcon.contains(event.target);

    if (
        !clickedInsideLeft &&
        !clickedInsideRight &&
        !clickedSettingsIcon
    ) {
        closePanels();
    }

});

// Open Settings Panels Mobile 
const settingsIconMobil = document.getElementById('settingsIconMobil');
const panelMobil = document.getElementById('panel-mobil');

settingsIconMobil.addEventListener('click', () => {
    if (panelMobil.style.display === 'block') {
        // Hide panels
        panelMobil.style.display = 'none';
        // Change icon
        settingsIconMobil.src = 'images/settings.svg';
    } else {
        // Show panel
        panelMobil.style.display = 'block';
        // Change icon
        settingsIconMobil.src = 'images/close.svg';
    }
});


/* //////////////////////////////////////// */
/* 2. Switch Between Reading And Study Mode */
/* //////////////////////////////////////// */

const readingModeToggle = document.getElementById('reading-mode-toggle');
const studyingModeToggle = document.getElementById('studying-mode-toggle');

const readingModeToggleMobile = document.getElementById('reading-mode-toggle-mobile');
const studyingModeToggleMobile = document.getElementById('studying-mode-toggle-mobile');

const filterSwitches = document.querySelectorAll('.filter-sw');

// Activate Reading Mode
function activateReadingMode() {
    filterSwitches.forEach(switchInput => {

        switchInput.checked = false;
        // Trigger Switches
        switchInput.dispatchEvent(new Event('change'));
    });

    // Desktop Buttons
    readingModeToggle.classList.add('active-btn');
    readingModeToggle.classList.remove('inactive-btn');

    studyingModeToggle.classList.remove('active-btn');
    studyingModeToggle.classList.add('inactive-btn');

    // Mobile Buttons
    readingModeToggleMobile.classList.add('active-btn');
    readingModeToggleMobile.classList.remove('inactive-btn');

    studyingModeToggleMobile.classList.remove('active-btn');
    studyingModeToggleMobile.classList.add('inactive-btn');
}


// Activate Studying Mode
function activateStudyingMode() {
    filterSwitches.forEach(switchInput => {
        switchInput.checked = true;
        // Trigger Switches
        switchInput.dispatchEvent(new Event('change'));
    });
	
	// Close Details On Mobile
	const isMobile = window.matchMedia("(max-width: 768px)").matches;

	if (isMobile) {
		const detailElements = document.querySelectorAll('details');
		detailElements.forEach(detail => {
			detail.removeAttribute('open');
			});
	}

    // Update Desktop Buttons
    studyingModeToggle.classList.add('active-btn');
    studyingModeToggle.classList.remove('inactive-btn');

    readingModeToggle.classList.remove('active-btn');
    readingModeToggle.classList.add('inactive-btn');

    // Update Mobile Buttons
    studyingModeToggleMobile.classList.add('active-btn');
    studyingModeToggleMobile.classList.remove('inactive-btn');

    readingModeToggleMobile.classList.remove('active-btn');
    readingModeToggleMobile.classList.add('inactive-btn');
}

// Desktop Events
readingModeToggle.addEventListener('click', activateReadingMode);
studyingModeToggle.addEventListener('click', activateStudyingMode);

// Mobile Eevents
readingModeToggleMobile.addEventListener('click', activateReadingMode);
studyingModeToggleMobile.addEventListener('click', activateStudyingMode);


/* ///////// */
/* 3. Filter */
/* ///////// */

/* Toggle Script */
document.addEventListener("DOMContentLoaded", function() {
    var toggleNagari = document.getElementById("toggle-nagari");
    var toggleLatin = document.getElementById("toggle-latin");
	var toggleNagariMobile = document.getElementById("toggle-nagari-mobile");
    var toggleLatinMobile = document.getElementById("toggle-latin-mobile");
	
	//Desktop Toggle Nagari
    toggleNagari.addEventListener("change", function() {
        var elements = document.querySelectorAll(".vers-dev");
        elements.forEach(function(element) {
            element.style.display = toggleNagari.checked ? "block" : "none";
        });

        if (!toggleNagari.checked) {
            toggleLatin.disabled = true;
            toggleLatin.parentNode.style.opacity = "0.5";
        } else {
            toggleLatin.disabled = false;
            toggleLatin.parentNode.style.opacity = "1";
        }
    });
	//Desktop Toggle Latin
    toggleLatin.addEventListener("change", function() {
        var elements = document.querySelectorAll(".vers-latin");
        elements.forEach(function(element) {
            element.style.display = toggleLatin.checked ? "block" : "none";
        });

        if (!toggleLatin.checked) {
            toggleNagari.disabled = true;
            toggleNagari.parentNode.style.opacity = "0.5";
        } else {
            toggleNagari.disabled = false;
            toggleNagari.parentNode.style.opacity = "1";
        }
    });
	
	//Mobile Toggle Nagari
	toggleNagariMobile.addEventListener("change", function() {
        var elements = document.querySelectorAll(".vers-dev");
        elements.forEach(function(element) {
            element.style.display = toggleNagariMobile.checked ? "block" : "none";
        });

        if (!toggleNagariMobile.checked) {
            toggleLatinMobile.disabled = true;
            toggleLatinMobile.parentNode.style.opacity = "0.5";
        } else {
            toggleLatinMobile.disabled = false;
            toggleLatinMobile.parentNode.style.opacity = "1";
        }
    });
	//Mobile Toggle Latin
    toggleLatinMobile.addEventListener("change", function() {
        var elements = document.querySelectorAll(".vers-latin");
        elements.forEach(function(element) {
            element.style.display = toggleLatinMobile.checked ? "block" : "none";
        });

        if (!toggleLatinMobile.checked) {
            toggleNagariMobile.disabled = true;
            toggleNagariMobile.parentNode.style.opacity = "0.5";
        } else {
            toggleNagariMobile.disabled = false;
            toggleNagariMobile.parentNode.style.opacity = "1";
        }
    });
});


/* Toggle Filter */
document.addEventListener("DOMContentLoaded", function() {
    var toggleSwitches = document.querySelectorAll("#filter input[type='checkbox']");

    toggleSwitches.forEach(function(switchInput) {
        switchInput.addEventListener("change", function() {
            var target = switchInput.dataset.target;
            var elements = document.querySelectorAll("." + target);
            
            elements.forEach(function(element) {
                if (switchInput.checked) {
                    if (element.tagName.toLowerCase() === "details") {
                        element.setAttribute("open", "");
                        element.style.display = "block";
                    } else {
                        element.style.display = "block";
                    }
                } else {
                    if (element.tagName.toLowerCase() === "details") {
                        element.removeAttribute("open");
                    }
                    element.style.display = "none";
                }
            });
        });
    });
});


/* ///////////////////////////// */
/* 4. Chapter & Verse Navigation */
/* ///////////////////////////// */

// Chapter Smooth Scroll Function With Offset For Header
document.querySelectorAll('.scroll-link').forEach(anchor => {
	anchor.addEventListener('click', function (e) {
		e.preventDefault();

		// Remove 'active' From Other Chapter Links
		document.querySelectorAll('.scroll-link').forEach(link => {
			link.classList.remove('active');
		});

		// Add 'active' To Clicked Chapter Link
		this.classList.add('active');

		const target = document.querySelector(this.getAttribute('href'));
		const offset = 75; // Offset For Header

		window.scrollTo({
			top: target.offsetTop - offset,
			behavior: 'smooth'
		});
	});
});

// Verse Smooth Scroll Function With Offset For Header
document.querySelectorAll('.vers-link').forEach(anchor => {
	anchor.addEventListener('click', function (e) {
		e.preventDefault();

		// Remove 'active' From Other Verse Links
		document.querySelectorAll('.vers-link').forEach(link => {
			link.classList.remove('active');
		});

		// Add 'active' To Clicked Verse Link
		this.classList.add('active');

		const target = document.querySelector(this.getAttribute('href'));
		const offset = 75; // Offset For Header

		window.scrollTo({
			top: target.offsetTop - offset,
			behavior: 'smooth'
		});
	});
});


// Change Verse Navigation On Active Chapter
const chapterToggles = document.querySelectorAll('.chapter-toggle');
const verseTables = document.querySelectorAll('.verse-table-wrap');

chapterToggles.forEach(toggle => {

    toggle.addEventListener('click', (e) => {

        e.preventDefault();

        const chapter = toggle.dataset.chapter;

        // Active Chapter Button
        chapterToggles.forEach(btn => {
            btn.classList.remove('active-chapter');
        });

        toggle.classList.add('active-chapter');


        // Table Switching
        verseTables.forEach(wrapper => {

            const mainTable = wrapper.querySelector('.verse-table-main');
            const extraTable = wrapper.querySelector('.verse-table-extra');

            // Reset To Main View
            if (mainTable) {
                mainTable.classList.add('active-subtable');
            }

            if (extraTable) {
                extraTable.classList.remove('active-subtable');
            }

            // Activate Chapter
            if (wrapper.dataset.chapter === chapter) {
                wrapper.classList.add('active-table');
            } else {
                wrapper.classList.remove('active-table');
            }

        });

    });

});

//Show Next Verses
const showExtraButtons = document.querySelectorAll('.show-extra-btn');

showExtraButtons.forEach(button => {

    button.addEventListener('click', () => {

        const wrapper = button.closest('.verse-table-wrap');

        const mainTable = wrapper.querySelector('.verse-table-main');
        const extraTable = wrapper.querySelector('.verse-table-extra');

        mainTable.classList.remove('active-subtable');

        if (extraTable) {
            extraTable.classList.add('active-subtable');
        }

    });

});

//Back To Previous Verses
const showMainButtons = document.querySelectorAll('.show-main-btn');

showMainButtons.forEach(button => {

    button.addEventListener('click', () => {

        const wrapper = button.closest('.verse-table-wrap');

        const mainTable = wrapper.querySelector('.verse-table-main');
        const extraTable = wrapper.querySelector('.verse-table-extra');

        if (extraTable) {
            extraTable.classList.remove('active-subtable');
        }

        mainTable.classList.add('active-subtable');

    });

});


/* //////////////////////////// */
/* 5. Activate Expanded Version */
/*///////////////////////////// */

document.addEventListener("DOMContentLoaded", function() {

    const altrecSwitch = document.querySelector(
        '.expand-sw[data-target="altrec"]'
    );

    altrecSwitch.addEventListener("change", function() {

        const altRecElements = document.querySelectorAll('.altrec');
        const defRecElements = document.querySelectorAll('.defrec');

        const hp4 = document.getElementById('hp4');
        const hpx4 = document.getElementById('hpx4');


        if (altrecSwitch.checked) {

            // Show Alt Recension
            altRecElements.forEach(el => {
                el.style.display = 'block';
            });

            // Hide Default Recension
            defRecElements.forEach(el => {
                el.style.display = 'none';
            });

            // Switch Chapter Nav
            if (hp4) hp4.style.display = 'none';
            if (hpx4) hpx4.style.display = 'block';

        } else {

            // HIDE Alt Recension
            altRecElements.forEach(el => {
                el.style.display = 'none';
            });

            // SHOW Default Recension
            defRecElements.forEach(el => {
                el.style.display = 'block';
            });

            // Switch Chapter Nav Back
            if (hp4) hp4.style.display = 'block';
            if (hpx4) hpx4.style.display = 'none';

        }

    });

});


/* ///////////////////// */
/* 6. Highlight Readings */
/* ///////////////////// */

document.addEventListener('DOMContentLoaded', function() {
  var slider = document.querySelector('.highlight-sw');

  function updateColor() {
	var markElements = document.querySelectorAll('mark');
	var spanElements = document.querySelectorAll('span.lem');

	if (slider.checked) {
	  markElements.forEach(function(mark) {
		mark.classList.add('highlight');
		mark.classList.remove('default');
	  });
	  spanElements.forEach(function(span) {
		span.style.color = 'var(--mark-highlight)';
	  });
	} else {
	  markElements.forEach(function(mark) {
		mark.classList.remove('highlight');
		mark.classList.add('default');
	  });
	  spanElements.forEach(function(span) {
		span.style.color = 'var(--mark-default)';
	  });
	}
  }

  // Initialising
  updateColor();

  // Monitor Change To Slider
  slider.addEventListener('change', updateColor);
});


/* ////////////////////////////////////// */
/* 7. Switch Between Dark And Light Theme */
/* ////////////////////////////////////// */

function toggleDarkMode() {
    document.documentElement.classList.add("dark-mode");
    document.documentElement.classList.remove("light-mode");
    document.getElementById("dark-mode-toggle").classList.add("active-btn");
    document.getElementById("dark-mode-toggle").classList.remove("inactive-btn");
    document.getElementById("light-mode-toggle").classList.remove("active-btn");
    document.getElementById("light-mode-toggle").classList.add("inactive-btn");
	document.getElementById("dark-mode-toggle-mobile").classList.add("active-btn");
    document.getElementById("dark-mode-toggle-mobile").classList.remove("inactive-btn");
	document.getElementById("light-mode-toggle-mobile").classList.remove("active-btn");
    document.getElementById("light-mode-toggle-mobile").classList.add("inactive-btn");
}

function toggleLightMode() {
    document.documentElement.classList.add("light-mode");
    document.documentElement.classList.remove("dark-mode");
    document.getElementById("light-mode-toggle").classList.add("active-btn");
    document.getElementById("light-mode-toggle").classList.remove("inactive-btn");
    document.getElementById("dark-mode-toggle").classList.remove("active-btn");
    document.getElementById("dark-mode-toggle").classList.add("inactive-btn");
    document.getElementById("light-mode-toggle-mobile").classList.add("active-btn");
    document.getElementById("light-mode-toggle-mobile").classList.remove("inactive-btn");
	document.getElementById("dark-mode-toggle-mobile").classList.remove("active-btn");
    document.getElementById("dark-mode-toggle-mobile").classList.add("inactive-btn");
}
document.addEventListener('DOMContentLoaded', () => {
    const langFrBtn = document.getElementById('lang-fr');
    const langArBtn = document.getElementById('lang-ar');
    const searchForm = document.getElementById('search-form');
    const resultsSection = document.getElementById('results');
    const scheduleList = document.getElementById('schedule-list');

    // Autocomplete elements
    const originInput = document.getElementById('origin-input');
    const originHidden = document.getElementById('origin');
    const originSuggestions = document.getElementById('origin-suggestions');

    const destInput = document.getElementById('destination-input');
    const destHidden = document.getElementById('destination');
    const destSuggestions = document.getElementById('destination-suggestions');

    let currentLang = 'fr';
    let stations = [];

    const translations = {
        fr: {
            search_title: "Rechercher un train",
            origin: "Départ",
            destination: "Arrivée",
            departure_time: "Heure de départ",
            day_of_week: "Jour",
            search_btn: "Rechercher",
            results_title: "Résultats",
            lines_title: "Lignes SNTF",
            map_title: "Carte du Réseau",
            footer: "Tous droits réservés.",
            loading: "Chargement...",
            no_trains_found: "Aucun train trouvé",
            dep: "Dép",
            arr: "Arr",
            show_stops: "Voir les arrêts",
            hide_stops: "Masquer les arrêts",
            show_path: "Voir le parcours",
            hide_path: "Masquer le parcours",
            transfer_at: "Changement à",
            wait_time: "Attente",
            placeholder_origin: "Gare de départ...",
            placeholder_dest: "Gare d'arrivée..."
        },
        ar: {
            search_title: "بحث عن رحلة",
            origin: "الانطلاق",
            destination: "الوصول",
            departure_time: "وقت المغادرة",
            day_of_week: "اليوم",
            search_btn: "بحث",
            results_title: "النتائج",
            lines_title: "خطوط SNTF",
            map_title: "خريطة الشبكة",
            footer: "جميع الحقوق محفوظة.",
            loading: "جاري التحميل...",
            no_trains_found: "لا توجد رحلات",
            dep: "انطلاق",
            arr: "وصول",
            show_stops: "عرض المحطات",
            hide_stops: "إخفاء المحطات",
            show_path: "عرض المسار",
            hide_path: "إخفاء المسار",
            transfer_at: "تغيير في",
            wait_time: "انتظار",
            placeholder_origin: "محطة الانطلاق...",
            placeholder_dest: "محطة الوصول..."
        }
    };

    // Initialize Map
    const map = L.map('map').setView([36.75, 3.05], 10); // Algiers
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Fetch and Display Lines
    fetch('/api/lines/')
        .then(res => res.json())
        .then(data => {
            displayLines(data);
        })
        .catch(err => console.error('Error fetching lines:', err));

    // Fetch Stations
    fetch('/api/stations/')
        .then(res => res.json())
        .then(data => {
            stations = data;
            // No more populateSelects(), just ready for autocomplete
        })
        .catch(err => console.error('Error fetching stations:', err));

    // Custom Time Input Logic
    const timeHours = document.getElementById('time-hours');
    const timeMinutes = document.getElementById('time-minutes');
    const departureTimeHidden = document.getElementById('departure-time');

    // Set default time
    const now = new Date();
    const currentHours = String(now.getHours()).padStart(2, '0');
    const currentMinutes = String(now.getMinutes()).padStart(2, '0');

    timeHours.value = currentHours;
    timeMinutes.value = currentMinutes;
    updateHiddenTime();

    function updateHiddenTime() {
        let h = timeHours.value.padStart(2, '0');
        let m = timeMinutes.value.padStart(2, '0');
        // Simple validation
        if (parseInt(h) > 23) h = '23';
        if (parseInt(m) > 59) m = '59';
        departureTimeHidden.value = `${h}:${m}`;
    }

    function handleTimeInput(e, nextField) {
        const input = e.target;
        let value = input.value.replace(/[^0-9]/g, '');

        // Auto-advance
        if (value.length === 2) {
            if (nextField) nextField.focus();
        }

        // Validate max values
        const max = input.id === 'time-hours' ? 23 : 59;
        if (parseInt(value) > max) {
            value = String(max);
        }

        input.value = value;
        updateHiddenTime();
    }

    function handleTimeKeydown(e) {
        const input = e.target;
        const isHours = input.id === 'time-hours';

        if (e.key === 'ArrowUp') {
            e.preventDefault();
            let val = parseInt(input.value || '0');
            val = (val + 1) % (isHours ? 24 : 60);
            input.value = String(val).padStart(2, '0');
            updateHiddenTime();
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            let val = parseInt(input.value || '0');
            val = (val - 1 + (isHours ? 24 : 60)) % (isHours ? 24 : 60);
            input.value = String(val).padStart(2, '0');
            updateHiddenTime();
        } else if (e.key === 'ArrowRight' && isHours && input.selectionStart === input.value.length) {
            timeMinutes.focus();
        } else if (e.key === 'ArrowLeft' && !isHours && input.selectionStart === 0) {
            timeHours.focus();
        }
    }

    timeHours.addEventListener('input', (e) => handleTimeInput(e, timeMinutes));
    timeMinutes.addEventListener('input', (e) => handleTimeInput(e, null));

    timeHours.addEventListener('keydown', handleTimeKeydown);
    timeMinutes.addEventListener('keydown', handleTimeKeydown);

    // Focus select all
    timeHours.addEventListener('focus', () => timeHours.select());
    timeMinutes.addEventListener('focus', () => timeMinutes.select());

    // Set default day to today
    const dayOfWeekSelect = document.getElementById('day-of-week');
    const dayOfWeek = now.getDay(); // 0=Sunday, 1=Monday, ..., 6=Saturday
    dayOfWeekSelect.value = String(dayOfWeek);

    // Swap stations button
    const swapButton = document.getElementById('swap-stations');
    swapButton.addEventListener('click', () => {
        const originVal = originHidden.value;
        const originText = originInput.value;

        const destVal = destHidden.value;
        const destText = destInput.value;

        originHidden.value = destVal;
        originInput.value = destText;

        destHidden.value = originVal;
        destInput.value = originText;
    });

    // Autocomplete Setup
    function setupAutocomplete(input, hiddenInput, suggestionsDiv) {
        input.addEventListener('input', debounce((e) => {
            const query = e.target.value.toLowerCase();
            suggestionsDiv.innerHTML = '';

            if (query.length < 1) {
                suggestionsDiv.classList.add('hidden');
                return;
            }

            const filtered = stations.filter(s =>
                s.name_fr.toLowerCase().includes(query) ||
                s.name_ar.toLowerCase().includes(query)
            );

            if (filtered.length > 0) {
                filtered.forEach(station => {
                    const div = document.createElement('div');
                    div.className = 'suggestion-item';
                    const name = currentLang === 'fr' ? station.name_fr : station.name_ar;
                    div.textContent = name;
                    div.addEventListener('click', () => {
                        input.value = name;
                        hiddenInput.value = station.id;
                        suggestionsDiv.classList.add('hidden');
                        suggestionsDiv.innerHTML = '';
                    });
                    suggestionsDiv.appendChild(div);
                });
                suggestionsDiv.classList.remove('hidden');
            } else {
                suggestionsDiv.classList.add('hidden');
            }
        }, 300));

        // Hide suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!input.contains(e.target) && !suggestionsDiv.contains(e.target)) {
                suggestionsDiv.classList.add('hidden');
            }
        });
    }

    setupAutocomplete(originInput, originHidden, originSuggestions);
    setupAutocomplete(destInput, destHidden, destSuggestions);

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    function updateLanguage(lang) {
        currentLang = lang;
        document.documentElement.lang = lang;
        document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';

        // Update UI text
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (translations[lang][key]) {
                el.textContent = translations[lang][key];
            }
        });

        // Update placeholders
        originInput.placeholder = translations[lang].placeholder_origin;
        destInput.placeholder = translations[lang].placeholder_dest;

        // Update buttons
        if (lang === 'fr') {
            langFrBtn.classList.add('active');
            langArBtn.classList.remove('active');
        } else {
            langArBtn.classList.add('active');
            langFrBtn.classList.remove('active');
        }

        // Update input values if ID is selected (refresh name in new lang)
        if (originHidden.value) {
            const s = stations.find(st => st.id == originHidden.value);
            if (s) originInput.value = lang === 'fr' ? s.name_fr : s.name_ar;
        }
        if (destHidden.value) {
            const s = stations.find(st => st.id == destHidden.value);
            if (s) destInput.value = lang === 'fr' ? s.name_fr : s.name_ar;
        }
    }

    langFrBtn.addEventListener('click', () => updateLanguage('fr'));
    langArBtn.addEventListener('click', () => updateLanguage('ar'));

    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const fromId = originHidden.value;
        const toId = destHidden.value;
        const departureTime = departureTimeHidden.value;
        const dayOfWeek = document.getElementById('day-of-week').value;

        if (!fromId || !toId || !departureTime) {
            alert(currentLang === 'fr' ? "Veuillez remplir tous les champs" : "يرجى ملء جميع الحقول");
            return;
        }

        scheduleList.innerHTML = translations[currentLang].loading;
        resultsSection.classList.remove('hidden');

        // Save to recent searches (UX improvement)
        saveRecentSearch(fromId, toId);

        fetch(`/api/search/?from=${fromId}&to=${toId}&time=${departureTime}&day=${dayOfWeek}`)
            .then(res => res.json())
            .then(data => {
                displayResults(data);
            })
            .catch(err => {
                scheduleList.innerHTML = 'Error loading results.';
                console.error(err);
            });
    });

    function saveRecentSearch(fromId, toId) {
        // Simple implementation: just log for now, or could store in localStorage
        // localStorage.setItem('lastSearch', JSON.stringify({from: fromId, to: toId}));
    }

    function displayResults(trains) {
        const scheduleList = document.getElementById('schedule-list');
        scheduleList.innerHTML = '';

        if (trains.length === 0) {
            scheduleList.innerHTML = `<p>${translations[currentLang].no_trains_found}</p>`;
            return;
        }

        trains.forEach((train, index) => {
            const card = document.createElement('div');
            card.className = 'schedule-card'; // Note: CSS uses .train-card, let's fix this mismatch or update CSS
            // Actually CSS has .train-card. I should use .train-card.
            card.className = 'train-card';

            const isConnection = train.type === 'connection';
            const t = translations[currentLang];

            // Header with train number and times
            const trainDisplay = train.train_number.toLowerCase().startsWith('train') ?
                train.train_number : `Train ${train.train_number}`;

            // Badges
            let badgesHtml = '';
            if (train.badges && train.badges.length > 0) {
                badgesHtml = '<div class="badges">';
                train.badges.forEach(badge => {
                    let badgeClass = 'badge-default';
                    if (badge === 'Fastest') badgeClass = 'badge-fastest';
                    if (badge === 'Direct') badgeClass = 'badge-direct';
                    if (badge === 'Best Overall') badgeClass = 'badge-best';
                    badgesHtml += `<span class="badge ${badgeClass}">${badge}</span>`;
                });
                badgesHtml += '</div>';
            }

            const header = `
                <div class="train-header">
                    <div class="train-info-top">
                        <div class="train-number">${trainDisplay}</div>
                        ${badgesHtml}
                    </div>
                    <div class="train-times">
                        <div class="time-box">
                            <span class="time-label">${t.dep}</span>
                            <div class="time-value">${train.departure_time ? train.departure_time.substring(0, 5) : ''}</div>
                        </div>
                        <span class="arrow">→</span>
                        <div class="time-box">
                            <span class="time-label">${t.arr}</span>
                            <div class="time-value">${train.arrival_time ? train.arrival_time.substring(0, 5) : ''}</div>
                        </div>
                    </div>
                    ${train.duration ? `<div class="duration" style="font-size:0.9rem; color:#666;">${train.duration}</div>` : ''}
                </div>
            `;

            // Transfer info if connection
            let transferInfo = '';
            if (isConnection && train.transfer) {
                transferInfo = `
                    <div class="transfer-info">
                        <span class="transfer-icon">🔄</span>
                        <div>
                            <div>${t.transfer_at} <strong>${train.transfer.station}</strong></div>
                            <div class="transfer-time">${t.wait_time}: ${train.transfer.wait_time}</div>
                        </div>
                    </div>
                `;
            }

            // Stops toggle button
            const toggleText = isConnection ? t.show_path : t.show_stops;

            const stopsToggle = `
                <button class="stops-toggle" onclick="toggleStops(${index})">
                    ${toggleText}
                </button>
            `;

            // Stops list (hidden by default)
            let stopsList = '<div class="stops-list" id="stops-' + index + '" style="display:none;">';

            if (isConnection && train.legs) {
                train.legs.forEach((leg, legIndex) => {
                    const legTrainDisplay = leg.train.toLowerCase().startsWith('train') ?
                        leg.train : `Train ${leg.train}`;

                    stopsList += `<div class="leg-section">
                        <div class="leg-header">
                            ${legTrainDisplay}: ${leg.from} → ${leg.to}
                        </div>
                        <ul class="stops-ul" style="list-style:none; padding-left:10px;">`;

                    if (leg.stops) {
                        leg.stops.forEach(stop => {
                            stopsList += `<li>${stop.station} <span class="stop-time" style="float:right; color:#666;">${stop.time ? stop.time.substring(0, 5) : ''}</span></li>`;
                        });
                    }

                    stopsList += '</ul></div>';
                });
            } else {
                stopsList += '<ul class="stops-ul" style="list-style:none; padding-left:10px;">';
                if (train.stops) {
                    train.stops.forEach(stop => {
                        stopsList += `<li>${stop.station} <span class="stop-time" style="float:right; color:#666;">${stop.time ? stop.time.substring(0, 5) : ''}</span></li>`;
                    });
                }
                stopsList += '</ul>';
            }
            stopsList += '</div>';

            card.innerHTML = header + transferInfo + stopsToggle + stopsList;
            scheduleList.appendChild(card);
        });
    }

    // Make toggleStops global
    window.toggleStops = function (index) {
        const stopsList = document.getElementById('stops-' + index);
        const toggleButton = stopsList.previousElementSibling;
        const isConnection = toggleButton.textContent.includes(translations[currentLang].show_path) || toggleButton.textContent.includes(translations[currentLang].hide_path);

        if (stopsList.style.display === 'none') {
            stopsList.style.display = 'block';
            toggleButton.textContent = isConnection ? translations[currentLang].hide_path : translations[currentLang].hide_stops;
        } else {
            stopsList.style.display = 'none';
            toggleButton.textContent = isConnection ? translations[currentLang].show_path : translations[currentLang].show_stops;
        }
    };

    function displayLines(lines) {
        const linesGrid = document.getElementById('lines-grid');
        if (!linesGrid) return;

        linesGrid.innerHTML = '';
        linesGrid.className = 'lines-grid';

        lines.forEach(line => {
            const card = document.createElement('div');
            card.className = 'line-card';
            card.innerHTML = `
                <div class="line-code">${line.code}</div>
                <div class="line-name">${line.name}</div>
            `;
            linesGrid.appendChild(card);
        });
    }
});

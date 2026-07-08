/**
 * Product Card "+" Toggle — expands inline to show vehicle specs
 * Mimics official sagmoto.com inline detail toggle behavior
 */
(function() {
  'use strict';

  // ==================== Product Spec Data ====================
  var productData = {
    "x9 4x4 dump truck": {
      name: "X9 4×4 Самосвал",
      category: "Лёгкие грузовики",
      engine: "Yuchai YC4E",
      hp: 160,
      torque: "550 N·m",
      transmission: "6-speed Manual / 8-speed",
      drive: "4×4 Полный привод",
      gcw: "4.5T ~ 25T",
      wheelbase: "3300 / 3600 mm",
      cab: "Single-row flat-head / Day cab",
      suspension: "Leaf-spring, main + auxiliary",
      features: [
        "Полный привод, superior off-road capability",
        "Leaf-springs suspension, strong bearing capacity",
        "Extra-long service intervals for engine, gearbox and rear axle",
        "Low maintenance cost, simple structure"
      ]
    },
    "x9 tow truck": {
      name: "X9 Tow Truck",
      category: "Лёгкие грузовики",
      engine: "Yuchai YC4E",
      hp: 160,
      torque: "550 N·m",
      transmission: "6-speed Manual",
      drive: "4×2",
      gcw: "4.5T ~ 25T",
      wheelbase: "3360 / 3800 mm",
      cab: "Single-row flat-head",
      suspension: "Leaf-spring",
      features: [
        "Maximum gradient of over 30%",
        "Equipped with heavy-duty winch system",
        "Easy to cope with tough working conditions",
        "Compact design for urban recovery operations"
      ]
    },
    "x7 flatbed truck": {
      name: "X7 Бортовой грузовик",
      category: "Лёгкие грузовики",
      engine: "Yuchai YC4E",
      hp: 160,
      torque: "550 N·m",
      transmission: "6-speed Manual",
      drive: "4×2",
      gcw: "4.5T ~ 25T",
      wheelbase: "3360 / 3800 mm",
      cab: "Semi-floating cab",
      suspension: "Leaf-spring with dampers",
      features: [
        "Semi-floating cab + airbag shock-absorbing seat",
        "Pointer + LCD display instrumentation",
        "Fully wrapped airline seats, optimized sponge density",
        "Wide flatbed for versatile cargo applications"
      ]
    },
    "9-я серия sweeper": {
      name: "9-я серия Подметальная машина",
      category: "Спецтехника (Коммунальный)",
      engine: "Yuchai YC4D",
      hp: 140,
      torque: "480 N·m",
      transmission: "5-speed Manual",
      drive: "4×2",
      gcw: "4.5T ~ 25T",
      wheelbase: "3300 mm",
      cab: "Single-row flat-head",
      suspension: "Leaf-spring",
      features: [
        "Efficient street sweeping system",
        "High-capacity debris collection",
        "Powerful dust suppression capability",
        "Smart sanitation solution for modern cities"
      ]
    },
    "x6 dropside truck": {
      name: "X6 Бортовой грузовик",
      category: "Средние грузовики",
      engine: "Cummins ISD",
      hp: 210,
      torque: "800 N·m",
      transmission: "6-speed / 8-speed Manual",
      drive: "4×2",
      gcw: "12T ~ 60T",
      wheelbase: "3800 / 4200 mm",
      cab: "Day cab / Sleeper cab",
      suspension: "Multi-leaf spring",
      features: [
        "Minimum ground clearance 314mm, approach angle >25°",
        "New transmission system + maintenance-free drive axles",
        "Спецтехника low-rolling resistance tires for fuel efficiency",
        "Airbag shock-absorbing main seat, sleeper width 85cm"
      ]
    },
    "x6 awd cargo truck": {
      name: "X6 AWD Грузовики",
      category: "Средние грузовики",
      engine: "Cummins ISD",
      hp: 210,
      torque: "800 N·m",
      transmission: "6-speed Manual",
      drive: "4×4 Полный привод",
      gcw: "12T ~ 60T",
      wheelbase: "3800 / 4200 mm",
      cab: "Day cab",
      suspension: "Multi-leaf spring",
      features: [
        "4×4 Полный привод system",
        "Excellent off-road capability",
        "Robust chassis for various cargo",
        "High ground clearance for rough terrain"
      ]
    },
    "x6 sprinkler truck": {
      name: "X6 Поливомоечная машина",
      category: "Средние грузовики (Коммунальный)",
      engine: "Cummins ISD",
      hp: 210,
      torque: "800 N·m",
      transmission: "6-speed Manual",
      drive: "4×2",
      gcw: "12T ~ 60T",
      wheelbase: "3800 mm",
      cab: "Day cab",
      suspension: "Лёгкиеweight leaf-spring",
      features: [
        "Облегчённая конструкция chassis and frame",
        "M3000 cab with sedan-like interior",
        "Large water tank capacity",
        "Multiple spray modes for various applications"
      ]
    },
    "x6 cement mixers truck": {
      name: "X6 Автобетоносмеситель",
      category: "Средние грузовики (Спецтехника)",
      engine: "Cummins ISD",
      hp: 210,
      torque: "800 N·m",
      transmission: "6-speed Manual",
      drive: "6×4",
      gcw: "12T ~ 60T",
      wheelbase: "3800+1350 mm",
      cab: "Day cab",
      suspension: "Reinforced multi-leaf spring",
      features: [
        "High-strength mixing drum, extended service life",
        "Reliable hydraulic drive system",
        "Efficient concrete mixing and discharge",
        "Robust chassis for construction site operations"
      ]
    },
    "e1st tractor": {
      name: "E1st Тягач",
      category: "Тяжёлые грузовики",
      engine: "Cummins Z14EVIE 560",
      hp: 560,
      torque: "2650 N·m",
      transmission: "Eaton AMT 12-speed",
      drive: "6×4",
      gcw: "18T ~ 100T",
      wheelbase: "3300+1350 mm",
      cab: "Flat-floor high-roof sleeper",
      suspension: "4-point air suspension",
      features: [
        "Cummins + Eaton AMT + Hande axle — exclusive power chain",
        "Flat floor design, internal height 2.13m",
        "Optimized CFD aerodynamics, drag coefficient 0.45",
        "Fuel consumption 26.97L/100km (main+trailer matched)"
      ]
    },
    "z3 tractor truck": {
      name: "Z3 Тягач",
      category: "Тяжёлые грузовики",
      engine: "Cummins M13 520",
      hp: 520,
      torque: "2500 N·m",
      transmission: "12-speed Manual / AMT",
      drive: "6×4",
      gcw: "18T ~ 100T",
      wheelbase: "3200+1350 mm",
      cab: "Flat-floor high-roof sleeper",
      suspension: "4-point air suspension",
      features: [
        "Следующая-gen powertrain with intelligent electronic system",
        "Flat-floor design, stand and walk freely in cab",
        "High-strength cab meets latest European safety standards",
        "Efficient, fast, clean logistics experience"
      ]
    },
    "x3s trailer truck": {
      name: "X3s Тягач",
      category: "Тяжёлые грузовики",
      engine: "Cummins ISME 420 л.с.",
      hp: 420,
      torque: "2000 N·m",
      transmission: "10-speed Manual",
      drive: "6×4",
      gcw: "18T ~ 100T",
      wheelbase: "3200+1350 mm",
      cab: "High-roof sleeper cab",
      suspension: "4-point mechanical suspension",
      features: [
        "Versatile heavy-duty tractor",
        "Excellent power-to-weight ratio",
        "Ideal for regional and inter-city transport",
        "Кабина meets ECER29-03 collision standard"
      ]
    },
    "e3 tractor truck": {
      name: "E3 Тягач",
      category: "Тяжёлые грузовики",
      engine: "Yuchai YC6MK",
      hp: 400,
      torque: "1800 N·m",
      transmission: "9-speed / 12-speed Manual",
      drive: "6×4",
      gcw: "18T ~ 100T",
      wheelbase: "3200+1350 mm",
      cab: "High-roof sleeper cab",
      suspension: "4-point mechanical suspension",
      features: [
        "Dual warning system for driving safety",
        "Berth width 850mm, upper-lower spacing 800mm",
        "Efficient power chain, excellent chassis",
        "Cost-effective medium-haul transport solution"
      ]
    },
    "x9 aerial work platform truck": {
      name: "X9 Aerial Work Platform Truck",
      category: "Спецтехника",
      engine: "Yuchai YC4D",
      hp: 140,
      torque: "480 N·m",
      transmission: "5-speed Manual",
      drive: "4×2",
      gcw: "4.5T ~ 25T",
      wheelbase: "3360 mm",
      cab: "Day cab",
      suspension: "Leaf-spring",
      features: [
        "Multi-level telescopic arms, large operating range",
        "High-strength materials, high-precision manufacturing",
        "Multiple safety protection systems in cab",
        "Strong stability, flexible mobility"
      ]
    },
    "x9 tow truck": {
      name: "X9 Tow Truck",
      category: "Спецтехника",
      engine: "Yuchai YC4E",
      hp: 160,
      torque: "550 N·m",
      transmission: "6-speed Manual",
      drive: "4×2",
      gcw: "4.5T ~ 25T",
      wheelbase: "3800 mm",
      cab: "Day cab",
      suspension: "Leaf-spring",
      features: [
        "Тяжёлые-duty winch for vehicle recovery",
        "Maximum gradient of over 30%",
        "Professional roadside assistance platform",
        "Compact and maneuverable design"
      ]
    },
    "x7 concrete mixer truck": {
      name: "X7 Автобетоносмеситель",
      category: "Спецтехника",
      engine: "Yuchai YC4E",
      hp: 160,
      torque: "550 N·m",
      transmission: "6-speed Manual",
      drive: "4×2 / 6×4",
      gcw: "12T ~ 60T",
      wheelbase: "3800 / 4200 mm",
      cab: "Day cab",
      suspension: "Reinforced multi-leaf spring",
      features: [
        "High-strength wear-resistant steel drum",
        "Reliable hydraulic system",
        "Main mirror + blind mirror for reduced blind spots",
        "Reinforced double-layer chassis for tough conditions"
      ]
    },
    "x3s mixer trucks 8x4": {
      name: "X3s Mixer Trucks 8×4",
      category: "Спецтехника",
      engine: "Yuchai YC4D 140",
      hp: 140,
      torque: "480 N·m",
      transmission: "6-speed Manual",
      drive: "8×4",
      gcw: "25T ~ 100T",
      wheelbase: "1800+3000+1350 mm",
      cab: "Day cab",
      suspension: "Reinforced multi-leaf spring",
      features: [
        "8×4 drive for maximum load capacity",
        "Large mixing drum capacity",
        "High-strength frame for construction sites",
        "Reliable operation in demanding conditions"
      ]
    },
    "off-road dump truck": {
      name: "Внедорожный самосвал",
      category: "Внедорожные грузовики",
      engine: "Yuchai / Cummins",
      hp: 400,
      torque: "1900 N·m",
      transmission: "9-speed / 12-speed Manual",
      drive: "6×4 / 6×6",
      gcw: "25T ~ 100T",
      wheelbase: "3800+1350 mm",
      cab: "Day cab / Sleeper cab",
      suspension: "Reinforced mining suspension",
      features: [
        "850mm wide-chassis structure for poor road conditions",
        "Спецтехникаized mining rear suspension, load 25.3T→30.5T",
        "Directional adjustable exhaust tailpipe",
        "Stable performance on extreme terrain"
      ]
    },
    "9-я серия": {
      name: "9 Series Внедорожные",
      category: "Внедорожные грузовики",
      engine: "Yuchai / Cummins",
      hp: 400,
      torque: "1900 N·m",
      transmission: "9-speed / 12-speed Manual",
      drive: "6×4 / 6×6",
      gcw: "25T ~ 100T",
      wheelbase: "3800+1350 mm",
      cab: "Multiple cab options",
      suspension: "Тяжёлые-duty leaf spring",
      features: [
        "Durability, high performance, high load-bearing",
        "Multiple cab options available",
        "Adaptable to fuel tankers, sprinklers, dump trucks",
        "Designed for extreme off-road conditions"
      ]
    },
    "7 series": {
      name: "7-я серия Внедорожные",
      category: "Внедорожные грузовики",
      engine: "Yuchai",
      hp: 340,
      torque: "1600 N·m",
      transmission: "9-speed Manual",
      drive: "6×4 / 6×6",
      gcw: "25T ~ 100T",
      wheelbase: "3600+1350 mm",
      cab: "Day cab",
      suspension: "Double-layer frame, reinforced leaf spring",
      features: [
        "Powerful engine, excellent maneuverability",
        "Усиленная защитная решётка масляного поддона",
        "Двухслойная конструкция рамы",
        "Ideal for mining and heavy construction"
      ]
    },
    "6 series": {
      name: "6-я серия Внедорожные",
      category: "Внедорожные грузовики",
      engine: "Cummins ISD",
      hp: 285,
      torque: "1100 N·m",
      transmission: "6-speed / 8-speed Manual",
      drive: "4×2 / 6×4",
      gcw: "12T ~ 60T",
      wheelbase: "3800 mm",
      cab: "Day cab",
      suspension: "Reinforced leaf spring",
      features: [
        "Strong power and efficient transportation",
        "Reinforced design with iron bumper",
        "Customized upper-body configurations",
        "Balanced performance for construction & transport"
      ]
    },
    "i9": {
      name: "i9 Electric Truck",
      category: "Электромобили Vehicle",
      engine: "Electric Привод Motor",
      hp: 200,
      torque: "1200 N·m",
      transmission: "Single-speed reduction gear",
      drive: "4×2",
      range: "430 km (full charge)",
      wheelbase: "3360 mm",
      cab: "Day cab",
      charging: "120KW fast charge, 65min full",
      features: [
        "Integrated electric drive axle, higher efficiency",
        "430km working range, 120KW fast charging",
        "Brake energy recovery — ~15% energy saving",
        "Zero emission, low noise operation"
      ]
    },
    "i9 lite": {
      name: "i9 Lite Electric Truck",
      category: "Электромобили Vehicle",
      engine: "Electric Привод Motor",
      hp: 160,
      torque: "900 N·m",
      transmission: "Single-speed reduction gear",
      drive: "4×2",
      range: "300 km (full charge)",
      wheelbase: "3300 mm",
      cab: "Day cab",
      charging: "DC fast charge supported",
      features: [
        "Compact electric light truck",
        "Cost-effective urban logistics solution",
        "Zero emission, low operating cost",
        "Ideal for last-mile delivery"
      ]
    },
    "i5 Мусоровоз": {
      name: "i5 Compressor Car",
      category: "Электромобили Vehicle (Sanitation)",
      engine: "Electric Привод Motor",
      hp: 120,
      torque: "700 N·m",
      transmission: "Single-speed reduction gear",
      drive: "4×2",
      range: "250 km (full charge)",
      wheelbase: "2800 mm",
      cab: "Day cab",
      charging: "DC fast charge supported",
      features: [
        "Electric garbage compactor truck",
        "Zero emission sanitation solution",
        "Compact size for urban streets",
        "Low noise ideal for residential areas"
      ]
    }
  };

  // ==================== Toggle Handler ====================
  function toggleSpecs(btn) {
    var card = btn.closest('.product-grid-item');
    if (!card) return;

    var panel = card.querySelector('.product-specs-panel');
    if (!panel) {
      // First time: build and show panel
      panel = buildSpecPanel(card);
      card.appendChild(panel);
      btn.textContent = '\u2212'; // minus sign
      btn.classList.add('active');
      // Trigger animation
      requestAnimationFrame(function() {
        panel.classList.add('open');
      });
    } else if (panel.classList.contains('open')) {
      // Close
      panel.classList.remove('open');
      btn.textContent = '+';
      btn.classList.remove('active');
    } else {
      // Re-open
      panel.classList.add('open');
      btn.textContent = '\u2212';
      btn.classList.add('active');
    }
  }

  function getProductИмя(card) {
    var img = card.querySelector('img');
    if (img && img.alt) return img.alt.trim().toLowerCase();
    var h4 = card.querySelector('h4');
    if (h4) return h4.textContent.trim().toLowerCase();
    return '';
  }

  function findProductData(name) {
    // Exact match
    if (productData[name]) return productData[name];

    // Case-insensitive exact match
    var nameLower = name.toLowerCase();
    for (var key in productData) {
      if (key === nameLower) return productData[key];
    }

    // Starts-with match (e.g. "x9 tow truck" starts with "x9 tow truck")
    for (var k in productData) {
      if (nameLower.indexOf(k) === 0 && k.length > 3) return productData[k];
    }

    // Contains match
    for (var k2 in productData) {
      if (nameLower.indexOf(k2) !== -1 && k2.length > 3) return productData[k2];
    }

    return null;
  }

  function buildSpecPanel(card) {
    var name = getProductИмя(card);
    var data = findProductData(name);

    var panel = document.createElement('div');
    panel.classИмя = 'product-specs-panel';

    if (!data) {
      panel.innerHTML = '<div class="specs-loading">Характеристики недоступны</div>';
      return panel;
    }

    var html = '<div class="specs-inner">';
    html += '<table class="specs-table">';
    html += '<tr><td class="specs-label">Категория</td><td class="specs-value">' + data.category + '</td></tr>';
    html += '<tr><td class="specs-label">Двигатель</td><td class="specs-value">' + data.engine + '</td></tr>';
    html += '<tr><td class="specs-label">Мощность</td><td class="specs-value">' + data.hp + ' HP</td></tr>';
    html += '<tr><td class="specs-label">Крутящий момент</td><td class="specs-value">' + data.torque + '</td></tr>';
    html += '<tr><td class="specs-label">Трансмиссия</td><td class="specs-value">' + data.transmission + '</td></tr>';
    html += '<tr><td class="specs-label">Привод</td><td class="specs-value">' + data.drive + '</td></tr>';
    if (data.range) {
      html += '<tr><td class="specs-label">Запас хода</td><td class="specs-value highlight">' + data.range + '</td></tr>';
    } else {
      html += '<tr><td class="specs-label">ПММ</td><td class="specs-value">' + data.gcw + '</td></tr>';
    }
    html += '<tr><td class="specs-label">Колёсная база</td><td class="specs-value">' + data.wheelbase + '</td></tr>';
    html += '<tr><td class="specs-label">Кабина</td><td class="specs-value">' + data.cab + '</td></tr>';
    html += '<tr><td class="specs-label">Подвеска</td><td class="specs-value">' + data.suspension + '</td></tr>';
    if (data.charging) {
      html += '<tr><td class="specs-label">Зарядка</td><td class="specs-value highlight">' + data.charging + '</td></tr>';
    }
    html += '</table>';

    html += '<div class="specs-features">';
    html += '<h5>Ключевые особенности</h5>';
    html += '<ul>';
    for (var i = 0; i < data.features.length; i++) {
      html += '<li>' + data.features[i] + '</li>';
    }
    html += '</ul></div>';
    html += '</div>';

    panel.innerHTML = html;
    return panel;
  }

  // ==================== Init ====================
  function init() {
    var buttons = document.querySelectorAll('.pg-plus');
    for (var i = 0; i < buttons.length; i++) {
      (function(btn) {
        // Remove href navigation
        btn.removeAttribute('href');
        btn.style.cursor = 'pointer';
        btn.addEventListener('click', function(e) {
          e.preventDefault();
          e.stopPropagation();
          toggleSpecs(btn);
        });
      })(buttons[i]);
    }
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

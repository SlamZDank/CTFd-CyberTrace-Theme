// Challenge Window Size: Large

// Challenge Category Order Custom Function
function compareFn(a, b) {
  const priority = {
    "OSINT - IRL": 1,
    "OSINT": 2,
    "OSINT - SERIES": 3,
    "MISC": 4
  };
  const prioA = priority[a.trim()] ?? 999;
  const prioB = priority[b.trim()] ?? 999;

  if (prioA !== prioB) return prioA - prioB;

  return a.localeCompare(b);
}

// Challenge Order Custom Function
function compareFn(a, b) {
  var ax = [],
    bx = [];

  a.name.replace(/(\d+)|(\D+)/g, function (_, $1, $2) {
    ax.push([$1 || Infinity, $2 || ""]);
  });
  b.name.replace(/(\d+)|(\D+)/g, function (_, $1, $2) {
    bx.push([$1 || Infinity, $2 || ""]);
  });

  while (ax.length && bx.length) {
    var an = ax.shift();
    var bn = bx.shift();
    var nn = an[0] - bn[0] || an[1].localeCompare(bn[1]);
    if (nn) return nn;
  }

  return ax.length - bx.length;
}

// Use Built-IN Syntax Highlighter is set to ON

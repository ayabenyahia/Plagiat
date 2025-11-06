// Navigation entre les pages
function showPage(pageId) {
  document
    .querySelectorAll(".page")
    .forEach((p) => p.classList.remove("active"));
  document.getElementById(pageId).classList.add("active");
}

// Gestion de la blacklist
const blacklist = [];

function ajouterBlacklist() {
  const nom = document.getElementById("nomBlacklist").value.trim();
  if (!nom) return alert("Veuillez entrer un nom !");
  blacklist.push(nom);
  afficherBlacklist();
  document.getElementById("nomBlacklist").value = "";
}

function afficherBlacklist() {
  const list = document.getElementById("listeBlacklist");
  list.innerHTML = blacklist.map((n) => `<li>${n}</li>`).join("");
}

// ---- COMPARATEUR DE TEXTES ---- //
function levenshtein(a, b) {
  const matrix = Array.from({ length: a.length + 1 }, () =>
    Array(b.length + 1).fill(0)
  );
  for (let i = 0; i <= a.length; i++) matrix[i][0] = i;
  for (let j = 0; j <= b.length; j++) matrix[0][j] = j;

  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,
        matrix[i][j - 1] + 1,
        matrix[i - 1][j - 1] + cost
      );
    }
  }
  return matrix[a.length][b.length];
}

function calculerSimilarite(texte1, texte2) {
  const distance = levenshtein(texte1, texte2);
  const longueurMax = Math.max(texte1.length, texte2.length);
  return longueurMax === 0
    ? 100
    : ((1 - distance / longueurMax) * 100).toFixed(2);
}

function interpretation(taux) {
  taux = parseFloat(taux);
  if (taux < 15) return { msg: "Pas de plagiat", color: "green" };
  if (taux < 30) return { msg: "Ressemblance faible", color: "limegreen" };
  if (taux < 50) return { msg: "Plagiat partiel", color: "orange" };
  if (taux < 80) return { msg: "Forte similarité", color: "orangered" };
  return { msg: "Plagiat confirmé", color: "red" };
}

function genererDiff(t1, t2) {
  const mots1 = t1.split(/\s+/);
  const mots2 = t2.split(/\s+/);
  const max = Math.max(mots1.length, mots2.length);
  let diff1 = "",
    diff2 = "";
  for (let i = 0; i < max; i++) {
    if (mots1[i] === mots2[i]) {
      diff1 += `<span class="identique">${mots1[i] || ""}</span> `;
      diff2 += `<span class="identique">${mots2[i] || ""}</span> `;
    } else {
      diff1 += `<span class="different">${mots1[i] || ""}</span> `;
      diff2 += `<span class="different">${mots2[i] || ""}</span> `;
    }
  }
  return { diff1, diff2 };
}

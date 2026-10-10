// Trellis math engine - pure arithmetic, shared by the page and the tests.
// Every borrowed number is a labeled garden-build norm, not a rule.
(function (root) {
"use strict";

// Labeled norms (common garden-build references):
// - Slat grids read well at about 15 cm spacing; the real gap is the width divided between the slats.
// - Twine grids use the same 15 cm squares, with about 10% extra for knots and tie-offs.
// - Espalier wires run about 40 cm apart up the wall, anchored about every 60 cm, with about 5% extra for tensioning.

function r1(x) { return Math.round(x * 10) / 10; }
function positive() {
  for (var i = 0; i < arguments.length; i++) {
    var v = arguments[i];
    if (typeof v !== "number" || !isFinite(v) || v <= 0) return false;
  }
  return true;
}

function slatGrid(wCm, hCm, gapCm) {
  if (!positive(wCm, hCm)) return { error: "trellis dimensions must be positive" };
  if (!positive(gapCm)) return { error: "gap must be positive" };
  var vSlats = Math.floor(wCm / gapCm) + 1;
  var hSlats = Math.floor(hCm / gapCm) + 1;
  if (vSlats < 2 || hSlats < 2) return { error: "gap is wider than the trellis" };
  var realGapW = r1(wCm / (vSlats - 1));
  var realGapH = r1(hCm / (hSlats - 1));
  var lumberM = r1((vSlats * hCm + hSlats * wCm) / 100);
  return { wCm: r1(wCm), hCm: r1(hCm), vSlats: vSlats, hSlats: hSlats, realGapW: realGapW, realGapH: realGapH, lumberM: lumberM };
}

function renderSlat(r) {
  if (r.error) return r.error;
  return "A " + r.wCm + " x " + r.hCm + " cm trellis takes " + r.vSlats + " vertical and " + r.hSlats +
    " horizontal slats at a real " + r.realGapW + " x " + r.realGapH + " cm gap - about " + r.lumberM +
    " m of slat in total (labeled 15 cm grid).";
}

function twineGrid(wCm, hCm, gridCm) {
  if (!positive(wCm, hCm)) return { error: "trellis dimensions must be positive" };
  if (!positive(gridCm)) return { error: "grid size must be positive" };
  var vLines = Math.floor(wCm / gridCm) + 1;
  var hLines = Math.floor(hCm / gridCm) + 1;
  if (vLines < 2 || hLines < 2) return { error: "grid is wider than the trellis" };
  var twineM = r1((vLines * hCm + hLines * wCm) / 100 * 1.1);
  return { wCm: r1(wCm), hCm: r1(hCm), vLines: vLines, hLines: hLines, twineM: twineM };
}

function renderTwine(r) {
  if (r.error) return r.error;
  return "A " + r.wCm + " x " + r.hCm + " cm grid is " + r.vLines + " vertical and " + r.hLines +
    " horizontal lines - about " + r.twineM + " m of twine with the labeled 10% for knots and tie-offs.";
}

function espalierWire(wCm, hCm, rowGapCm, anchorGapCm) {
  if (!positive(wCm, hCm)) return { error: "wall dimensions must be positive" };
  if (!positive(rowGapCm, anchorGapCm)) return { error: "gaps must be positive" };
  var rows = Math.floor(hCm / rowGapCm);
  if (rows < 1) return { error: "wall is shorter than one labeled wire row" };
  var anchorsPerRow = Math.floor(wCm / anchorGapCm) + 1;
  var anchors = rows * anchorsPerRow;
  var wireM = r1(rows * wCm / 100 * 1.05);
  return { wCm: r1(wCm), hCm: r1(hCm), rows: rows, anchorsPerRow: anchorsPerRow, anchors: anchors, wireM: wireM };
}

function renderEspalier(r) {
  if (r.error) return r.error;
  return "A " + r.wCm + " x " + r.hCm + " cm wall takes " + r.rows + " wire rows at the labeled 40 cm spacing, " +
    r.anchorsPerRow + " anchors per row (" + r.anchors + " vine eyes in total) and about " + r.wireM +
    " m of wire with the labeled 5% for tensioning.";
}

var api = {
  slatGrid: slatGrid,
  twineGrid: twineGrid,
  espalierWire: espalierWire,
  renderSlat: renderSlat,
  renderTwine: renderTwine,
  renderEspalier: renderEspalier
};
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.TrellisMath = api;
})(typeof window !== "undefined" ? window : globalThis);

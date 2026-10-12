#!/usr/bin/env python3
"""Repair PDF math-font mojibake in the ML4T question pool text.

The exam-pool PDF embeds a math font with a broken ToUnicode map, so text extraction
produced garbage codepoints for math symbols. This module reverses the fixable cases
deterministically and FLAGS the rest (never guesses a subscript, which could corrupt a formula).

Fixable (high-confidence):
  - Mathematical Alphanumeric Symbols (italic X, y, p, β, λ, σ, …) -> plain letters, via Unicode NFKC.
  - fi/fl ligatures (U+FB01/FB02), private-use Symbol-font bullet (U+F0B7) -> "•".
  - Subscripts: the font mapped a contiguous Oriya codepoint run to subscripts. Confirmed by the
    pool's own "X₁ Earnings Yield / X₂ Debt-to-Equity / X₃ Volatility" example and the β₀ intercept:
      U+0B34→₀ U+0B35→₁ U+0B36→₂ U+0B37→₃ U+0B38→₄ U+0B39→₅
    Plus any codepoint named "… DIGIT N" (Oriya/Tamil/Malayalam digit glyphs) -> subscript N.
  - Hat/accent vowel-sign glyphs following a letter -> combining circumflex, composed to ŷ, ŵ, …

Not fixable automatically -> reported by garbled_chars() so the caller can flag the question:
  leftover Indic/Ethiopic/Tamil/… letter glyphs and unnamed codepoints (e.g. U+0BDD) whose intended
  subscript/symbol can't be known without the font or a clean re-render (poppler/OCR).
"""
import unicodedata, re

_SUBS = '₀₁₂₃₄₅₆₇₈₉'
_ORIYA_SUB = {0x0B34: '₀', 0x0B35: '₁', 0x0B36: '₂', 0x0B37: '₃', 0x0B38: '₄', 0x0B39: '₅'}
_HAT = {0x0DDC, 0x0BDC, 0x0BCB, 0x0BC5, 0x0B4B, 0x0DCF}  # vowel-sign glyphs used as a circumflex (ŷ, p̂)
_DIGITS = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE']
_GARBLE_SCRIPTS = ('ORIYA', 'TAMIL', 'MALAYALAM', 'SINHALA', 'ETHIOPIC', 'TELUGU',
                   'KANNADA', 'BENGALI', 'DEVANAGARI', 'GUJARATI', 'GURMUKHI')


_FOOTER = re.compile(r'\s*\b\d{1,3}\s+Rev:\d{12}\b')

def clean(s):
    """Return the text with deterministic PDF-extraction noise removed. Deliberately NARROW:
    only the italic math-letter block and fi/fl ligatures are normalized. Real superscripts,
    subscripts, fractions and symbols (², ³, ₁, ½, …, µ, ℝ) are preserved — a blanket NFKC once
    flattened "0.60²" into "0.602". Garbled math-font glyphs are fixed at the SOURCE (slices, from
    the PDF page images — see content/math_fixes.json); anything left is reported by garbled_chars()."""
    if not s:
        return s
    s = _FOOTER.sub('', s)                                  # pool page footers ("167 Rev:081020261230")
    s = s.replace('\uf0b7', '• ').replace('\uf0a7', '• ')  # Symbol-font bullets
    out = []
    for ch in s:
        o = ord(ch)
        if 0x1D400 <= o <= 0x1D7FF or 0xFB00 <= o <= 0xFB06:   # math italic X, β… → X, β; ﬁ → fi
            out.append(unicodedata.normalize('NFKC', ch))
        elif o in (0x200A, 0x2009, 0x202F):                    # hair/thin spaces → space
            out.append(' ')
        else:
            out.append(ch)
    return unicodedata.normalize('NFC', ''.join(out))


def garbled_chars(s):
    """Return the sorted distinct chars that are still mis-extracted glyph garbage after clean()."""
    bad = set()
    for ch in s:
        if ord(ch) <= 0x7f:
            continue
        try:
            n = unicodedata.name(ch)
        except ValueError:
            n = ''
        if n == '' or any(scr in n for scr in _GARBLE_SCRIPTS):
            bad.add(ch)
    return ''.join(sorted(bad, key=ord))


if __name__ == '__main__':
    import sys
    t = sys.stdin.read()
    sys.stdout.write(clean(t))

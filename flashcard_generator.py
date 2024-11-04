import csv


def genera_latex_flashcards(csv_file):
    # Header del documento LaTeX con formattazione leggibile
    latex_code = (
        r"\documentclass[a4paper,twoside]{article} "
        "\n"
        r"\usepackage[utf8]{inputenc} "
        "\n"
        r"\usepackage[italian]{babel} "
        "\n"
        r"\usepackage{tikz} "
        "\n"
        r"\usepackage{geometry} "
        "\n"
        r"\geometry{ "
        "\n"
        r"  a4paper, "
        "\n"
        r"  total={170mm,257mm}, "
        "\n"
        r"  left=10mm, "
        "\n"
        r"  right=10mm, "
        "\n"
        r"  top=10mm, "
        "\n"
        r"  bottom=10mm "
        "\n"
        r"} "
        "\n\n"
        r"\newcommand{\flashcard}[4]{ "
        "\n"
        r"  \begin{tikzpicture} "
        "\n"
        r"    \draw (0,0) rectangle (11,6); "  # Dimensioni aumentate a 11x6
        "\n"
        r"    \ifodd\value{page} "
        "\n"
        r"      \node[font=\large, text width=10cm, align=center] at (5.5,3) {\textbf{#2}\\[0.5cm] #3 \\ \footnotesize{Pagina: #4}}; "
        "\n"
        r"    \else "
        "\n"
        r"      \node[font=\large] at (5.5,3) {\textbf{#1}}; "
        "\n"
        r"    \fi "
        "\n"
        r"  \end{tikzpicture} "
        "\n"
        r"} "
        "\n\n"
        r"\begin{document} "
        "\n"
        r"\pagestyle{empty} "
        "\n\n"
    )

    # Lettura del file CSV
    flashcards = []
    with open(csv_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = {k: v.replace('"', "``") for k, v in row.items()}
            flashcards.append(row)

    # Creazione delle pagine con le flashcard
    for i in range(0, len(flashcards), 10):  # 10 flashcards per pagina
        # Inizio della pagina pari (fronte)
        latex_code += (
            r"  \begin{center} "
            "\n"
            r"    \vspace*{5cm} "  # Aggiungi padding verticale di 5 cm
            "\n"
            r"    \begin{tikzpicture}[remember picture, overlay, shift={(0,0)}] "
            "\n"
        )

        # Posizionamento delle flashcard in una griglia 2x5
        for j, card in enumerate(flashcards[i : i + 10]):
            # Calcolo delle coordinate per due colonne e cinque righe
            x = -5.5 if j % 2 == 0 else 5.5  # Due colonne
            y = 4 - (j // 2) * 6  # Cinque righe, altezza 6 per righe più alte
            latex_code += f"      \\node at ({x},{y}) {{\\flashcard{{{card['Sigla']}}}{{{card['Sigla_espansa']}}}{{{card['Spiegazione']}}}{{{card['Pagina']}}}}};\n"

        # Fine della pagina pari
        latex_code += (
            r"    \end{tikzpicture} " "\n" r"  \end{center} " "\n" r"  \newpage " "\n\n"
        )

        # Inizio della pagina dispari (retro)
        latex_code += (
            r"  \begin{center} "
            "\n"
            r"    \vspace*{5cm} "  # Aggiungi padding verticale di 5 cm
            "\n"
            r"    \begin{tikzpicture}[remember picture, overlay, shift={(0,0)}] "
            "\n"
        )

        # Posizionamento delle flashcard in una griglia 2x5 sul retro
        for j, card in enumerate(flashcards[i : i + 10]):
            x = -5.5 if j % 2 == 0 else 5.5
            y = 4 - (j // 2) * 6
            latex_code += f"      \\node at ({x},{y}) {{\\flashcard{{{card['Sigla']}}}{{{card['Sigla_espansa']}}}{{{card['Spiegazione']}}}{{{card['Pagina']}}}}};\n"

        # Fine della pagina dispari
        latex_code += (
            r"    \end{tikzpicture} " "\n" r"  \end{center} " "\n" r"  \newpage " "\n\n"
        )

    # Footer del documento LaTeX
    latex_code += r"\end{document}"

    return latex_code


# Genera il codice LaTeX a partire dal file CSV
latex_output = genera_latex_flashcards("./flashcards.csv")

# Salva in un file .tex
with open("flashcards.tex", "w", encoding="utf-8") as f:
    f.write(latex_output)

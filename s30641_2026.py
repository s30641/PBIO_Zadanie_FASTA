# Numer albumu: s30641
# Data: 2026-05-11
# Opis: Generator losowych sekwencji DNA z zapisem do formatu FASTA.

import random


def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    """Pobiera od użytkownika liczbę całkowitą z zakresu. W przypadku błędu powtarza pytanie."""
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")
        except ValueError:
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")


def generate_sequence(length: int) -> str:
    """Zwraca losową sekwencję DNA o zadanej długości."""
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choices(nucleotides, k=length))


def calculate_stats(sequence: str) -> dict:
    """Zwraca słownik ze statystykami sekwencji.
    Klucze: "A", "C", "G", "T" (wartości float, %), "GC" (wartość float, %)."""
    length = len(sequence)
    if length == 0:
        return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "GC": 0.0}

    a_count = sequence.count('A')
    c_count = sequence.count('C')
    g_count = sequence.count('G')
    t_count = sequence.count('T')

    return {
        "A": (a_count / length) * 100,
        "C": (c_count / length) * 100,
        "G": (g_count / length) * 100,
        "T": (t_count / length) * 100,
        "GC": ((c_count + g_count) / length) * 100
    }


def insert_name(sequence: str, name: str) -> str:
    """Wstawia imię w losową pozycję sekwencji. Imię zapisane małymi literami."""
    if not name:
        return sequence
    insert_pos = random.randint(0, len(sequence))
    return sequence[:insert_pos] + name.lower() + sequence[insert_pos:]


def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    """Zwraca sformatowany rekord FASTA jako string."""
    header = f">{seq_id}"
    if description:
        header += f" {description}"

    lines = [header]
    for i in range(0, len(sequence), line_width):
        lines.append(sequence[i:i + line_width])

    return "\n".join(lines)


# --- FUNKCJONALNOŚCI DODATKOWE ---

def transcribe_dna_to_rna(sequence: str) -> str:
    """Dodatek 1: Przeprowadza transkrypcję in silico (zamiana T na U)."""
    return sequence.replace('T', 'U')


def get_complementary_sequence(sequence: str) -> str:
    """Dodatek 2: Generuje nić komplementarną do zadanej sekwencji DNA."""
    mapping = str.maketrans("ACGT", "TGCA")
    return sequence.translate(mapping)


def find_motif_positions(sequence: str, motif: str) -> list:
    """Dodatek 3: Wyszukuje motyw i zwraca listę pozycji (indeksowanie od 1)."""
    positions = []
    index = sequence.find(motif)
    while index != -1:
        positions.append(index + 1)
        index = sequence.find(motif, index + 1)
    return positions


def save_sliding_window_gc(sequence: str, window_size: int, filename: str):
    """Dodatek 4: Oblicza GC-content w przesuwnym oknie i zapisuje wyniki do pliku CSV."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("pozycja_startu,gc_content\n")
        for i in range(len(sequence) - window_size + 1):
            window = sequence[i:i + window_size]
            gc_val = ((window.count('G') + window.count('C')) / window_size) * 100
            f.write(f"{i + 1},{gc_val:.2f}\n")


def main():
    """Główna funkcja programu integrująca wszystkie elementy."""
    # Pobieranie danych bazowych
    length = validate_positive_int("Podaj długość sekwencji: ")

    while True:
        seq_id = input("Podaj ID sekwencji: ")
        if any(c.isspace() for c in seq_id):
            print("Błąd: ID sekwencji nie może zawierać białych znaków.")
        elif not seq_id:
            print("Błąd: ID nie może być puste.")
        else:
            break

    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")

    # Pobieranie parametrów dla dodatków
    user_motif = input("Podaj motyw do wyszukania (np. ATG): ").upper()
    win_size = validate_positive_int("Podaj szerokość okna do analizy GC: ", max_val=length)

    # Proces generowania
    base_seq = generate_sequence(length)
    stats = calculate_stats(base_seq)
    final_dna = insert_name(base_seq, name)

    # 1. Zapis multi-FASTA (DNA, mRNA, Komplementarna)
    fasta_filename = f"{seq_id}.fasta"
    with open(fasta_filename, "w", encoding="utf-8") as f:
        # Oryginalna sekwencja z imieniem
        f.write(format_fasta(seq_id, description, final_dna) + "\n\n")
        # Sekwencja mRNA (na bazie czystego DNA)
        mrna = transcribe_dna_to_rna(base_seq)
        f.write(format_fasta(f"{seq_id}_mRNA", "Transkrypcja in silico", mrna) + "\n\n")
        # Sekwencja komplementarna
        compl = get_complementary_sequence(base_seq)
        f.write(format_fasta(f"{seq_id}_COMPL", "Nić komplementarna", compl))

    # 2. Statystyki w konsoli
    print(f"\nSekwencje zapisane do pliku: {fasta_filename}")
    print(f"Statystyki sekwencji (n={length}):")
    for nt, val in stats.items():
        if nt != "GC":
            print(f"  {nt}: {val:.2f}%")
    print(f"  GC-content: {stats['GC']:.2f}%")

    # 3. Wyniki wyszukiwania motywu
    if user_motif:
        hits = find_motif_positions(base_seq, user_motif)
        if hits:
            print(f"Motyw '{user_motif}' znaleziony na pozycjach: {hits}")
        else:
            print(f"Nie znaleziono motywu '{user_motif}'.")

    # 4. Analiza okna przesuwnego
    csv_name = f"{seq_id}_gc_analysis.csv"
    save_sliding_window_gc(base_seq, win_size, csv_name)
    print(f"Analiza okna GC została zapisana do pliku: {csv_name}")


if __name__ == "__main__":
    main()
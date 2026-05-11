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
    # random.choices losuje ze zwracaniem, k określa długość
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

    # Losowanie indeksu, w który wstawimy imię
    insert_pos = random.randint(0, len(sequence))
    return sequence[:insert_pos] + name.lower() + sequence[insert_pos:]


def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    """Zwraca sformatowany rekord FASTA jako string."""
    # Budowa nagłówka
    header = f">{seq_id}"
    if description:
        header += f" {description}"

    lines = [header]
    # Łamanie sekwencji na linie o stałej szerokości
    for i in range(0, len(sequence), line_width):
        lines.append(sequence[i:i + line_width])

    return "\n".join(lines)


def main():
    """Główna funkcja programu integrująca wszystkie elementy."""
    # 1. Pobieranie długości sekwencji z walidacją
    length = validate_positive_int("Podaj długość sekwencji: ")

    # 2. Pobieranie ID z walidacją braku białych znaków
    while True:
        seq_id = input("Podaj ID sekwencji: ")
        if " " in seq_id or "\t" in seq_id:
            print("Błąd: ID sekwencji nie może zawierać białych znaków.")
        elif not seq_id:
            print("Błąd: ID nie może być puste.")
        else:
            break

    # 3. Pobieranie opcjonalnych danych
    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")

    # 4. Generowanie czystej biologicznie sekwencji i obliczanie statystyk
    base_sequence = generate_sequence(length)
    stats = calculate_stats(base_sequence)

    # 5. Wstawienie imienia (robimy to po statystykach, żeby imię nie zaburzyło wyników)
    final_sequence = insert_name(base_sequence, name)

    # 6. Formatowanie do standardu FASTA
    fasta_content = format_fasta(seq_id, description, final_sequence)

    # 7. Zapis do pliku
    filename = f"{seq_id}.fasta"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(fasta_content)

    # 8. Wyświetlenie podsumowania na ekranie
    print(f"\nSekwencja zapisana do pliku: {filename}\n")
    print(f"Statystyki sekwencji (n={length}):")
    print(f"  A: {stats['A']:.2f}%")
    print(f"  C: {stats['C']:.2f}%")
    print(f"  G: {stats['G']:.2f}%")
    print(f"  T: {stats['T']:.2f}%")
    print(f"  GC-content: {stats['GC']:.2f}%")


if __name__ == "__main__":
    main()
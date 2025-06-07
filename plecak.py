import sys

def read_from_keyboard():
    while True:
        try:
            line = input("Podaj liczbę elementów (n) i pojemność plecaka (c): ")
            n, c = map(int, line.strip().split())
            if n <= 0 or c < 0:
                raise ValueError
            break
        except ValueError:
            print("Błędne dane. n musi być >0, c >=0, obie to liczby całkowite.")
    items = []

    print("Dodawanie przedmiotów: waga i wartość odzielone spacjami (np. '3 15')")
    for i in range(n):
        while True:
            try:
                line = input(f"Przedmiot {i+1}: ")
                w, v = map(int, line.strip().split())
                if w < 0 or v < 0:
                    raise ValueError
                items.append((w, v))
                break
            except ValueError:
                print("Błędne dane. Podaj dwie nieujemne liczby całkowite.")
    return n, c, items

def read_from_file():
    plik = input("Nazwa pliku: ")
    try:
        with open(plik) as f:
            header = f.readline().split()
            if len(header) != 2:
                raise ValueError("Pierwsza linia musi zawierać dokładnie 2 liczby.")
            n, c = map(int, header)
            if n <= 0 or c < 0:
                raise ValueError("n musi być >0, c ≥0.")
            items = []
            for idx, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                parts = line.split()
                if len(parts) != 2:
                    raise ValueError(f"Błąd w linii {idx+1}: oczekiwane 2 liczby.")
                w, v = map(int, parts)
                if w < 0 or v < 0:
                    raise ValueError(f"Błąd w linii {idx+1}: liczby nieujemne.")
                items.append((w, v))
            if len(items) != n:
                raise ValueError(f"Liczba wczytanych przedmiotów ({len(items)}) != n ({n}).")
            return n, c, items
    except Exception as e:
        print(f"Nie udało się wczytać pliku: {e}")
        sys.exit(1)

def naive_knapsack(n, c, items):
    lista_elementow = [
        [w, v, (v / w) if w > 0 else float('inf'), i]
        for i, (w, v) in enumerate(items)
    ]
    lista_elementow.sort(key=lambda x: x[2], reverse=True)

    lista_plecaka = []
    zajetosc_plecaka = 0
    i = 0
    while i < n and zajetosc_plecaka <= c:
        w, v, ratio, idx = lista_elementow[i]
        if zajetosc_plecaka + w <= c:
            lista_plecaka.append([w, v, ratio, idx])
            zajetosc_plecaka += w
        i += 1

    return lista_plecaka

def brute_force_knapsack(n, c, items):
    best_v = 0
    best_w = 0
    best_set = []
    for mask in range(2**n):
        w_sum = 0
        v_sum = 0
        subset = []
        for i in range(n):
            if mask & (2**i):
                w_sum += items[i][0]
                v_sum += items[i][1]
                if w_sum > c:
                    break
                subset.append(i)
        else:
            if v_sum > best_v:
                best_v = v_sum
                best_w = w_sum
                best_set = subset.copy()

    lista_plecaka = [
        [
            items[i][0],
            items[i][1],
            (items[i][1] / items[i][0]) if items[i][0] > 0 else float('inf'),
            i
        ]
        for i in best_set
    ]
    return lista_plecaka

def dynamic_knapsack(n, c, items):
    # xd
    return brute_force_knapsack(n, c, items)

def print_solution(name, lista_plecaka, c):

    print(f"\n=== {name} ===")
    if not lista_plecaka:
        print("Brak wybranych przedmiotów.")
        return

    wagi, wartosci, ratios, indeksy = zip(*lista_plecaka)
    total_w = sum(wagi)
    total_v = sum(wartosci)

    print(f"Pojemność plecaka (c): {c}")
    print(f"Sumaryczna masa:      {total_w}")
    print(f"Sumaryczna wartość:   {total_v}")
    print("Wybrane przedmioty (indeks od 1):", [i+1 for i in indeksy])

def main():
    mode = ''
    while mode not in ('k', 'f'):
        mode = input("Źródło danych — klawiatura (k) czy plik (f)? ").strip().lower()

    if mode == 'k':
        n, c, items = read_from_keyboard()
    else:
        n, c, items = read_from_file()

    sol_dp = dynamic_knapsack(n, c, items)
    print_solution("Programowanie dynamiczne", sol_dp, c)

    sol_g = naive_knapsack(n, c, items)
    print_solution("Algorytm zachłanny", sol_g, c)
    _, wartosci_dp, _, _ = zip(*sol_dp) if sol_dp else ((), (), (), ())
    v_dp = sum(wartosci_dp)
    _, wartosci_g, _, _ = zip(*sol_g) if sol_g else ((), (), (), ())
    v_g = sum(wartosci_g)
    print("Rozwiązanie zachłanne jest", "optymalne." if v_g == v_dp else "nieoptymalne.")

    sol_bf = brute_force_knapsack(n, c, items)
    print_solution("Przegląd zupełny (brute-force)", sol_bf, c)

if __name__ == "__main__":
    main()

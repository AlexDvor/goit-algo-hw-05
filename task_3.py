import timeit


"""
Завдання 3

Порівняйте ефективність алгоритмів пошуку підрядка: Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа на основі двох текстових файлів (стаття 1, стаття 2). 
Використовуючи timeit, треба виміряти час виконання кожного алгоритму для двох видів підрядків: одного, що дійсно існує в тексті, та іншого — вигаданого 
(вибір підрядків за вашим бажанням). На основі отриманих даних визначте найшвидший алгоритм для кожного тексту окремо та в цілому.

"""


def boyer_search(text, pattern):
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1

    bad_char = {pattern[i]: i for i in range(m)}

    s = 0
    while s <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            return s
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))

    return -1


def kmp_search(text, pattern):
    def compute_lps_array(pattern):
        length = 0
        lps = [0] * len(pattern)
        i = 1

        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    m = len(pattern)
    n = len(text)
    lps = compute_lps_array(pattern)
    i = j = 0

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return -1


def rabin_karp_search(text, pattern, prime=101):
    m = len(pattern)
    n = len(text)
    base = 256
    pattern_hash = 0
    text_hash = 0
    h = 1

    for i in range(m - 1):
        h = (h * base) % prime

    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        text_hash = (base * text_hash + ord(text[i])) % prime

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i : i + m] == pattern:
                return i

        if i < n - m:
            text_hash = (
                base * (text_hash - ord(text[i]) * h) + ord(text[i + m])
            ) % prime
            if text_hash < 0:
                text_hash += prime

    return -1


with open("article1.txt", "r", encoding="utf-8") as f:
    text1 = f.read()

with open("article2.txt", "r", encoding="utf-8") as f:
    text2 = f.read()


existing_substring = "Вікіпедія GPGPU"
non_existing_substring = "CPU"


def measure_time(search_function, text, pattern):
    return timeit.timeit(lambda: search_function(text, pattern), number=100)


bm_time1 = measure_time(boyer_search, text1, existing_substring)
kmp_time1 = measure_time(kmp_search, text1, existing_substring)
rk_time1 = measure_time(rabin_karp_search, text1, existing_substring)

bm_time2 = measure_time(boyer_search, text2, existing_substring)
kmp_time2 = measure_time(kmp_search, text2, existing_substring)
rk_time2 = measure_time(rabin_karp_search, text2, existing_substring)

print(f"Article 1 – Боєра-Мура: {bm_time1}, КМП: {kmp_time1}, Рабін-Карп: {rk_time1}")
print(f"Article 2 – Боєра-Мура: {bm_time2}, КМП: {kmp_time2}, Рабін-Карп: {rk_time2}")

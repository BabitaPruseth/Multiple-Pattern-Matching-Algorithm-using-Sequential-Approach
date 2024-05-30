from pattern_matching import PatternMatching as PM


matching = PM.PatternMatching()


def random_dna_gen(string_len, k):
    import random

    patterns = []
    string = "".join(random.choices("ACGT", weights=(0.3, 0.2, 0.2, 0.3), k=string_len))

    for num in k:
        patterns.append("".join(random.choices("ACGT", k=num)))

    with open("dataset.txt", "w") as file:
        file.write(string)
        for pattern in patterns:
            file.write("\n")
            file.write(pattern)


def proposed_match_test(func1, func2):
    try:
        func1_res = func1()
        func2_res = func2()
        assert func1_res == func2_res

    except AssertionError:
        print(f"Oops results of {func1.__name__} & {func2.__name__} are not same!")


# random_dna_gen(10000, [10, 20, 30, 40, 50])

with open("dataset.txt") as file:
    matching.text = file.readline().strip()
    for line in file:
        matching.pattern = line.strip()
        print(f"\nfor pattern {matching.pattern}:")
        print(f"Match Indices: {matching.proposed_match()}")
        print(f"Number of Occurrences: {matching.text.count(matching.pattern)}")
        # matching.performance()
        # proposed_match_test(matching.naive_match, matching.proposed_match)

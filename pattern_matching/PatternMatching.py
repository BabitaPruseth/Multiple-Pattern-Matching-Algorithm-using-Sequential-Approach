from collections import Counter, defaultdict


class PatternMatching:
    _preprocess_proposed_match_data = defaultdict(set)

    def __init__(self, text=None, pattern=None):
        self.text = None
        self.pattern = None

    def naive_match(self, text=None, pattern=None):
        if text is None:
            text = self.text

        if pattern is None:
            pattern = self.pattern

        n = len(text)
        k = len(pattern)
        indices = []

        for i in range(n - k + 1):
            curr_kmer = text[i : i + k]
            if pattern == curr_kmer:
                indices.append(i)

        return indices

    def better_match(self, text=None, pattern=None):
        if text is None:
            text = self.text

        if pattern is None:
            pattern = self.pattern

        k = len(pattern)

        preprocessed_data = self._preprocess_better_match(text, str(k))

        if pattern in preprocessed_data:
            return preprocessed_data[pattern]

        return []

    def _preprocess_better_match(self, text, k):
        import json
        import os

        cwd = os.getcwd()
        path = os.path.join(cwd, ".temp")
        try:
            os.mkdir(path)
        except OSError:
            pass

        os.chdir(path)

        try:
            with open("preprocessed_data.json") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        try:
            if data["text"] == text:
                return data["kmer"][k]

        except KeyError:
            data["text"] = text
            data["kmer"] = {}

        if k not in data["kmer"]:
            data["kmer"][k] = {}

            for i in range(len(text) - int(k) + 1):
                kmer = text[i : i + int(k)]
                if kmer in data["kmer"][k]:
                    data["kmer"][k][kmer].append(i)
                else:
                    data["kmer"][k][kmer] = [i]

        with open("preprocessed_data.json", "w") as file:
            json.dump(data, file, indent=2)

        return data["kmer"][k]

    @classmethod
    def _preprocess_proposed_match(cls, text, n):
        for i in range(n - 1):
            cls._preprocess_proposed_match_data[text[i : i + 2]].add(i)

        return cls._preprocess_proposed_match_data

    def proposed_match(self, text=None, pattern=None):

        if text is None:
            text = self.text

        if pattern is None:
            pattern = self.pattern

        n = len(text)
        k = len(pattern)
        indices = []
        idx_table_pat = defaultdict(list)
        count_table_pat = Counter()

        # creates index table for the text
        if not self._preprocess_proposed_match_data:
            idx_table_str = self._preprocess_proposed_match(text, n)

        else:
            idx_table_str = self._preprocess_proposed_match_data

        # creates index table for the pattern
        for i in range(0, k - 1, 2):
            idx_table_pat[pattern[i : i + 2]].append(i)
            count_table_pat.update([pattern[i : i + 2]])

        # creates sorted array of pairs in pattern
        sorted_pat_pair = sorted(idx_table_pat.keys(), key=count_table_pat.get)

        # Initial Check - Takes constant time
        for pair in sorted_pat_pair:
            if pair not in idx_table_str:
                return indices

        # creates sorted array of indexes of least occuring
        # pair in pattern present in text
        match_idx = sorted(idx_table_str[sorted_pat_pair[0]])

        # stores index of first least occuring pair in pattern
        align_idx = idx_table_pat[sorted_pat_pair[0]][0]

        for idx_str in match_idx:
            cont = True
            for pair in sorted_pat_pair:
                if cont is False:
                    break
                for idx_pat in idx_table_pat[pair]:
                    # stores relative position of current pair in pattern
                    curr_align = idx_pat - align_idx
                    try:
                        if idx_str + curr_align not in idx_table_str[pair]:
                            cont = False
                            break
                    except (KeyError, IndexError):
                        cont = False
                        break

            # To handle odd length pattern
            try:
                if cont is True and text[idx_str + (k - align_idx - 1)] == pattern[-1]:
                    indices.append(idx_str - align_idx)
            except (KeyError, IndexError):
                continue

        return indices

    def performance(self):
        import time

        funcs = [self.naive_match, self.proposed_match]

        for func in funcs:
            tic = time.perf_counter()
            func()
            toc = time.perf_counter()
            print(f"{func.__name__} took {(toc - tic):.4f}s to run.")

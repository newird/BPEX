#!/usr/bin/python3
from common import *
import os

class Cluster(object):

    def __init__(self, correct_dir, vector_dir, cluster_dir):
        self.vector_dir = vector_dir
        self.correct_dir = correct_dir
        self.cluster_dir = cluster_dir
        self.vector()
        self.cluster()

    def vector(self):
        if not os.path.exists(self.vector_dir):
            os.mkdir(self.vector_dir)

        for dir in os.listdir(self.correct_dir):
            problem_dir = os.path.join(self.correct_dir, dir)
            problem_vector_dir = os.path.join(self.vector_dir, dir)
            if os.path.isdir(problem_dir):
                ac_symb = os.path.join(problem_dir, 'ac_symb')

                if not os.path.exists(problem_vector_dir):
                    os.mkdir(problem_vector_dir)

                for symb in os.listdir(ac_symb):
                    symb_path = os.path.join(ac_symb, symb)
                    vector_path = os.path.join(problem_vector_dir, symb)
                    if os.path.exists(vector_path):
                        continue
                    try:
                        seq = self.load_params(symb_path)
                        with open(vector_path, 'w') as f:
                            f.write(str(seq))
                            f.close()
                    except:
                        pass

    def read_vector(self, path):
        f = open(path, 'r')
        res = f.readlines()
        if len(res) > 0:
            return eval(res[0])
        else:
            return 0

    def sim(self, v1, v2):
        return len(self.seq_align(v1, v2)) / min(len(v1), len(v2))

    def seq_align(self, vector1, vector2):
        alignments = []
        exclude = set(alignments)

        result = self.score_board(lambda n1, n2: self.score(n1, n2, exclude), vector1, vector2)

        for i, n1, j, n2, b in result:
            if b:
                alignments.append((n1, n2))

        return alignments

    def score_board(self, score, vector1, vector2):
        from itertools import count

        seq1 = [0] + vector1
        seq2 = [0] + vector2

        T = [[0 for __ in seq2] for _ in seq1]
        U = [[0 for __ in seq2] for _ in seq1]

        for i, n1 in zip(count(0), seq1):
            for j, n2 in zip(count(0), seq2):
                if i == 0:
                    T[i][j] = 0
                    U[i][j] = 0
                elif j == 0:
                    T[i][j] = 0
                    U[i][j] = 0
                else:
                    s = score(n1, n2)

                    T[i][j], U[i][j] = max(
                        (T[i - 1][j - 1] + s, 2),  # match
                        (T[i - 1][j], 3),  # delete
                        (T[i][j - 1], 4))  # insert

                    if U[i][j] == 2 and s > 0: U[i][j] = 1  # select

        align = list(self.iter_align(seq1, seq2, U))
        align.reverse()
        return align

    def score(self, n1, n2, exclude=None):
        if n1 == n2:
            if exclude and n1 == n2:
                return 0
            return 2
        else:
            return -1

    def iter_align(self, seq1, seq2, U):
        i = len(seq1) - 1
        j = len(seq2) - 1

        while i > 0 and j > 0:
            if U[i][j] == 1:
                yield (i, seq1[i], j, seq2[j], True)
                i -= 1
                j -= 1
            elif U[i][j] == 2:
                yield (i, seq1[i], j, seq2[j], False)
                i -= 1
                j -= 1
            elif U[i][j] == 3:
                yield (i, seq1[i], 0, None, False)
                i -= 1
            elif U[i][j] == 4:
                yield (0, None, j, seq2[j], False)
                j -= 1

        while j > 0:
            yield (0, None, j, seq2[j], False)
            j -= 1

        while i > 0:
            yield (i, seq1[i], 0, None, False)
            i -= 1

    def cluster(self):
        if not os.path.exists(self.cluster_dir):
            os.mkdir(self.cluster_dir)

        for dir in os.listdir(self.vector_dir):
            problem_vector_dir = os.path.join(self.vector_dir, dir)
            problem_cluster_dir = os.path.join(self.cluster_dir, dir)
            if os.path.isdir(problem_vector_dir):
                if not os.path.exists(problem_cluster_dir):
                    os.mkdir(problem_cluster_dir)
                for vector in os.listdir(problem_vector_dir):
                    v1 = self.read_vector(os.path.join(problem_vector_dir, vector))
                    for cluster in os.listdir(problem_cluster_dir):
                        v2 = self.read_vector(os.path.join(problem_cluster_dir, cluster))
                        if self.sim(v1, v2) > 0.9:
                            if len(v2) > len(v1):
                                os.rename(os.path.join(problem_cluster_dir, cluster), os.path.join(problem_cluster_dir, vector))
                                with open(os.path.join(problem_cluster_dir, vector), 'w') as f:
                                    f.write(str(v1))
                                    f.close()
                            break
                    else:
                        with open(os.path.join(problem_cluster_dir, vector), 'w') as f:
                            f.write(str(v1))
                            f.close()


    def load_params(self, symbfile):
        from itertools import count
        import pickle
        f = open(symbfile, 'rb')
        exec = pickle.load(f)
        f.close()
        seq = []

        for I, s in zip(exec, count(1)):
            if isinstance(I, STIns) and I.vid != 0 and I.loc > 0:
                seq.append(I.value)
        return seq
# Bpex

## Environment

Bpex is tested on the following operating systems:

- Ubuntu 16.04

Bpex is tested on the following Python versions:

- python 3.7

## Dependencies

Running example and benchmark:

- numpy
- Levenshtein (NEW)

Development or run other programs:

- clang-3.7

## Usage

the path of dataset is ./data/problem, and the structure is like this
make sure you have wrong_answer, corrent_answer and input.txt

```
correntanswer
 1024163167.c
 1024214049.c
 1024214679.c
cluster
 1024163167
 1024214049
 1024214679
wronganswer
 1024163167.c
 1024214049.c
 1024214679.c
 1024627607.c
 1024803348.c
 1025857746.c
 1025864249.c
input.txt
```

The content in cluter file is like this
the first line is wrong file and the others are correct file

```
wronganswer/1024163167.c
correctanswer/1056808672.c
correctanswer/1086907501.c
correctanswer/1056945287.c
correctanswer/1056808591.c
correctanswer/1056864099.c
correctanswer/1057156957.c
correctanswer/1057281149.c
correctanswer/1057281167.c
correctanswer/1057503529.c
correctanswer/1057943461.c
```

then run `sh run_bpex.sh`, all done
The result will be present in data/problem/bpex_result/submit_id/tmp/align.txt
the first line in accurracy
and the others are the result of source code alignment

```
0.59062873745823
while(t--) <-> while(n--)
while(t--) <-> while(n--)
for(i=0;i<n;i++) <-> int N,K,temp,count=0,count1=0,count2=0,count3=0,q,c;
for(i=0;i<n;i++) <-> for(int i=0;i<N;i++)
for(i=0;i<n;i++) <-> for(int i=0;i<N;i++)
for(i=0;i<n;i++) <-> for(int i=0;i<N;i++)
for(i=0;i<n;i++) <-> for(int i=0;i<N;i++)
for(i=0;i<n;i++) <-> for(int i=0;i<N;i++)
```

统计信息：
执行python cal.py ./data/<problemname>/bpex_result/自动统计所有信息

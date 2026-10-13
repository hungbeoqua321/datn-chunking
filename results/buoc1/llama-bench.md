| model                          |       size |     params | backend    | threads |  fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | ------: | --: | --------------: | -------------------: |
| qwen3 4B Q4_0                  |   2.21 GiB |     4.02 B | CPU        |       3 |   1 |          pp2048 |         25.11 ± 0.25 |
| qwen3 4B Q4_0                  |   2.21 GiB |     4.02 B | CPU        |       3 |   1 |           tg128 |          8.99 ± 0.05 |
| qwen3 4B Q4_K - Medium         |   2.32 GiB |     4.02 B | CPU        |       3 |   1 |          pp2048 |         18.69 ± 0.01 |
| qwen3 4B Q4_K - Medium         |   2.32 GiB |     4.02 B | CPU        |       3 |   1 |           tg128 |          7.69 ± 0.11 |

build: cbe28bb (1)

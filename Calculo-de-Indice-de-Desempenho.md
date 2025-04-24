# Cálculo de Índice de Desempenho para Mesas de Commander - Conquest

## Introdução
Este documento detalha o cálculo do **Índice de Desempenho (ID)** para seis mesas, cada uma representando um cenário único :
1. Vitória isolada com todos os oponentes zerados em pontos de vida simultaneamente.
2. Vitória isolada com todos os oponentes zerados, cada um eliminado por jogadores diferentes, com o vencedor matando o último.
3. Vitória isolada via combo infinito, sem eliminações parciais.
4. Vitória isolada via combo infinito, com uma eliminação direta realizada por outro jogador.
5. Empate com todos os jogadores terminando com a mesma quantidade de pontos de vida.
6. Empate com jogadores terminando com diferentes quantidades de pontos de vida.

Os cálculos utilizam a fórmula do ID, com siglas e significados explicitados, apresentados em tabelas para cada mesa. O ranking geral dos 24 jogadores é fornecido ao final.

## Sistema de Pontuação
O **Índice de Desempenho (ID)** é calculado como uma porcentagem (0% a 100%) por partida, com base em cinco métricas:
- **Resultado da Partida (RP)** – Resultado final (vitória, empate, colocação): 40%.
- **Turno de Vitória ou Empate (TV)** – Turno em que a partida termina: 20%.
- **Eliminações Realizadas (ER)** – Oponentes eliminados diretamente ou via combo: 20%.
- **Pontos de Vida Restantes (PV)** – Vida no fim ou na eliminação: 10%.
- **Ações Estratégicas (AE)** – Engajamento (mana, feitiços, dano): 10%.

**Fórmula do ID**:
```
ID = (0,4 × RP) + (0,2 × TV) + (0,2 × ER) + (0,1 × PV) + (0,1 × AE)
```

**Definição das Variáveis**:
| Variável | Sigla | Nome em Português | Peso | Fórmula |
|----------|-------|-------------------|------|---------|
| Resultado da Partida | RP | Resultado final (vitória, empate, colocação) | 40% | Vitória isolada: 100 pontos<br>Empate em 1º: 50 pontos<br>2º: 30 pontos<br>3º: 20 pontos<br>4º: 10 pontos |
| Turno de Vitória ou Empate | TV | Turno em que a partida terminou | 20% | (20 - Turno) / 20 * 100<br>Ex.: Turno 8 → (20-8)/20 * 100 = 60 pontos<br>Máximo 20 turnos |
| Eliminações Realizadas | ER | Oponentes eliminados diretamente ou via combo | 20% | (Eliminações / 3) * 100<br>Ex.: 1 eliminação → (1/3) * 100 = 33,33 pontos<br>Para combos: inclui oponentes ativos no momento da vitória |
| Pontos de Vida Restantes | PV | Percentual de vida no fim ou na eliminação | 10% | (Vida atual / 40) * 100<br>Ex.: 20 PV → (20/40) * 100 = 50 pontos |
| Ações Estratégicas | AE | Mana gasto, feitiços conjurados, dano causado | 10% | Normalizado com base na média da mesa<br>Ex.: Dano médio → 50 pontos |

**Nota sobre ER**: Em vitórias por combo infinito, o vencedor recebe crédito por eliminar todos os oponentes ativos no momento da vitória, além de eliminações diretas anteriores, até o limite de 3 eliminações (ER = 100).

## Mesa 1: Vitória Isolada (Oponentes com 0 PV Simultaneamente)
**Contexto**: P1 vence no turno 8, eliminando P2, P3 e P4 simultaneamente (ex.: feitiço global), deixando todos com 0 PV. P1 termina com 15 PV. Todos têm AE na média.

**Parâmetros**:
- **P1 (Vencedor)**: RP = 100, TV = (20-8)/20*100 = 60, ER = 3/3*100 = 100, PV = 15/40*100 = 37,5, AE = 50.
- **P2 (2º)**: RP = 30, TV = 60, ER = 0, PV = 0, AE = 50.
- **P3 (3º)**: RP = 20, TV = 60, ER = 0, PV = 0, AE = 50.
- **P4 (4º)**: RP = 10, TV = 60, ER = 0, PV = 0, AE = 50.

**Fórmula**:
```
ID = (0,4 × RP) + (0,2 × TV) + (0,2 × ER) + (0,1 × PV) + (0,1 × AE)
```

**Cálculo**:
| Jogador | Colocação | RP (Resultado da Partida, 40%) | TV (Turno de Vitória, 20%) | ER (Eliminações Realizadas, 20%) | PV (Pontos de Vida Restantes, 10%) | AE (Ações Estratégicas, 10%) | ID (%) |
|---------|-----------|--------------------------------|---------------------------|----------------------------------|------------------------------------|-----------------------------|--------|
| P1      | 1º        | 100                            | 60                        | 100                              | 37,5                               | 50                          | (0,4×100) + (0,2×60) + (0,2×100) + (0,1×37,5) + (0,1×50) = 40 + 12 + 20 + 3,75 + 5 = **80,75** |
| P2      | 2º        | 30                             | 60                        | 0                                | 0                                  | 50                          | (0,4×30) + (0,2×60) + (0,2×0) + (0,1×0) + (0,1×50) = 12 + 12 + 0 + 0 + 5 = **29,00** |
| P3      | 3º        | 20                             | 60                        | 0                                | 0                                  | 50                          | (0,4×20) + (0,2×60) + (0,2×0) + (0,1×0) + (0,1×50) = 8 + 12 + 0 + 0 + 5 = **25,00** |
| P4      | 4º        | 10                             | 60                        | 0                                | 0                                  | 50                          | (0,4×10) + (0,2×60) + (0,2×0) + (0,1×0) + (0,1×50) = 4 + 12 + 0 + 0 + 5 = **21,00** |

## Mesa 2: Vitória Isolada (Oponentes Zerados, Eliminações por Diferentes Jogadores)
**Contexto**: P5 vence no turno 8, eliminando P8 (último oponente). P6 elimina P7, P7 elimina P6, todos com 0 PV. P5 termina com 15 PV. Todos têm AE na média.

**Parâmetros**:
- **P5 (Vencedor)**: RP = 100, TV = 60, ER = 1/3*100 = 33,33, PV = 37,5, AE = 50.
- **P6 (2º)**: RP = 30, TV = 60, ER = 1/3*100 = 33,33, PV = 0, AE = 50.
- **P7 (3º)**: RP = 20, TV = 60, ER = 1/3*100 = 33,33, PV = 0, AE = 50.
- **P8 (4º)**: RP = 10, TV = 60, ER = 0, PV = 0, AE = 50.

**Fórmula**:
```
ID = (0,4 × RP) + (0,2 × TV) + (0,2 × ER) + (0,1 × PV) + (0,1 × AE)
```

**Cálculo**:
| Jogador | Colocação | RP (Resultado da Partida, 40%) | TV (Turno de Vitória, 20%) | ER (Eliminações Realizadas, 20%) | PV (Pontos de Vida Restantes, 10%) | AE (Ações Estratégicas, 10%) | ID (%) |
|---------|-----------|--------------------------------|---------------------------|----------------------------------|------------------------------------|-----------------------------|--------|
| P5      | 1º        | 100                            | 60                        | 33,33                            | 37,5                               | 50                          | (0,4×100) + (0,2×60) + (0,2×33,33) + (0,1×37,5) + (0,1×50) = 40 + 12 + 6,67 + 3,75 + 5 = **67,42** |
| P6      | 2º        | 30                             | 60                        | 33,33                            | 0                                  | 50                          | (0,4×30) + (0,2×60) + (0,2×33,33) + (0,1×0) + (0,1×50) = 12 + 12 + 6,67 + 0 + 5 = **35,67** |
| P7      | 3º        | 20                             | 60                        | 33,33                            | 0                                  | 50                          | (0,4×20) + (0,2×60) + (0,2×33,33) + (0,1×0) + (0,1×50) = 8 + 12 + 6,67 + 0 + 5 = **31,67** |
| P8      | 4º        | 10                             | 60                        | 0                                | 0                                  | 50                          | (0,4×10) + (0,2×60) + (0,2×0) + (0,1×0) + (0,1×50) = 4 + 12 + 0 + 0 + 5 = **21,00** |

## Mesa 3: Vitória Isolada (Combo Infinito, Sem Eliminações Parciais)
**Contexto**: P9 vence no turno 8 com um combo infinito, sem eliminações diretas. P10, P11 e P12 (3 oponentes ativos) são considerados eliminados pelo combo. P9 termina com 20 PV. Todos têm AE na média.

**Parâmetros**:
- **P9 (Vencedor)**: RP = 100, TV = 60, ER = 3/3*100 = 100 (3 oponentes ativos eliminados pelo combo), PV = 50, AE = 50.
- **P10 (2º)**: RP = 30, TV = 60, ER = 0, PV = 15/40*100 = 37,5, AE = 50.
- **P11 (3º)**: RP = 20, TV = 60, ER = 0, PV = 10/40*100 = 25, AE = 50.
- **P12 (4º)**: RP = 10, TV = 60, ER = 0, PV = 5/40*100 = 12,5, AE = 50.

**Fórmula**:
```
ID = (0,4 × RP) + (0,2 × TV) + (0,2 × ER) + (0,1 × PV) + (0,1 × AE)
```

**Cálculo**:
| Jogador | Colocação | RP (Resultado da Partida, 40%) | TV (Turno de Vitória, 20%) | ER (Eliminações Realizadas, 20%) | PV (Pontos de Vida Restantes, 10%) | AE (Ações Estratégicas, 10%) | ID (%) |
|---------|-----------|--------------------------------|---------------------------|----------------------------------|------------------------------------|-----------------------------|--------|
| P9      | 1º        | 100                            | 60                        | 100                              | 50                                 | 50                          | (0,4×100) + (0,2×60) + (0,2×100) + (0,1×50) + (0,1×50) = 40 + 12 + 20 + 5 + 5 = **82,00** |
| P10     | 2º        | 30                             | 60                        | 0                                | 37,5                               | 50                          | (0,4×30) + (0,2×60) + (0,2×0) + (0,1×37,5) + (0,1×50) = 12 + 12 + 0 + 3,75 + 5 = **32,75** |
| P11     | 3º        | 20                             | 60                        | 0                                | 25                                 | 50                          | (0,4×20) + (0,2×60) + (0,2×0) + (0,1×25) + (0,1×50) = 8 + 12 + 0 + 2,5 + 5 = **27,50** |
| P12     | 4º        | 10                             | 60                        | 0                                | 12,5                               | 50                          | (0,4×10) + (0,2×60) + (0,2×0) + (0,1×12,5) + (0,1×50) = 4 + 12 + 0 + 1,25 + 5 = **22,25** |

## Mesa 4: Vitória Isolada (Combo Infinito, Eliminação por Outro Jogador)
**Contexto**: P13 vence no turno 8 com um combo infinito, sem eliminações diretas. P14 elimina P16 diretamente (ex.: dano de combate) antes do combo. P13 considera P14, P15 e P16 (3 oponentes ativos) eliminados pelo combo. P13 termina com 20 PV. Todos têm AE na média.

**Parâmetros**:
- **P13 (Vencedor)**: RP = 100, TV = 60, ER = 3/3*100 = 100 (3 oponentes ativos eliminados pelo combo), PV = 50, AE = 50.
- **P14 (2º)**: RP = 30, TV = 60, ER = 1/3*100 = 33,33, PV = 15/40*100 = 37,5, AE = 50.
- **P15 (3º)**: RP = 20, TV = 60, ER = 0, PV = 10/40*100 = 25, AE = 50.
- **P16 (4º)**: RP = 10, TV = 60, ER = 0, PV = 0, AE = 50.

**Fórmula**:
```
ID = (0,4 × RP) + (0,2 × TV) + (0,2 × ER) + (0,1 × PV) + (0,1 × AE)
```

**Cálculo**:
| Jogador | Colocação | RP (Resultado da Partida, 40%) | TV (Turno de Vitória, 20%) | ER (Eliminações Realizadas, 20%) | PV (Pontos de Vida Restantes, 10%) | AE (Ações Estratégicas, 10%) | ID (%) |
|---------|-----------|--------------------------------|---------------------------|----------------------------------|------------------------------------|-----------------------------|--------|
| P13     | 1º        | 100                            | 60                        | 100                              | 50                                 | 50                          | (0,4×100) + (0,2×60) + (0,2×100) + (0,1×50) + (0,1×50) = 40 + 12 + 20 + 5 + 5 = **82,00** |
| P14     | 2º        | 30                             | 60                        | 33,33                            | 37,5                               | 50                          | (0,4×30) + (0,2×60) + (0,2×33,33) + (0,1×37,5) + (0,1×50) = 12 + 12 + 6,67 + 3,75 + 5 = **39,42** |
| P15     | 3º        | 20                             | 60                        | 0                                | 25                                 | 50                          | (0,4×20) + (0,2×60) + (0,2×0) + (0,1×25) + (0,1×50) = 8 + 12 + 0 + 2,5 + 5 = **27,50** |
| P16     | 4º        | 10                             | 60                        | 0                                | 0                                  | 50                          | (0,4×10) + (0,2×60) + (0,2×0) + (0,1×0) + (0,1×50) = 4 + 12 + 0 + 0 + 5 = **21,00** |

## Mesa 5: Empate (Todos com Mesma Vida)
**Contexto**: P17, P18, P19 e P20 empatam em 1º lugar no turno 12 (ex.: tempo esgotado). Nenhum jogador é eliminado, todos com 20 PV. AE na média.

**Parâmetros**:
- **P17, P18, P19, P20**: RP = 50, TV = (20-12)/20*100 = 40, ER = 0, PV = 20/40*100 = 50, AE = 50.

**Fórmula**:
```
ID = (0,4 × RP) + (0,2 × TV) + (0,2 × ER) + (0,1 × PV) + (0,1 × AE)
```

**Cálculo**:
| Jogador | Colocação | RP (Resultado da Partida, 40%) | TV (Turno de Vitória, 20%) | ER (Eliminações Realizadas, 20%) | PV (Pontos de Vida Restantes, 10%) | AE (Ações Estratégicas, 10%) | ID (%) |
|---------|-----------|--------------------------------|---------------------------|----------------------------------|------------------------------------|-----------------------------|--------|
| P17     | 1º (empate) | 50                           | 40                        | 0                                | 50                                 | 50                          | (0,4×50) + (0,2×40) + (0,2×0) + (0,1×50) + (0,1×50) = 20 + 8 + 0 + 5 + 5 = **38,00** |
| P18     | 1º (empate) | 50                           | 40                        | 0                                | 50                                 | 50                          | (0,4×50) + (0,2×40) + (0,2×0) + (0,1×50) + (0,1×50) = 20 + 8 + 0 + 5 + 5 = **38,00** |
| P19     | 1º (empate) | 50                           | 40                        | 0                                | 50                                 | 50                          | (0,4×50) + (0,2×40) + (0,2×0) + (0,1×50) + (0,1×50) = 20 + 8 + 0 + 5 + 5 = **38,00** |
| P20     | 1º (empate) | 50                           | 40                        | 0                                | 50                                 | 50                          | (0,4×50) + (0,2×40) + (0,2×0) + (0,1×50) + (0,1×50) = 20 + 8 + 0 + 5 + 5 = **38,00** |

## Mesa 6: Empate (Vidas Diferentes)
**Contexto**: P21, P22, P23 e P24 empatam em 1º lugar no turno 12, sem eliminações. Cada jogador tem PV diferentes. AE na média.

**Parâmetros**:
- **P21**: RP = 50, TV = 40, ER = 0, PV = 30/40*100 = 75, AE = 50.
- **P22**: RP = 50, TV = 40, ER = 0, PV = 20/40*100 = 50, AE = 50.
- **P23**: RP = 50, TV = 40, ER = 0, PV = 10/40*100 = 25, AE = 50.
- **P24**: RP = 50, TV = 40, ER = 0, PV = 5/40*100 = 12,5, AE = 50.

**Fórmula**:
```
ID = (0,4 × RP) + (0,2 × TV) + (0,2 × ER) + (0,1 × PV) + (0,1 × AE)
```

**Cálculo**:
| Jogador | Colocação | RP (Resultado da Partida, 40%) | TV (Turno de Vitória, 20%) | ER (Eliminações Realizadas, 20%) | PV (Pontos de Vida Restantes, 10%) | AE (Ações Estratégicas, 10%) | ID (%) |
|---------|-----------|--------------------------------|---------------------------|----------------------------------|------------------------------------|-----------------------------|--------|
| P21     | 1º (empate) | 50                           | 40                        | 0                                | 75                                 | 50                          | (0,4×50) + (0,2×40) + (0,2×0) + (0,1×75) + (0,1×50) = 20 + 8 + 0 + 7,5 + 5 = **40,50** |
| P22     | 1º (empate) | 50                           | 40                        | 0                                | 50                                 | 50                          | (0,4×50) + (0,2×40) + (0,2×0) + (0,1×50) + (0,1×50) = 20 + 8 + 0 + 5 + 5 = **38,00** |
| P23     | 1º (empate) | 50                           | 40                        | 0                                | 25                                 | 50                          | (0,4×50) + (0,2×40) + (0,2×0) + (0,1×25) + (0,1×50) = 20 + 8 + 0 + 2,5 + 5 = **35,50** |
| P24     | 1º (empate) | 50                           | 40                        | 0                                | 12,5                               | 50                          | (0,4×50) + (0,2×40) + (0,2×0) + (0,1×12,5) + (0,1×50) = 20 + 8 + 0 + 1,25 + 5 = **34,25** |

## Ranking Geral
Com base nos IDs calculados, o ranking dos 24 jogadores é:

| Posição | Jogador | Mesa | ID (%) |
|---------|---------|------|--------|
| 1       | P9      | 3    | 82,00  |
| 2       | P13     | 4    | 82,00  |
| 3       | P1      | 1    | 80,75  |
| 4       | P5      | 2    | 67,42  |
| 5       | P21     | 6    | 40,50  |
| 6       | P14     | 4    | 39,42  |
| 7       | P17     | 5    | 38,00  |
| 8       | P18     | 5    | 38,00  |
| 9       | P19     | 5    | 38,00  |
| 10      | P20     | 5    | 38,00  |
| 11      | P22     | 6    | 38,00  |
| 12      | P6      | 2    | 35,67  |
| 13      | P23     | 6    | 35,50  |
| 14      | P10     | 3    | 32,75  |
| 15      | P7      | 2    | 31,67  |
| 16      | P24     | 6    | 34,25  |
| 17      | P2      | 1    | 29,00  |
| 18      | P11     | 3    | 27,50  |
| 19      | P15     | 4    | 27,50  |
| 20      | P3      | 1    | 25,00  |
| 21      | P12     | 3    | 22,25  |
| 22      | P4      | 1    | 21,00  |
| 23      | P8      | 2    | 21,00  |
| 24      | P16     | 4    | 21,00  |

## Observações
- **Mesa 1**: P1 alcança ID elevado (80,75%) devido a RP (100), ER (100, eliminou todos simultaneamente) e PV (37,5). Perdedores (P2, P3, P4) têm IDs baixos (29,00% a 21,00%) devido a RP reduzido, PV zerado e ER = 0.
- **Mesa 2**: P5 tem ID (67,42%), inferior a Mesa 1 devido a ER = 33,33 (uma eliminação). P6 e P7 se beneficiam de ER = 33,33, com IDs (35,67% e 31,67%) superiores a outros perdedores. P8, sem eliminações, tem ID baixo (21,00%).
- **Mesa 3**: P9, com vitória por combo, tem ID (82,00%), ligeiramente superior a P1 (80,75%) devido a maior PV (50 vs. 37,5) e ER = 100 (3 oponentes ativos eliminados pelo combo). Perdedores (P10, P11, P12) têm IDs variados (22,25% a 32,75%) devido a PV.
- **Mesa 4**: P13, com vitória por combo e sem eliminações diretas, mantém ID (82,00%) com ER = 100 (3 oponentes ativos eliminados pelo combo). P14, com uma eliminação direta (ER = 33,33), tem ID elevado (39,42%) entre perdedores, beneficiado por PV = 37,5. P15 e P16 têm IDs menores (27,50% e 21,00%), com P16 penalizado por PV = 0.
- **Mesa 5**: Empate com PV iguais resulta em IDs idênticos (38,00%) para P17, P18, P19 e P20.
- **Mesa 6**: Empate com PV diferentes gera IDs variados (34,25% a 40,50%), com P21 liderando (40,50%) devido a PV = 75.
- **Impacto da Mudança na Mesa 4**: P13 mantém ID = 82,00%, pois ER = 100 (3 oponentes ativos), mesmo sem eliminações diretas. P14 ganha ID (39,42%) maior que outros perdedores de mesas com vitórias (ex.: P2, 29,00%) devido a ER = 33,33 e PV = 37,5, refletindo sua contribuição ativa. P16, eliminado por P14, tem ID baixo (21,00%) devido a PV = 0.
- **Ranking**: Vencedores por combo (P9, P13) lideram (82,00%), seguidos por P1 (80,75%). P5 (Mesa 2, 67,42%) tem ID menor devido a ER = 33,33. P14 (Mesa 4, 39,42%) se destaca entre perdedores, superando alguns empatados (ex.: P17-P20, 38,00%) devido a ER e PV.

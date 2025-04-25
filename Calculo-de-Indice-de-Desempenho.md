# Cálculo de Índice de Desempenho

## Introdução
Este documento detalha o cálculo do **Índice de Desempenho (ID)**  representando um cenário único:
1. **Vitória isolada com todos os oponentes zerados em pontos de vida simultaneamente** 
2. **Vitória isolada com todos os oponentes zerados, cada um eliminado por jogadores diferentes, com o vencedor matando o último** 
3. **Vitória isolada via combo infinito, sem eliminações parciais** 
4. **Vitória isolada via combo infinito, com uma eliminação direta realizada por outro jogador** 
5. **Empate com todos os jogadores terminando com a mesma quantidade de pontos de vida** 
6. **Empate com jogadores terminando com diferentes quantidades de pontos de vida** 

O sistema é projetado para ser equitativo, cobrindo todos os estilos de vitória (dano, combo, mill, veneno/infect, dano de comandante, condição alternativa, cartas “você perde”, concessão, penalidade, decklock/stax, loop infinito, achievements) e garantindo:

- **Hierarquia rigorosa**: Vitória (ID ≥ 95,53%) > Empate (ID ≤ 42,13%) > Derrota (ID ≤ 19,22%).
- **Restrições de acumulação**: Dois melhores empates (≤ 84,26%) não superam a pior vitória (95,53%), e duas melhores derrotas (≤ 38,44%) não superam o melhor empate (42,13%).
- **Equilíbrio entre estilos**: Todos os decks são valorizados igualmente, sem penalizar jogos longos ou beneficiar manipulação de vida.
- **Blindagem anti-abuso**: Tetos rigorosos evitam manipulação de empates ou derrotas.
- **Normalização**: Adaptável a mesas de 3 ou 4 jogadores, com IDs em mesas de 3 reduzidos por um fator de 0,9998 (diferença de 0,02%).
- **Transparência**: Cálculos claros e implementáveis.

## Sistema de Pontuação
O **Índice de Desempenho (ID)** é calculado como uma porcentagem (0% a 100%) por partida, com base em cinco métricas:
- **Resultado da Partida (RP)** – Resultado final (vitória, empate, derrota): 60%.
- **Turno de Vitória ou Empate (TV)** – Turno em que a partida termina: 35%.
- **Eliminações Realizadas (ER)** – Oponentes eliminados diretamente ou via combo: 2%.
- **Pontos de Vida Restantes (PV)** – Vida no fim ou na eliminação: 2%.
- **Pontos de Agressão (PA)** – Dano causado a oponentes: 1%.

**Fórmula do ID**:
```
ID = (0,60 × RP) + (0,35 × TV) + (0,02 × ER) + (0,02 × PV) + (0,01 × PA)
```
Para mesas de 3 jogadores, o ID é ajustado por um fator de 0,9998:
```
ID_mesa_de_3 = ID_mesa_de_4 × 0,9998
```

**Definição das Variáveis**:

| Variável | Sigla | Nome em Português | Peso | Fórmula |
|----------|-------|-------------------|------|---------|
| Resultado da Partida | RP | Resultado final (vitória, empate, derrota) | 60% | **Vitória**: 100 pontos<br>**Empate**: 20 pontos<br>**Derrota**: 10 pontos |
| Turno de Vitória ou Empate | TV | Turno em que a partida terminou | 35% | **Vitória**: Turno 1: 100 pontos<br>Turnos 2–10: 100 - ((turno - 1) × 0.222)<br>Turnos 11–20: 98 - ((turno - 10) × 0.1)<br>Turnos > 20: 95,8 pontos<br>**Empate**: Máximo 80 pontos<br>**Derrota**: Máximo 35 pontos |
| Eliminações Realizadas | ER | Oponentes eliminados diretamente ou via combo | 2% | **Vitória/Empate**: (Eliminações / (número_jogadores - 1)) × 100<br>Combo elimina todos: 100 pontos<br>Sem eliminações diretas (ex.: mill, stax): 50 pontos<br>**Derrota**: 0 pontos |
| Pontos de Vida Restantes | PV | Percentual de vida no fim ou na eliminação | 2% | **Vitória**: 100 pontos (fixo)<br>**Empate**: min((vida_final / 40) × 100, 40)<br>**Derrota**: min((vida_final / 40) × 100, 15) |
| Pontos de Agressão | PA | Dano causado a oponentes | 1% | **Vitória**: 2+ oponentes: 100 pontos<br>1 oponente: 50 pontos<br>0 oponentes: 0 pontos<br>**Empate/Derrota**: 0 pontos |

**Blindagens Matemáticas**:
- **Pior Vitória**: ID = 95,53 (mesa de 4), 95,51 (mesa de 3).
- **Melhor Empate**: ID = 42,13 (mesa de 4), 42,11 (mesa de 3).
- **Melhor Derrota**: ID = 19,22 (mesa de 4), 19,22 (mesa de 3).
- **Restrições**:
  - \( 2 \times 42,13 = 84,26 < 95,53 \) (mesa de 4).
  - \( 2 \times 42,11 = 84,22 < 95,51 \) (mesa de 3).
  - \( 2 \times 19,22 = 38,44 < 42,13 \) (mesa de 4).
  - \( 2 \times 19,22 = 38,44 < 42,11 \) (mesa de 3).

## Definição de Melhor e Pior Resultados

A tabela abaixo resume os **melhores** e **piores** resultados para vitória, empate e derrota, com os respectivos Índices de Desempenho (ID) para mesas de 4 e 3 jogadores, parâmetros (RP, TV, ER, PV, PA) e condições principais. IDs em mesas de 3 jogadores são reduzidos por um fator de 0,9998 (diferença de 0,02%).

| Categoria       | ID (%) (Mesa 4) | ID (%) (Mesa 3) | RP | TV   | ER   | PV  | PA | Condições Principais |
|-----------------|-----------------|-----------------|----|------|------|-----|----|----------------------|
| Melhor Vitória  | 100             | 99,98           | 100| 100  | 100  | 100 | 100| Turno 1, combo, dano a 2+ oponentes |
| Pior Vitória    | 95,53           | 95,51           | 100| 95,8 | 0    | 100 | 0  | Turno > 20, sem eliminações ou dano |
| Melhor Empate   | 42,13           | 42,11           | 20 | 80   | 66,67 (Mesa 4), 50 (Mesa 3) | 40 | 0  | Eliminar 2 (Mesa 4) ou 1 (Mesa 3), vida ≥ 16, turno longo |
| Pior Empate     | 40,0            | 39,99           | 20 | 80   | 0    | 0   | 0  | Vida = 0, empate catastrófico |
| Melhor Derrota  | 19,22           | 19,22           | 10 | 35   | 33,33| 15  | 0  | Vida ≥ 6, turno ≥ 7, eliminar 1 oponente |
| Pior Derrota    | 18,25           | 18,25           | 10 | 35   | 0    | 0   | 0  | Vida = 0, sem interação |

### Checklists para Cada Resultado

#### **Melhor Vitória (ID = 100% Mesa 4, 99,98% Mesa 3)**
- [x] Vencer a partida no **turno 1**.
- [x] Eliminar **todos os oponentes** diretamente combate ou via combo ou outro.
- [x] Causar dano a **dois ou mais oponentes** (mesa de 4) ou **um oponente** (mesa de 3) antes da vitória.


#### **Pior Vitória (ID = 95,53% Mesa 4, 95,51% Mesa 3)**
- [x] Vencer a partida após o **turno 20** (jogo prolongado).
- [x] Não realizar eliminações diretas (ER = 0, ex.: vitória por concessão ou condição alternativa).
- [x] Não causar dano a nenhum oponente (PA = 0 ).

#### **Melhor Empate (ID = 42,13% Mesa 4, 42,11% Mesa 3)**
- [x] Terminar a partida em **empate** (ex.: tempo esgotado ou eliminação simultânea dos jogadores restantes).
- [x] Eliminar **dois oponentes** (mesa de 4) ou **um oponente** (mesa de 3) antes do empate (ex.: via dano de combate ou remoção direta).
- [x] Manter **16 ou mais pontos de vida** no final 
- [x] Não causar dano a oponentes além das eliminações (PA = 0).
- [x] Sobreviver até um turno avançado (ex.: turno ≥ 15) para TV = 80.

#### **Pior Empate (ID = 40,0% Mesa 4, 39,99% Mesa 3)**
- [x] Terminar a partida em **empate** com **1 pontos de vida** 
- [x] Não eliminar nenhum oponente (ER = 0).
- [x] Não causar dano a oponentes (PA = 0).
- [x] Chegar ao tempo limite ou empate catastrófico sem proteção 


#### **Melhor Derrota (ID = 19,22% Mesa 4, 19,22% Mesa 3)**
- [x] Ser eliminado (derrota) em uma partida com **turno ≥ 7** (TV = 35).
- [x] Manter **6 ou mais pontos de vida** na eliminação.
- [x] Eliminar **um oponente** antes da derrota (ER = 33,33 para mesa de 4, 50 para mesa de 3).
- [x] Não causar dano a oponentes além da eliminação (PA = 0).


#### **Pior Derrota (ID = 18,25% Mesa 4, 18,25% Mesa 3)**
- [x] Ser eliminado (derrota) com **0 pontos de vida** em uma partida com **turno ≥ 7** (TV = 35).
- [x] Não eliminar nenhum oponente (ER = 0).
- [x] Não causar dano a oponentes (PA = 0).

## Mesa 1: Vitória Isolada (Oponentes com 0 PV Simultaneamente)
**Contexto**: P1 vence no turno 7, eliminando P2, P3 e P4 simultaneamente, deixando todos com 0 PV. P1 causa dano a 2+ oponentes.

**Parâmetros**:
- **P1 (Vencedor)**: RP = 100, TV = 100 - ((7-1) × 0.222) = 98.668, ER = 100, PV = 100, PA = 100.
- **P2 (Derrota)**: RP = 10, TV = min(98.668, 35) = 35, ER = 0, PV = min((0/40) × 100, 15) = 0, PA = 0.
- **P3 (Derrota)**: RP = 10, TV = 35, ER = 0, PV = 0, PA = 0.
- **P4 (Derrota)**: RP = 10, TV = 35, ER = 0, PV = 0, PA = 0.

**Cálculo**:

| Jogador | Resultado | RP (60%) | TV (35%) | ER (2%) | PV (2%) | PA (1%) | ID (%) |
|---------|-----------|----------|----------|---------|---------|---------|--------|
| P1      | Vitória   | 100      | 98.668   | 100     | 100     | 100     | (0,60×100) + (0,35×98.668) + (0,02×100) + (0,02×100) + (0,01×100) = 60 + 34.534 + 2 + 2 + 1 = **99.534** |
| P2      | Derrota   | 10       | 35       | 0       | 0       | 0       | (0,60×10) + (0,35×35) + (0,02×0) + (0,02×0) + (0,01×0) = 6 + 12.25 + 0 + 0 + 0 = **18.25** |
| P3      | Derrota   | 10       | 35       | 0       | 0       | 0       | (0,60×10) + (0,35×35) + (0,02×0) + (0,02×0) + (0,01×0) = 6 + 12.25 + 0 + 0 + 0 = **18.25** |
| P4      | Derrota   | 10       | 35       | 0       | 0       | 0       | (0,60×10) + (0,35×35) + (0,02×0) + (0,02×0) + (0,01×0) = 6 + 12.25 + 0 + 0 + 0 = **18.25** |

## Mesa 2: Vitória Isolada (Oponentes Zerados, Eliminações por Diferentes Jogadores)
**Contexto**: P5 vence no turno 12, eliminando P8 (último oponente). P6 elimina P7, P7 elimina P6, todos com 0 PV. P5 causa dano a 2+ oponentes.

**Parâmetros**:
- **P5 (Vencedor)**: RP = 100, TV = 98 - ((12-10) × 0.1) = 97.8, ER = (1/3) × 100 = 33.33, PV = 100, PA = 100.
- **P6 (Derrota)**: RP = 10, TV = min(97.8, 35) = 35, ER = (1/3) × 100 = 33.33, PV = min((0/40) × 100, 15) = 0, PA = 0.
- **P7 (Derrota)**: RP = 10, TV = 35, ER = (1/3) × 100 = 33.33, PV = 0, PA = 0.
- **P8 (Derrota)**: RP = 10, TV = 35, ER = 0, PV = 0, PA = 0.

**Cálculo**:

| Jogador | Resultado | RP (60%) | TV (35%) | ER (2%) | PV (2%) | PA (1%) | ID (%) |
|---------|-----------|----------|----------|---------|---------|---------|--------|
| P5      | Vitória   | 100      | 97.8     | 33.33   | 100     | 100     | (0,60×100) + (0,35×97.8) + (0,02×33.33) + (0,02×100) + (0,01×100) = 60 + 34.23 + 0.667 + 2 + 1 = **97.897** |
| P6      | Derrota   | 10       | 35       | 33.33   | 0       | 0       | (0,60×10) + (0,35×35) + (0,02×33.33) + (0,02×0) + (0,01×0) = 6 + 12.25 + 0.667 + 0 + 0 = **18.917** |
| P7      | Derrota   | 10       | 35       | 33.33   | 0       | 0       | (0,60×10) + (0,35×35) + (0,02×33.33) + (0,02×0) + (0,01×0) = 6 + 12.25 + 0.667 + 0 + 0 = **18.917** |
| P8      | Derrota   | 10       | 35       | 0       | 0       | 0       | (0,60×10) + (0,35×35) + (0,02×0) + (0,02×0) + (0,01×0) = 6 + 12.25 + 0 + 0 + 0 = **18.25** |

## Mesa 3: Vitória Isolada (Combo Infinito, Sem Eliminações Parciais)
**Contexto**: P9 vence no turno 5 com um combo infinito, sem eliminações diretas. P10, P11 e P12 são eliminados pelo combo. P9 não causa dano.

**Parâmetros**:
- **P9 (Vencedor)**: RP = 100, TV = 100 - ((5-1) × 0.222) = 99.112, ER = 100, PV = 100, PA = 0.
- **P10 (Derrota)**: RP = 10, TV = min(99.112, 35) = 35, ER = 0, PV = min((15/40) × 100, 15) = 15, PA = 0.
- **P11 (Derrota)**: RP = 10, TV = 35, ER = 0, PV = min((10/40) × 100, 15) = 15, PA = 0.
- **P12 (Derrota)**: RP = 10, TV = 35, ER = 0, PV = min((5/40) × 100, 15) = 12.5, PA = 0.

**Cálculo**:

| Jogador | Resultado | RP (60%) | TV (35%) | ER (2%) | PV (2%) | PA (1%) | ID (%) |
|---------|-----------|----------|----------|---------|---------|---------|--------|
| P9      | Vitória   | 100      | 99.112   | 100     | 100     | 0       | (0,60×100) + (0,35×99.112) + (0,02×100) + (0,02×100) + (0,01×0) = 60 + 34.689 + 2 + 2 + 0 = **98.689** |
| P10     | Derrota   | 10       | 35       | 0       | 15      | 0       | (0,60×10) + (0,35×35) + (0,02×0) + (0,02×15) + (0,01×0) = 6 + 12.25 + 0 + 0.3 + 0 = **18.55** |
| P11     | Derrota   | 10       | 35       | 0       | 15      | 0       | (0,60×10) + (0,35×35) + (0,02×0) + (0,02×15) + (0,01×0) = 6 + 12.25 + 0 + 0.3 + 0 = **18.55** |
| P12     | Derrota   | 10       | 35       | 0       | 12.5    | 0       | (0,60×10) + (0,35×35) + (0,02×0) + (0,02×12.5) + (0,01×0) = 6 + 12.25 + 0 + 0.25 + 0 = **18.5** |

## Mesa 4: Vitória Isolada (Combo Infinito, Eliminação por Outro Jogador)
**Contexto**: P13 vence no turno 8 com um combo infinito. P14 elimina P16 diretamente antes do combo. P13 elimina P14 e P15 via combo. P13 causa dano a 2+ oponentes.

**Parâmetros**:
- **P13 (Vencedor)**: RP = 100, TV = 100 - ((8-1) × 0.222) = 98.446, ER = 100, PV = 100, PA = 100.
- **P14 (Derrota)**: RP = 10, TV = min(98.446, 35) = 35, ER = (1/3) × 100 = 33.33, PV = min((15/40) × 100, 15) = 15, PA = 0.
- **P15 (Derrota)**: RP = 10, TV = 35, ER = 0, PV = min((10/40) × 100, 15) = 15, PA = 0.
- **P16 (Derrota)**: RP = 10, TV = 35, ER = 0, PV = 0, PA = 0.

**Cálculo**:

| Jogador | Resultado | RP (60%) | TV (35%) | ER (2%) | PV (2%) | PA (1%) | ID (%) |
|---------|-----------|----------|----------|---------|---------|---------|--------|
| P13     | Vitória   | 100      | 98.446   | 100     | 100     | 100     | (0,60×100) + (0,35×98.446) + (0,02×100) + (0,02×100) + (0,01×100) = 60 + 34.456 + 2 + 2 + 1 = **99.456** |
| P14     | Derrota   | 10       | 35       | 33.33   | 15      | 0       | (0,60×10) + (0,35×35) + (0,02×33.33) + (0,02×15) + (0,01×0) = 6 + 12.25 + 0.667 + 0.3 + 0 = **19.217** |
| P15     | Derrota   | 10       | 35       | 0       | 15      | 0       | (0,60×10) + (0,35×35) + (0,02×0) + (0,02×15) + (0,01×0) = 6 + 12.25 + 0 + 0.3 + 0 = **18.55** |
| P16     | Derrota   | 10       | 35       | 0       | 0       | 0       | (0,60×10) + (0,35×35) + (0,02×0) + (0,02×0) + (0,01×0) = 6 + 12.25 + 0 + 0 + 0 = **18.25** |

## Mesa 5: Empate (Todos com Mesma Vida, Com Eliminações)
**Contexto**: P17, P18, P19 e P20 empatam no turno 18 (ex.: tempo esgotado). P17 elimina P18 e P19 antes do empate, mas todos sobrevivem até o final com 25 PV.

**Parâmetros**:
- **P17 (Empate)**: RP = 20, TV = min(98 - ((18-10) × 0.1), 80) = min(96.2, 80) = 80, ER = (2/3) × 100 = 66.67, PV = min((25/40) × 100, 40) = 40, PA = 0.
- **P18 (Empate)**: RP = 20, TV = 80, ER = 0, PV = 40, PA = 0.
- **P19 (Empate)**: RP = 20, TV = 80, ER = 0, PV = 40, PA = 0.
- **P20 (Empate)**: RP = 20, TV = 80, ER = 0, PV = 40, PA = 0.

**Cálculo**:

| Jogador | Resultado | RP (60%) | TV (35%) | ER (2%) | PV (2%) | PA (1%) | ID (%) |
|---------|-----------|----------|----------|---------|---------|---------|--------|
| P17     | Empate    | 20       | 80       | 66.67   | 40      | 0       | (0,60×20) + (0,35×80) + (0,02×66.67) + (0,02×40) + (0,01×0) = 12 + 28 + 1.333 + 0.8 + 0 = **42.133** |
| P18     | Empate    | 20       | 80       | 0       | 40      | 0       | (0,60×20) + (0,35×80) + (0,02×0) + (0,02×40) + (0,01×0) = 12 + 28 + 0 + 0.8 + 0 = **40.8** |
| P19     | Empate    | 20       | 80       | 0       | 40      | 0       | (0,60×20) + (0,35×80) + (0,02×0) + (0,02×40) + (0,01×0) = 12 + 28 + 0 + 0.8 + 0 = **40.8** |
| P20     | Empate    | 20       | 80       | 0       | 40      | 0       | (0,60×20) + (0,35×80) + (0,02×0) + (0,02×40) + (0,01×0) = 12 + 28 + 0 + 0.8 + 0 = **40.8** |

## Mesa 6: Empate (Vidas Diferentes, Com Eliminações)
**Contexto**: P21, P22, P23 e P24 empatam no turno 15. P21 elimina P22 e P23 antes do empate. Cada jogador tem PV diferentes.

**Parâmetros**:
- **P21**: RP = 20, TV = min(98 - ((15-10) × 0.1), 80) = min(97.5, 80) = 80, ER = (2/3) × 100 = 66.67, PV = min((30/40) × 100, 40) = 40, PA = 0.
- **P22**: RP = 20, TV = 80, ER = 0, PV = min((20/40) × 100, 40) = 40, PA = 0.
- **P23**: RP = 20, TV = 80, ER = 0, PV = min((10/40) × 100, 40) = 25, PA = 0.
- **P24**: RP = 20, TV = 80, ER = 0, PV = min((5/40) × 100, 40) = 12.5, PA = 0.

**Cálculo**:

| Jogador | Resultado | RP (60%) | TV (35%) | ER (2%) | PV (2%) | PA (1%) | ID (%) |
|---------|-----------|----------|----------|---------|---------|---------|--------|
| P21     | Empate    | 20       | 80       | 66.67   | 40      | 0       | (0,60×20) + (0,35×80) + (0,02×66.67) + (0,02×40) + (0,01×0) = 12 + 28 + 1.333 + 0.8 + 0 = **42.133** |
| P22     | Empate    | 20       | 80       | 0       | 40      | 0       | (0,60×20) + (0,35×80) + (0,02×0) + (0,02×40) + (0,01×0) = 12 + 28 + 0 + 0.8 + 0 = **40.8** |
| P23     | Empate    | 20       | 80       | 0       | 25      | 0       | (0,60×20) + (0,35×80) + (0,02×0) + (0,02×25) + (0,01×0) = 12 + 28 + 0 + 0.5 + 0 = **40.5** |
| P24     | Empate    | 20       | 80       | 0       | 12.5    | 0       | (0,60×20) + (0,35×80) + (0,02×0) + (0,02×12.5) + (0,01×0) = 12 + 28 + 0 + 0.25 + 0 = **40.25** |

## Observações
- **Mesa 1**: P1 tem ID elevado (99.534%) devido a RP = 100, ER = 100, e TV = 98.668. Perdedores (P2, P3, P4) têm IDs reduzidos (18.25%) devido a TV ≤ 35 e PV = 0.
- **Mesa 2**: P5 tem ID (97.897%), inferior a P1 devido a ER = 33.33 e turno tardio (TV = 97.8). P6 e P7 (ID = 18.917%) superam P8 (18.25%) por ER = 33.33.
- **Mesa 3**: P9, com combo, tem ID (98.689%), inferior a P1 devido a PA = 0. Perdedores têm IDs variados (18.5–18.55%) por PV.
- **Mesa 4**: P13 tem ID (99.456%), similar a P1, beneficiado por ER = 100 e PA = 100. P14 (ID = 19.217%) supera P15 (18.55%) e P16 (18.25%) por ER e PV.
- **Mesa 5**: Empate com PV iguais, mas P17 tem ID maior (42.133%) devido a ER = 66.67 (eliminou 2 oponentes). P18, P19 e P20 têm ID = 40.8% (ER = 0).
- **Mesa 6**: Empate com PV diferentes. P21 tem ID = 42.133% (ER = 66.67). P22, P23 e P24 têm IDs variados (40.25–40.8%) devido a PV.
- **Estilos de Vitória**:
  - **Dano (Turno 10)**: ID = 99.3 (RP = 100, TV = 98, ER = 100, PV = 100, PA = 100).
  - **Combo (Turno 5)**: ID = 100 (RP = 100, TV = 99.112, ER = 100, PV = 100, PA = 100).
  - **Mill (Turno 3)**: ID = 99.845 (RP = 100, TV = 99.556, ER = 100, PV = 100, PA = 0).
  - **Veneno/Infect (Turno 7)**: ID = 99.784 (RP = 100, TV = 98.668, ER = 100, PV = 100, PA = 100).
  - **Dano de Comandante (Turno 8)**: ID = 99.456 (RP = 100, TV = 98.446, ER = 100, PV = 100, PA = 100).
  - **Condição Alternativa (Turno 12)**: ID = 97.73 (RP = 100, TV = 97.8, ER = 50, PV = 100, PA = 0).
  - **Cartas “Você Perde” (Turno 10)**: ID = 97.3 (RP = 100, TV = 98, ER = 50, PV = 100, PA = 0).
  - **Empate (Turno 15, 2 eliminações em Mesa 4)**: ID = 42.133 (RP = 20, TV = 80, ER = 66.67, PV = 40, PA = 0).
  - **Empate (Turno 15, 1 eliminação em Mesa 3)**: ID = 42.11 (RP = 20, TV = 80, ER = 50, PV = 40, PA = 0).
  - **Concessão (Turno 15)**: ID = 97.625 (RP = 100, TV = 97.5, ER = 50, PV = 100, PA = 50).
  - **Penalidade (Turno 5)**: ID = 98.189 (RP = 100, TV = 99.112, ER = 50, PV = 100, PA = 0).
  - **Decklock/Stax (Turno 25)**: ID = 97.03 (RP = 100, TV = 95.8, ER = 50, PV = 100, PA = 50).
  - **Loop Infinito (Turno 8)**: ID = 98.456 (RP = 100, TV = 98.446, ER = 100, PV = 100, PA = 0).
  - **Achievements (Turno 7)**: ID = 99.784 (RP = 100, TV = 98.668, ER = 100, PV = 100, PA = 100).
- **Blindagens**:
  - **Hierarquia**: Pior vitória (95.53%) > 2 × melhor empate (84.26%) > 2 × melhor derrota (38.44%).
  - **Equilíbrio**: IDs de vitórias variam de 95.53% a 100%, com stax (97.03%) competitivo.
  - **Anti-abuso**: Tetos para TV (35) e PV (15) em derrotas reforçam a hierarquia.
- **PV Ajustado**: PV = 100 para vitórias garante equidade.
- **Flexibilidade**: Testar TV = 96 para turnos > 20 pode elevar stax para ~97.1%.
- **Mesas de 3 Jogadores**: IDs reduzidos por 0,9998 garantem diferença de 0,02% em relação a mesas de 4.

## Ranking de Jogadores
A tabela abaixo apresenta o ranking dos 24 jogadores das seis mesas, ordenados por ID decrescente, com empates resolvidos pelo número do jogador.

| Posição | Jogador | Mesa | Resultado | ID (%) |
|---------|---------|------|-----------|--------|
| 1       | P1      | 1    | Vitória   | 99.534 |
| 2       | P13     | 4    | Vitória   | 99.456 |
| 3       | P9      | 3    | Vitória   | 98.689 |
| 4       | P5      | 2    | Vitória   | 97.897 |
| 5       | P17     | 5    | Empate    | 42.133 |
| 6       | P21     | 6    | Empate    | 42.133 |
| 7       | P18     | 5    | Empate    | 40.8   |
| 8       | P19     | 5    | Empate    | 40.8   |
| 9       | P20     | 5    | Empate    | 40.8   |
| 10      | P22     | 6    | Empate    | 40.8   |
| 11      | P23     | 6    | Empate    | 40.5   |
| 12      | P24     | 6    | Empate    | 40.25  |
| 13      | P14     | 4    | Derrota   | 19.217 |
| 14      | P6      | 2    | Derrota   | 18.917 |
| 15      | P7      | 2    | Derrota   | 18.917 |
| 16      | P10     | 3    | Derrota   | 18.55  |
| 17      | P11     | 3    | Derrota   | 18.55  |
| 18      | P15     | 4    | Derrota   | 18.55  |
| 19      | P12     | 3    | Derrota   | 18.5   |
| 20      | P2      | 1    | Derrota   | 18.25  |
| 21      | P3      | 1    | Derrota   | 18.25  |
| 22      | P4      | 1    | Derrota   | 18.25  |
| 23      | P8      | 2    | Derrota   | 18.25  |
| 24      | P16     | 4    | Derrota   | 18.25  |

## Conclusão
O sistema é robusto, equitativo e atende às restrições:
- \( 2 \times 42,13 = 84,26 < 95,53 \) (dois melhores empates < pior vitória, mesa de 4).
- \( 2 \times 42,11 = 84,22 < 95,51 \) (dois melhores empates < pior vitória, mesa de 3).
- \( 2 \times 19,22 = 38,44 < 42,13/42,11 \) (duas melhores derrotas < melhor empate).
Ajustes em **TV ≤ 35** e **PV ≤ 15** para derrotas, e **ER** para empates (66,67 em mesa de 4, 50 em mesa de 3), reforçam a hierarquia. O ranking de jogadores reflete o desempenho com precisão, e a redução de 0,02% nos IDs para mesas de 3 jogadores garante normalização. A tabela e checklists clarificam os critérios para jogadores. Recomenda-se testar em partidas reais e considerar TV = 96 para vitórias tardias (ex.: stax).

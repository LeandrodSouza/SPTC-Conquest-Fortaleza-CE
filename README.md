# SPTC-Conquest-Fortaleza-CE

# Sistema de Pontuação Torneio Commander - Conquest

## Introdução

### Objetivo
Desenvolver um sistema de pontuação para o torneio Commander - Conquest, utilizando o Índice de Desempenho (ID) com siglas RP, TV, ER, PV e AE. 
Projetado para torneios de 4 a 100 jogadores, o sistema avalia o desempenho em cenários variados de vitórias, empates e derrotas, promovendo matchmaking equilibrado, desempates e prevenção de colusão:

### Escopo
O sistema é projetado para torneios flexíveis, com 4 a 100 jogadores, organizados em mesas de 4 (ou menos mesa, se necessário). Ele abrange:
- Cálculo do ID com base em Resultado da Partida (RP), Turno de Vitória ou Empate (TV), Eliminações Realizadas (ER), Pontos de Vida Restantes (PV) e Ações Estratégicas (AE).
- Matchmaking baseado em ID médio.
- Critérios de desempate.
- Medidas anti-colusão.
- Suporte a cenários variados, como diferentes turnos, pontos de vida e eliminações.

## Visão Geral

### Descrição
O sistema calcula o **Índice de Desempenho (ID)** como uma porcentagem (0% a 100%) por partida, com base em cinco métricas:
- **Resultado da Partida (RP)**: Vitória, empate ou colocação (1º a 4º). - 40%
- **Turno de Vitória ou Empate (TV)**: Turno em que a partida termina. - 20%
- **Eliminações Realizadas (ER)**: Oponentes eliminados diretamente. - 20%
- **Pontos de Vida Restantes (PV)**: Vida no fim ou na eliminação. - 10%
- **Ações Estratégicas (AE)**: Engajamento (mana, feitiços, dano ou outro a definir). - 10%

**Fórmula do ID**:
```
ID = (0,4 × RP) + (0,2 × TV) + (0,2 × ER) + (0,1 × PV) + (0,1 × AE)
```

### Objetivos
- Escalar para 4 a 100 jogadores.
- Recompensar desempenho em vitórias, empates e derrotas.
- Garantir matchmaking equilibrado.
- Fornecer desempates justos.
- Prevenir colusão em partidas multiplayer.

## Requisitos Funcionais

### 1. Cálculo do Índice de Desempenho (ID)
- **RF1.1**: Calcular o ID por partida com siglas RP, TV, ER, PV, AE, suportando:
  - Vitórias isoladas, empates em 1º, colocações (2º a 4º).
  - Turnos de 1 a 20+.
  - Eliminações de 0 a 3.
  - Pontos de vida de 0 a 30+.
  - Ações estratégicas variadas.
- **RF1.2**: Registrar ID por rodada e calcular média acumulada.
- **RF1.3**: Suportar entrada de dados via aplicativo, planilha ou web, validando turnos, eliminações, PV e AE.
- **RF1.4**: Permitir ajustes manuais por juízes.

#### Definição das Variáveis
| Variável | Sigla | Nome em Português | Peso | Fórmula |
|----------|-------|-------------------|------|---------|
| Resultado da Partida | RP | Resultado final (vitória, empate, colocação) | 40% | Vitória isolada: 100 pontos<br>Empate em 1º: 50 pontos<br>2º: 30 pontos<br>3º: 20 pontos<br>4º: 10 pontos |
| Turno de Vitória ou Empate | TV | Turno em que a partida terminou | 20% | (20 - Turno) / 20 * 100<br>Ex.: Turno 5 → (20-5)/20 * 100 = 75 pontos<br>Máximo 20 turnos (turnos maiores normalizados) |
| Eliminações Realizadas | ER | Oponentes eliminados diretamente | 20% | (Eliminações / 3) * 100<br>Ex.: 2 eliminações → (2/3) * 100 = 66,67 pontos |
| Pontos de Vida Restantes | PV | Percentual de vida no fim ou na eliminação | 10% | (Vida atual / 40) * 100<br>Ex.: 20 PV → (20/40) * 100 = 50 pontos |
| Ações Estratégicas | AE | Mana gasto, feitiços conjurados, dano causado | 10% | Normalizado com base na média da mesa<br>Ex.: Dano médio → 50 pontos |

### 2. Matchmaking
- **RF2.1**: Agrupar por ID médio, com desvio máximo de 10% por mesa, para 4 a 100 jogadores.
- **RF2.2**: Evitar repetição de adversários, priorizando equilíbrio.
- **RF2.3**: Usar algoritmo Swiss adaptado para multiplayer.
- **RF2.4**: Lidar com mesas de 3 jogadores, ajustando cálculos de ID.

### 3. Limite de Tempo
- **RF3.1**: Rodadas de 90 minutos.
- **RF3.2**: Turno adicional se a partida não terminar.
- **RF3.3**: Empate em 1º (RP = 50) para jogadores ativos após turno adicional.

### 4. Critérios de Desempate
- **RF4.1**: Critérios na ordem:
  1. Média de ID acumulada.
  2. Força dos adversários (média de IDs dos oponentes).
  3. Número de vitórias isoladas (RP = 100).
  4. Método aleatório.
- **RF4.2**: Calcular e exibir desempates automaticamente.

### 5. Regras Anti-Colusão
- **RF5.1**: Monitorar:
  - Ausência de ataques sem justificativa.
  - Concentração de eliminações em subgrupos.
  - Baixa pontuação em AE.
  - Turnos prolongados intencionalmente.
- **RF5.2**: Penalidades:
  - Advertência (infrações leves).
  - Redução de 20% no ID (infrações moderadas).
  - Desclassificação (infrações graves/reincidências).
- **RF5.3**: Ferramenta para denúncias anônimas.
- **RF5.4**: Análise estatística de desvios em AE, ER, TV.
- **RF5.5**: Banco de dados de infrações.

## Requisitos Não Funcionais
- **RNF1**: Processar IDs e matchmaking para até 100 jogadores em <15 segundos.
- **RNF2**: Interface intuitiva com nomes em português.
- **RNF3**: Backup automático após cada rodada.
- **RNF4**: Acessível via web/aplicativo, compatível com móveis e desktops.
- **RNF5**: Entrada de dados em tempo real com validação.
- **RNF6**: Escalar para 4 a 100 jogadores sem perda de desempenho.

## Considerações de Cenários
O sistema é projetado para:
- **Tamanhos variados**: 4 a 100 jogadores, com mesas de 4 (ou 3, se necessário).
- **Resultados diversos**: Vitórias isoladas, empates múltiplos, derrotas com PV e eliminações variados.
- **Turnos e PV**: Turnos de 1 a 20+ e PV de 0 a 40+, com normalização para casos extremos.
- **Colusão**: Detecção de manipulações como alianças ou passividade.
- **Desempenho**: Recompensa eficiência (TV), eliminações (ER), resistência (PV) e engajamento (AE).

## Falhas Potenciais e Mitigações
| Falha | Descrição | Mitigação |
|-------|-----------|-----------|
| Dados imprecisos | Erros em turnos, eliminações, PV ou AE | Validação automática e revisão por juízes |
| Colusão não detectada | Manipulação de resultados (ex.: evitar ataques, prolongar turnos) | Análise estatística de AE, ER, TV e denúncias anônimas |
| Matchmaking desbalanceado | IDs muito diferentes na mesma mesa | Limite de 10% de desvio por mesa |
| Sistema lento | Atrasos em grandes torneios | Backend otimizado com caching |
| Escalabilidade limitada | Problemas em torneios pequenos/grandes | Algoritmo adaptável para mesas de 3/4 jogadores |


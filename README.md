
# SPTC-Fortaleza-CE
## Sistema de Pontuação Torneio Commander 

## Descrição

O **Sistema de Gerenciamento de Torneios Commander** é uma solução completa para organizar e gerenciar torneios do formato Commander, um modo popular de jogos de cartas colecionáveis. Ele automatiza processos como cadastro de jogadores, juízes e decks, emparelhamento de mesas, registro de resultados, cálculo de pontuações, detecção de colusões e geração de rankings. Projetado para ser robusto e escalável, o sistema suporta torneios de diferentes tamanhos, garantindo precisão e conformidade com as regras do formato.

Este README fornece uma visão detalhada do sistema, descrevendo suas 15 classes principais, as regras de negócio, fórmulas de pontuação e exemplos práticos, como uma rodada com 6 mesas. Ele é voltado para organizadores de torneios, administradores do sistema e desenvolvedores interessados em entender ou contribuir com o projeto.

## Funcionalidades Principais

- Cadastro seguro de juízes, jogadores e decks, com validações de email e senha.
- Configuração de torneios com número mínimo de jogadores e rodadas automáticas.
- Emparelhamento de jogadores em mesas usando um sistema Swiss simplificado, evitando repetições de oponentes.
- Registro de eliminações, desistências e resultados de partidas, com cálculo do índice de desempenho (ID).
- Detecção de colusões com base em padrões suspeitos e aplicação de penalidades (advertências, reduções de ID ou desclassificações).
- Persistência de dados para salvar e recuperar o estado do torneio.
- Geração de rankings com critérios de desempate e relatórios detalhados.
- Gerenciamento de tempo para rodadas, com suporte a turnos extras.

## Instalação

1. **Pré-requisitos**:
   - Python 3.8 ou superior.
   - Bibliotecas necessárias: `uuid`, `datetime`, `json`, `re`, `pathlib`, `os`, `colorama`.

2. **Configuração**:
   - Clone o repositório do projeto.
   - Instale as dependências: `pip install colorama`.
   - Execute o script principal: `python app-js.py`.

3. **Persistência**:
   - O sistema salva dados automaticamente em `dados_sistema.json` após cada operação.
   - Dados salvos são carregados ao iniciar o sistema, se o arquivo existir.

## Uso

O sistema opera por meio de um menu interativo no terminal, com 14 opções:

1. **Cadastrar Juiz**: Registra um juiz com nome, email e senha.
2. **Cadastrar Torneio**: Cria um torneio com nome e número mínimo de jogadores.
3. **Cadastrar Jogador**: Registra um jogador com nome, email e senha.
4. **Cadastrar Deck**: Associa um deck a um jogador, especificando o comandante.
5. **Inscrever Jogador**: Inscreve um jogador em um torneio com um deck validado.
6. **Finalizar Inscrições**: Encerra as inscrições e define o número de rodadas.
7. **Iniciar Rodada**: Forma mesas e inicia partidas.
8. **Registrar Resultados**: Registra resultados de partidas, calculando o ID.
9. **Gerar Ranking**: Exibe o ranking geral do torneio.
10. **Gerar Relatório**: Produz um relatório detalhado de torneios, jogadores e decks.
11. **Registrar Eliminação/Desistência**: Registra eliminações parciais ou desistências.
12. **Registrar Denúncia**: Reporta suspeitas de colusão.
13. **Aplicar Penalidade**: Aplica penalidades a jogadores, com autenticação de juiz.
14. **Sair**: Salva o estado e encerra o sistema.

### Exemplo de Fluxo
1. Cadastre um juiz (ex.: "Ana", "ana@exemplo.com", senha "Senha123").
2. Crie um torneio (ex.: "Desafio 2025", mínimo de 4 jogadores).
3. Cadastre jogadores (ex.: "Bruno", "bruno@exemplo.com") e seus decks.
4. Inscreva jogadores no torneio.
5. Finalize as inscrições e inicie rodadas.
6. Registre resultados e gere rankings ou relatórios.

## Estrutura do Sistema

O sistema é composto por 15 classes, cada uma com responsabilidades específicas e regras bem definidas. Abaixo, detalhamos cada classe.

### 1. Utilitários

**Propósito**: Fornece ferramentas auxiliares para validações e cálculos comuns.  
**Atributos Principais**: Métodos para validação de emails, índices numéricos e cálculo de médias.  
**Responsabilidades**:  
- Valida emails para garantir unicidade entre jogadores e juízes.  
- Verifica se índices numéricos estão dentro de intervalos válidos (ex.: opções de menu de 1 a 14).  
- Calcula a média do índice de desempenho (ID) de uma lista de jogadores.  
- Fornece mensagens de erro padrão (ex.: "Torneio não existe").  
**Contexto de Uso**: Usada por outras classes para validar entradas (ex.: ao cadastrar um jogador) ou calcular métricas (ex.: média de ID por mesa).  
**Regras**:  
- Emails duplicados são rejeitados.  
- Índices fora do intervalo geram erros.  
- Médias são calculadas apenas para listas não vazias, retornando 0 caso contrário.

### 2. Validador

**Propósito**: Realiza validações específicas para entradas do sistema.  
**Atributos Principais**: Métodos para validar emails, senhas, vida final e turnos.  
**Responsabilidades**:  
- Valida o formato de emails (ex.: deve conter "@" e domínio válido).  
- Verifica a força de senhas (mínimo 8 caracteres, com letras maiúsculas, minúsculas e números).  
- Normaliza a vida final, limitando-a a 40 pontos.  
- Valida turnos com base no turno atual e turnos extras permitidos.  
**Contexto de Uso**: Usada durante cadastros (ex.: email de juiz) e registros de resultados (ex.: vida final).  
**Regras**:  
- Emails inválidos geram erros.  
- Senhas fracas são rejeitadas com mensagens específicas.  
- Vida final é ajustada para o intervalo [0, 40].  
- Turnos excedentes (além do turno atual + turnos extras) são inválidos.

### 3. Juiz

**Propósito**: Representa um juiz que gerencia o torneio e toma decisões críticas.  
**Atributos Principais**: Identificador único, nome, email, senha, permissões (ex.: configurar torneio, aplicar penalidades).  
**Responsabilidades**:  
- Configura torneios, definindo nome e número mínimo de jogadores.  
- Valida resultados de partidas, garantindo conformidade.  
- Aplica penalidades (advertências, reduções de ID, desclassificações).  
- Autentica-se com email e senha para ações sensíveis.  
**Contexto de Uso**: Um juiz é cadastrado antes do torneio e realiza ações como iniciar rodadas ou investigar colusões.  
**Regras**:  
- Emails devem ser únicos e válidos.  
- Senhas devem atender aos critérios de força.  
- A autenticação é obrigatória para penalidades.

### 4. Jogador

**Propósito**: Representa um participante do torneio, com desempenho rastreado.  
**Atributos Principais**: Identificador único, nome, email, senha, decks, histórico de partidas, índice de desempenho (ID), vitórias isoladas, penalidades.  
**Responsabilidades**:  
- Inscreve-se em torneios com um deck validado.  
- Participa de partidas, podendo vencer, empatar, ser eliminado ou desistir.  
- Acumula pontos no ID com base nos resultados.  
- Recebe penalidades por infrações.  
**Contexto de Uso**: Jogadores são cadastrados, inscrevem-se em torneios e competem em mesas.  
**Regras**:  
- Emails e senhas devem ser únicos e válidos.  
- Um jogador só pode usar um deck por torneio.  
- Penalidades afetam o ID ou podem levar à desclassificação.

### 5. Deck

**Propósito**: Representa o conjunto de cartas de um jogador, identificado por um comandante.  
**Atributos Principais**: Identificador único, jogador dono, comandante, status de validação, torneio associado, status ativo/inativo.  
**Responsabilidades**:  
- É cadastrado para um jogador, especificando o comandante.  
- Deve ser validado antes do torneio.  
- Fica associado a um torneio e marcado como inativo até sua conclusão.  
- É liberado para reutilização após o torneio.  
**Contexto de Uso**: Um jogador cadastra um deck, que é validado por um juiz antes da inscrição.  
**Regras**:  
- Um deck só pode ser usado em um torneio por vez.  
- Decks inativos ou associados a outros torneios são inválidos.  
- O comandante não pode ser vazio.

### 6. Torneio

**Propósito**: Representa um evento competitivo com múltiplas rodadas.  
**Atributos Principais**: Identificador único, nome, data, número de rodadas, mínimo de jogadores, listas de jogadores, juízes e mesas, rodada atual, status de inscrições, tempo por rodada, turnos extras.  
**Responsabilidades**:  
- Define as regras do torneio (ex.: mínimo de jogadores, tempo de rodada).  
- Gerencia inscrições até seu encerramento.  
- Organiza rodadas, distribuindo jogadores em mesas.  
- Rastreia o progresso até a conclusão.  
**Contexto de Uso**: Um juiz cria o torneio, jogadores se inscrevem, e o sistema gerencia rodadas até determinar os vencedores.  
**Regras**:  
- Mínimo de 4 jogadores, com distribuição ideal de 4 ou 3 por mesa.  
- Inscrições são encerradas antes das rodadas.  
- O número de rodadas é calculado automaticamente (ex.: 3 para até 8 jogadores, 4 para até 16).  
- Decks são liberados ao finalizar o torneio.

### 7. Partida

**Propósito**: Representa um confronto entre jogadores em uma mesa.  
**Atributos Principais**: Identificador único, lista de jogadores, turno atual, eliminações, resultados, pontuações, tempo de início.  
**Responsabilidades**:  
- Agrupa 3 ou 4 jogadores por mesa.  
- Registra eliminações, desistências e resultados (vitória, empate, derrota).  
- Calcula pontuações com base nos resultados.  
- Monitora o tempo da partida.  
**Contexto de Uso**: Criada automaticamente ao iniciar uma rodada, com resultados registrados ao final.  
**Regras**:  
- Apenas um jogador pode vencer por mesa, ou todos os ativos empatam.  
- Eliminações não podem exceder o número de jogadores menos 2.  
- Turnos registrados devem respeitar o limite (turno atual + turnos extras).  
- Jogadores eliminados recebem derrota.

### 8. Eliminação

**Propósito**: Registra a saída de um jogador de uma partida.  
**Atributos Principais**: Jogador eliminado, jogador causador (se aplicável), turno, indicador de desistência.  
**Responsabilidades**:  
- Documenta quem foi eliminado, quando e por quem (ou se foi desistência).  
- Contribui para o cálculo de pontuações (ex.: eliminações válidas).  
**Contexto de Uso**: Usada quando um jogador perde todos os pontos de vida ou desiste.  
**Regras**:  
- Eliminações causadas por outro jogador contam para o componente ER do ID.  
- Desistências não geram pontos de eliminação.  
- O turno deve ser válido (dentro do limite de turnos extras).

### 9. Inscrição

**Propósito**: Gerencia a associação de um jogador e seu deck a um torneio.  
**Atributos Principais**: Identificador único, torneio, jogador, deck, data de inscrição, status (ativa, cancelada, concluída).  
**Responsabilidades**:  
- Registra a inscrição de um jogador com um deck específico.  
- Permite cancelar a inscrição, liberando o deck.  
- Marca a inscrição como concluída ao finalizar o torneio.  
**Contexto de Uso**: Usada quando um jogador se inscreve em um torneio.  
**Regras**:  
- Um jogador só pode se inscrever uma vez por torneio.  
- O deck deve estar ativo e não associado a outro torneio.  
- Cancelamentos liberam o deck para outros usos.

### 10. Persistência

**Propósito**: Gerencia o armazenamento e recuperação do estado do sistema.  
**Atributos Principais**: Métodos para salvar e carregar dados em JSON.  
**Responsabilidades**:  
- Salva torneios, jogadores, juízes, decks e inscrições em um arquivo.  
- Carrega dados salvos para retomar um torneio.  
**Contexto de Uso**: Usada após cada operação (ex.: registrar resultados) e ao iniciar o sistema.  
**Regras**:  
- Dados são salvos em formato JSON, preservando relações entre entidades.  
- Se o arquivo de dados não existir, o sistema inicia com estado vazio.  
- Erros de carregamento são tratados com mensagens claras.

### 11. Calculador de Índice de Desempenho

**Propósito**: Calcula o índice de desempenho (ID) dos jogadores.  
**Atributos Principais**: Fórmulas para os componentes RP, TV, ER, PV, PA e limites de validação.  
**Responsabilidades**:  
- Calcula o ID como a soma ponderada de cinco componentes.  
- Valida se o ID está dentro dos limites para cada resultado.  
- Aplica ajuste de 0,02% para mesas de 3 jogadores.  
**Contexto de Uso**: Usada ao registrar resultados de partidas.  
**Fórmulas e Regras**:
- **RP (Resultado, peso 60%)**:
  - Vitória: 100 × 0,60 = 60 pontos.
  - Empate: 20 × 0,60 = 12 pontos.
  - Derrota: 10 × 0,60 = 6 pontos.
- **TV (Turno, peso 35%)**:
  - Baseado no turno final:
    - Turno 1: 100 pontos.
    - Turnos 2–10: 100 - (turno - 1) × 0,222.
    - Turnos 11–20: 98 - (turno - 10) × 0,1.
    - Após turno 20: 95,8.
  - Limites:
    - Vitória: Até 100 pontos.
    - Empate: Até 80 pontos.
    - Derrota: Até 35 pontos.
  - Multiplicado por 0,35.
- **ER (Eliminações, peso 2%)**:
  - (eliminações válidas / (jogadores na mesa - 1)) × 100 × 0,02.
  - Vitória sem eliminações: 50 × 0,02 = 1 ponto.
  - Derrota: 0 pontos.
- **PV (Vida Final, peso 2%)**:
  - Vida limitada a 40.
  - Vitória: 100 × 0,02 = 2 pontos.
  - Empate:
    - Vida ≥ 16: 40 × 0,02 = 0,8 ponto.
    - Vida < 16: (vida / 40) × 100 × 0,02.
  - Derrota:
    - Vida ≥ 6: 15 × 0,02 = 0,3 ponto.
    - Vida < 6: (vida / 40) × 100 × 0,02.
- **PA (Oponentes Danificados, peso 1%)**:
  - Vitória:
    - 2+ oponentes: 100 × 0,01 = 1 ponto.
    - 1 oponente: 50 × 0,01 = 0,5 ponto.
  - Empate ou Derrota: 0 pontos.
- **ID Total**:
  - ID = RP + TV + ER + PV + PA.
  - Mesas de 3 jogadores: ID × 0,9998.
- **Limites de Validação**:
  | Jogadores | Resultado | Mínimo | Máximo |
  |-----------|-----------|--------|--------|
  | 4         | Vitória   | 95,53  | 100,0  |
  | 4         | Empate    | 40,0   | 42,13  |
  | 4         | Derrota   | 18,25  | 20,88  |
  | 3         | Vitória   | 95,51  | 99,98  |
  | 3         | Empate    | 39,99  | 42,11  |
  | 3         | Derrota   | 18,25  | 19,22  |

### 12. Sistema Anti-Colusão

**Propósito**: Detecta e gerencia comportamentos suspeitos de conluio.  
**Atributos Principais**: Lista de denúncias e logs de padrões suspeitos.  
**Responsabilidades**:  
- Analisa partidas para identificar:
  - Vitórias sem dano a oponentes (PA = 0).
  - Eliminações concentradas em um jogador.
  - Turnos prolongados (>20) sem eliminações.
- Registra denúncias de colusão.  
- Aplica penalidades (advertência, redução de 20% no ID, desclassificação).  
**Contexto de Uso**: Usada após registrar resultados ou quando um juiz reporta uma suspeita.  
**Regras**:  
- Penalidades requerem autenticação de juiz.  
- Advertência: Sem impacto no ID.  
- Redução: Diminui 20% do ID acumulado.  
- Desclassificação: Remove o jogador e zera o ID.

### 13. Sistema de Emparelhamento

**Propósito**: Organiza jogadores em mesas usando um sistema Swiss simplificado.  
**Atributos Principais**: Histórico de oponentes enfrentados.  
**Responsabilidades**:  
- Distribui jogadores em mesas de 4 ou 3, dependendo do número total.  
- Evita repetições de oponentes entre rodadas.  
- Garante que a média de ID por mesa esteja próxima da média do torneio (desvio ≤ 5%).  
- Usa ordenação por ID nas rodadas subsequentes (aleatória na primeira).  
**Contexto de Uso**: Usada ao iniciar uma rodada para formar mesas.  
**Regras**:  
- Mesas de 3 só são formadas se o número de jogadores não for divisível por 4.  
- Mesas com desvio de ID acima de 5% são redistribuídas.  
- Mínimo de 4 jogadores por torneio.

### 14. Gerenciador de Tempo

**Propósito**: Controla o tempo das partidas.  
**Atributos Principais**: Temporizadores para partidas, com tempo de início, duração e turnos extras.  
**Responsabilidades**:  
- Inicia temporizadores ao começar uma rodada.  
- Verifica se o tempo foi esgotado, considerando turnos extras.  
- Força empate para jogadores ativos se o tempo acabar.  
**Contexto de Uso**: Usada durante rodadas para monitorar partidas.  
**Regras**:  
- Duração padrão: 45 minutos (ajustável).  
- Máximo de 5 turnos extras após o tempo regular.  
- Empate é aplicado após os turnos extras.

### 15. Sistema de Desempate

**Propósito**: Define critérios para ordenar jogadores com IDs iguais.  
**Atributos Principais**: Métodos para calcular a força dos oponentes.  
**Responsabilidades**:  
- Compara jogadores com base em:
  1. Índice de desempenho (ID).
  2. Força média dos oponentes (média de ID dos adversários).
  3. Número de vitórias isoladas.
  4. Sorteio aleatório.  
**Contexto de Uso**: Usada ao gerar rankings.  
**Regras**:  
- Força dos oponentes é calculada com base em todas as partidas.  
- Jogadores sem histórico têm força de oponentes igual a 0.

### 16. Gerenciador de Cadastros

**Propósito**: Gerencia o cadastro de juízes, jogadores e decks.  
**Atributos Principais**: Listas de juízes, jogadores e decks.  
**Responsabilidades**:  
- Cadastra juízes e jogadores, validando emails e senhas.  
- Cadastra e valida decks, associando-os a jogadores e torneios.  
- Busca entidades por email ou nome do deck.  
**Contexto de Uso**: Usada para gerenciar dados de participantes e seus decks.  
**Regras**:  
- Emails devem ser únicos.  
- Decks só podem ser validados se não estiverem associados a outros torneios.  
- Cadastros requerem validação de formato e unicidade.

### 17. Gerenciador de Torneio

**Propósito**: Coordena a criação, execução e finalização de torneios.  
**Atributos Principais**: Lista de torneios, integrações com emparelhamento, tempo e desempate.  
**Responsabilidades**:  
- Configura torneios com nome e mínimo de jogadores.  
- Calcula o número de rodadas com base no número de jogadores.  
- Valida resultados, garantindo consistência (ex.: uma vitória por mesa).  
- Processa pontuações e analisa colusões.  
**Contexto de Uso**: Usada pelo juiz para gerenciar torneios e pelo sistema para processar resultados.  
**Regras**:  
- Rodadas: 3 (≤8 jogadores), 4 (≤16), 5 (≤32), 6 (≤64), 7 (>64).  
- Resultados inválidos (ex.: múltiplas vitórias) são rejeitados.  
- Distribuição de mesas deve ser válida (4 ou 3 jogadores).

### 18. Sistema Torneio Commander

**Propósito**: Interface principal do sistema, coordenando todas as funcionalidades.  
**Atributos Principais**: Gerenciadores de torneios e cadastros, partidas ativas, sistema anti-colusão, mensagens de erro.  
**Responsabilidades**:  
- Exibe um menu interativo com 14 opções.  
- Coordena cadastros, inscrições, rodadas, resultados e relatórios.  
- Gerencia a persistência de dados após cada operação.  
**Contexto de Uso**: Ponto de entrada para usuários (juízes e administradores).  
**Regras**:  
- Operações sensíveis (ex.: penalidades) requerem autenticação.  
- Dados são salvos automaticamente após cada ação.  
- O sistema valida a existência de torneios e partidas antes de ações específicas.

## Regras de Pontuação e Validações

O índice de desempenho (ID) é a métrica principal, composta por cinco componentes (RP, TV, ER, PV, PA), conforme descrito na seção **Calculador de Índice de Desempenho**. As principais validações incluem:

- **Resultados por Mesa**:
  - Apenas um jogador pode vencer.  
  - Empates requerem que todos os jogadores ativos empatem.  
  - Eliminações/desistências implicam derrota.  
- **Eliminações**:
  - Máximo de eliminações: número de jogadores menos 2.  
  - Desistências não contam para ER.  
- **Turnos**:
  - Limitados ao turno atual + 5 turnos extras.  
- **Vida Final**:
  - Limitada a 40 pontos.  
- **Penalidades**:
  - Advertência: Sem impacto no ID.  
  - Redução: 20% do ID acumulado.  
  - Desclassificação: Remove o jogador e zera o ID.  
- **Anti-Colusão**:
  - Padrões suspeitos (ex.: vitória sem PA) são sinalizados.  
  - Denúncias requerem autenticação de juiz.

## Exemplo de Rodada

Abaixo, descrevemos uma rodada do torneio fictício **Desafio dos Comandantes 2025**, com 23 jogadores distribuídos em 6 mesas (5 de 4 jogadores e 1 de 3 jogadores). Os exemplos cobrem vitórias rápidas, empates, eliminações parciais, desistências e penalidades.

### Contexto da Rodada

- **Torneio**: Desafio dos Comandantes 2025.
- **Rodada**: 2ª de 5.
- **Jogadores**: 23 (5 mesas de 4, 1 mesa de 3).
- **Tempo por Rodada**: 45 minutos, com 5 turnos extras.
- **Média de ID**: 50,0 pontos (baseada na rodada anterior).

### Mesa 1 (3 Jogadores, Vitória Rápida por Combo)

**Jogadores**: Ana, Bruno, Clara.  
**Cenário**: Ana usa uma estratégia de combo no turno 1, eliminando Bruno e Clara.  
**Resultados**:
- Ana: Vitória, turno 1, 2 eliminações, vida final 40, 2 oponentes danificados.  
- Bruno: Derrota, turno 1, 0 eliminações, vida final 0, 0 oponentes danificados.  
- Clara: Derrota, turno 1, 0 eliminações, vida final 0, 0 oponentes danificados.  

**Cálculo do ID**:
- **Ana**:
  - RP: 100 × 0,60 = 60,0.
  - TV: 100 × 0,35 = 35,0.
  - ER: (2 / 2) × 100 × 0,02 = 2,0.
  - PV: 100 × 0,02 = 2,0.
  - PA: 100 × 0,01 = 1,0.
  - ID: (60,0 + 35,0 + 2,0 + 2,0 + 1,0) × 0,9998 = 99,98.
- **Bruno** e **Clara**:
  - RP: 10 × 0,60 = 6,0.
  - TV: 35 × 0,35 = 12,25.
  - ER: 0.
  - PV: 0.
  - PA: 0.
  - ID: (6,0 + 12,25 + 0 + 0 + 0) × 0,9998 = 18,25.

**Ranking da Mesa**:
1. Ana: 99,98 pontos (Vitória).
2. Bruno: 18,25 pontos (Derrota).
3. Clara: 18,25 pontos (Derrota).

### Mesa 2 (4 Jogadores, Vitória Rápida por Combo)

**Jogadores**: Diego, Elisa, Fábio, Gabriela.  
**Cenário**: Diego executa um combo no turno 1, eliminando todos os oponentes.  
**Resultados**:
- Diego: Vitória, turno 1, 3 eliminações, vida final 40, 3 oponentes danificados.  
- Elisa, Fábio, Gabriela: Derrota, turno 1, 0 eliminações, vida final 0, 0 oponentes danificados.  

**Cálculo do ID**:
- **Diego**:
  - RP: 60,0.
  - TV: 35,0.
  - ER: (3 / 3) × 100 × 0,02 = 2,0.
  - PV: 2,0.
  - PA: 1,0.
  - ID: 60,0 + 35,0 + 2,0 + 2,0 + 1,0 = 100,0.
- **Elisa, Fábio, Gabriela**:
  - RP: 6,0.
  - TV: 12,25.
  - ER: 0.
  - PV: 0.
  - PA: 0.
  - ID: 6,0 + 12,25 + 0 + 0 + 0 = 18,25.

**Ranking da Mesa**:
1. Diego: 100,0 pontos (Vitória).
2. Elisa, Fábio, Gabriela: 18,25 pontos (Derrota).

### Mesa 3 (4 Jogadores, Empate com Eliminação Parcial)

**Jogadores**: Hugo, Inês, João, Karen.  
**Cenário**: João é eliminado por Hugo no turno 5. O tempo esgota, forçando empate entre Hugo, Inês e Karen.  
**Resultados**:
- Hugo: Empate, turno 10, 1 eliminação, vida final 20, 2 oponentes danificados.  
- Inês: Empate, turno 10, 0 eliminações, vida final 16, 1 oponente danificado.  
- Karen: Empate, turno 10, 0 eliminações, vida final 12, 1 oponente danificado.  
- João: Derrota, turno 5, 0 eliminações, vida final 0, 0 oponentes danificados.  

**Cálculo do ID**:
- **Hugo**:
  - RP: 20 × 0,60 = 12,0.
  - TV: [100 - (10 - 1) × 0,222] = 80,002 × 0,35 = 28,0.
  - ER: (1 / 3) × 100 × 0,02 = 0,67.
  - PV: 40 × 0,02 = 0,8.
  - PA: 0.
  - ID: 12,0 + 28,0 + 0,67 + 0,8 + 0 = 41,47.
- **Inês**:
  - RP: 12,0.
  - TV: 28,0.
  - ER: 0.
  - PV: 40 × 0,02 = 0,8.
  - PA: 0.
  - ID: 12,0 + 28,0 + 0 + 0,8 + 0 = 40,8.
- **Karen**:
  - RP: 12,0.
  - TV: 28,0.
  - ER: 0.
  - PV: (12 / 40) × 100 × 0,02 = 0,6.
  - PA: 0.
  - ID: 12,0 + 28,0 + 0 + 0,6 + 0 = 40,6.
- **João**:
  - RP: 6,0.
  - TV: [100 - (5 - 1) × 0,222] = 99,112 × 0,35 = 12,25.
  - ER: 0.
  - PV: 0.
  - PA: 0.
  - ID: 6,0 + 12,25 + 0 + 0 + 0 = 18,25.

**Ranking da Mesa**:
1. Hugo: 41,47 pontos (Empate).
2. Inês: 40,8 pontos (Empate).
3. Karen: 40,6 pontos (Empate).
4. João: 18,25 pontos (Derrota).

### Mesa 4 (4 Jogadores, Vitória com Penalidade)

**Jogadores**: Lucas, Marina, Nina, Otávio.  
**Cenário**: Lucas vence no turno 8, eliminando Marina e Nina. Otávio desiste no turno 6. O juiz aplica uma advertência a Lucas por vitória sem dano a oponentes.  
**Resultados**:
- Lucas: Vitória, turno 8, 2 eliminações, vida final 30, 0 oponentes danificados (advertência).  
- Marina, Nina: Derrota, turno 8, 0 eliminações, vida final 0, 0 oponentes danificados.  
- Otávio: Derrota, turno 6, 0 eliminações, vida final 10, 0 oponentes danificados (desistência).  

**Cálculo do ID**:
- **Lucas**:
  - RP: 60,0.
  - TV: [100 - (8 - 1) × 0,222] = 84,446 × 0,35 = 29,56.
  - ER: (2 / 3) × 100 × 0,02 = 1,33.
  - PV: 2,0.
  - PA: 0 (sinalizado como suspeito).
  - ID: 60,0 + 29,56 + 1,33 + 2,0 + 0 = 92,89.
- **Marina, Nina**:
  - RP: 6,0.
  - TV: 12,25.
  - ER: 0.
  - PV: 0.
  - PA: 0.
  - ID: 6,0 + 12,25 + 0 + 0 + 0 = 18,25.
- **Otávio**:
  - RP: 6,0.
  - TV: [100 - (6 - 1) × 0,222] = 98,89 × 0,35 = 12,25.
  - ER: 0.
  - PV: 15 × 0,02 = 0,3.
  - PA: 0.
  - ID: 6,0 + 12,25 + 0 + 0,3 + 0 = 18,55.

**Ranking da Mesa**:
1. Lucas: 92,89 pontos (Vitória, advertência).
2. Otávio: 18,55 pontos (Derrota).
3. Marina, Nina: 18,25 pontos (Derrota).

### Mesa 5 (4 Jogadores, Empate Completo)

**Jogadores**: Pedro, Quitéria, Rafael, Sofia.  
**Cenário**: Nenhum jogador é eliminado, e o tempo esgota, forçando empate.  
**Resultados**:
- Pedro: Empate, turno 12, 0 eliminações, vida final 18, 2 oponentes danificados.  
- Quitéria: Empate, turno 12, 0 eliminações, vida final 16, 1 oponente danificado.  
- Rafael: Empate, turno 12, 0 eliminações, vida final 10, 1 oponente danificado.  
- Sofia: Empate, turno 12, 0 eliminações, vida final 8, 0 oponentes danificados.  

**Cálculo do ID**:
- **Pedro, Quitéria**:
  - RP: 12,0.
  - TV: [98 - (12 - 10) × 0,1] = 97,8 × 0,35 = 28,0.
  - ER: 0.
  - PV: 40 × 0,02 = 0,8.
  - PA: 0.
  - ID: 12,0 + 28,0 + 0 + 0,8 + 0 = 40,8.
- **Rafael**:
  - RP: 12,0.
  - TV: 28,0.
  - ER: 0.
  - PV: (10 / 40) × 100 × 0,02 = 0,5.
  - PA: 0.
  - ID: 12,0 + 28,0 + 0 + 0,5 + 0 = 40,5.
- **Sofia**:
  - RP: 12,0.
  - TV: 28,0.
  - ER: 0.
  - PV: (8 / 40) × 100 × 0,02 = 0,4.
  - PA: 0.
  - ID: 12,0 + 28,0 + 0 + 0,4 + 0 = 40,4.

**Ranking da Mesa**:
1. Pedro, Quitéria: 40,8 pontos (Empate).
2. Rafael: 40,5 pontos (Empate).
3. Sofia: 40,4 pontos (Empate).

### Mesa 6 (4 Jogadores, Vitória com Eliminações Parciais)

**Jogadores**: Tiago, Úrsula, Victor, Wanda.  
**Cenário**: Úrsula elimina Victor no turno 4. Wanda desiste no turno 6. Tiago vence no turno 10, eliminando Úrsula.  
**Resultados**:
- Tiago: Vitória, turno 10, 1 eliminação, vida final 25, 2 oponentes danificados.  
- Úrsula: Derrota, turno 10, 1 eliminação, vida final 0, 1 oponente danificado.  
- Victor: Derrota, turno 4, 0 eliminações, vida final 0, 0 oponentes danificados.  
- Wanda: Derrota, turno 6, 0 eliminações, vida final 15, 0 oponentes danificados (desistência).  

**Cálculo do ID**:
- **Tiago**:
  - RP: 60,0.
  - TV: [100 - (10 - 1) × 0,222] = 80,002 × 0,35 = 28,0.
  - ER: (1 / 3) × 100 × 0,02 = 0,67.
  - PV: 2,0.
  - PA: 1,0.
  - ID: 60,0 + 28,0 + 0,67 + 2,0 + 1,0 = 91,67.
- **Úrsula**:
  - RP: 6,0.
  - TV: 12,25.
  - ER: (1 / 3) × 100 × 0,02 = 0,67.
  - PV: 0.
  - PA: 0.
  - ID: 6,0 + 12,25 + 0,67 + 0 + 0 = 18,92.
- **Victor**:
  - RP: 6,0.
  - TV: [100 - (4 - 1) × 0,222] = 99,334 × 0,35 = 12,25.
  - ER: 0.
  - PV: 0.
  - PA: 0.
  - ID: 6,0 + 12,25 + 0 + 0 + 0 = 18,25.
- **Wanda**:
  - RP: 6,0.
  - TV: [100 - (6 - 1) × 0,222] = 98,89 × 0,35 = 12,25.
  - ER: 0.
  - PV: 15 × 0,02 = 0,3.
  - PA: 0.
  - ID: 6,0 + 12,25 + 0 + 0,3 + 0 = 18,55.

**Ranking da Mesa**:
1. Tiago: 91,67 pontos (Vitória).
2. Úrsula: 18,92 pontos (Derrota).
3. Wanda: 18,55 pontos (Derrota).
4. Victor: 18,25 pontos (Derrota).

### Ranking Geral Após a Rodada

Assumindo IDs acumulados da rodada anterior, o ranking geral considera o ID total, força dos oponentes e vitórias isoladas:

| Posição | Jogador   | ID Total | Vitórias Isoladas | Força dos Oponentes |
|---------|-----------|----------|-------------------|---------------------|
| 1       | Diego     | 150,0    | 2                 | 60,0                |
| 2       | Ana       | 149,98   | 2                 | 55,0                |
| 3       | Tiago     | 141,67   | 2                 | 50,0                |
| 4       | Hugo      | 91,47    | 1                 | 45,0                |
| ...     | ...       | ...      | ...               | ...                 |
| 20      | João      | 68,25    | 0                 | 40,0                |
| 21      | Victor    | 68,25    | 0                 | 35,0                |

**Desempate**:
- Diego supera Ana devido ao ID maior (150,0 vs. 149,98).  
- João supera Victor pelo maior valor de força dos oponentes (40,0 vs. 35,0).

## Contribuindo

Contribuições são bem-vindas! Para sugerir melhorias ou reportar problemas, abra uma issue no repositório. Siga as diretrizes no arquivo `CONTRIBUTING.md`.

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Set
import random
import math
import json
import re
from pathlib import Path
import os
from colorama import init, Fore, Style

# Inicializa colorama para formatação de cores no terminal
init()

class Utilitarios:
    """Classe responsável por funções utilitárias do sistema"""
    
    @staticmethod
    def calcular_media_ids(jogadores: List['Jogador']) -> float:
        """Calcula a média dos índices de desempenho de uma lista de jogadores"""
        if not jogadores:
            return 0.0
        return sum(j.indice_desempenho for j in jogadores) / len(jogadores)

    @staticmethod
    def validar_email_unico(email: str, entidades: List) -> bool:
        """Verifica se um email é único na lista de entidades"""
        return not any(e.email == email for e in entidades)

    @staticmethod
    def validar_indice_numerico(valor: str, minimo: int, maximo: int) -> int:
        """Valida se um valor está dentro de um intervalo numérico"""
        if not valor.isdigit() or int(valor) < minimo or int(valor) > maximo:
            raise ValueError(f"Índice inválido. Deve ser entre {minimo} e {maximo}.")
        return int(valor)

    @staticmethod
    def mensagens_erro():
        """Retorna um dicionário com mensagens de erro padrão"""
        return {
            "torneio_nao_existe": "Nenhum torneio criado. Crie um torneio primeiro (opção 2).",
            "jogador_nao_encontrado": "Jogador não encontrado.",
            "email_ja_cadastrado": "Email já cadastrado.",
            "indice_invalido": "Índice inválido.",
            "sem_partidas_ativas": "Nenhuma partida ativa. Inicie uma rodada primeiro (opção 7)."
        }

class Persistencia:
    """Classe responsável pela persistência de dados do sistema"""
    
    @staticmethod
    def salvar_estado(sistema: 'SistemaTorneioCommander', caminho: str = 'dados_sistema.json'):
        """Salva o estado atual do sistema em um arquivo JSON"""
        dados = {
            "torneios": [Persistencia._serializar_torneio(t) for t in sistema.gerenciador_torneio.torneios],
            "jogadores": [Persistencia._serializar_jogador(j) for j in sistema.gerenciador_cadastros.jogadores],
            "juizes": [Persistencia._serializar_juiz(j) for j in sistema.gerenciador_cadastros.juizes],
            "decks": [Persistencia._serializar_deck(d) for d in sistema.gerenciador_cadastros.decks]
        }
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(Fore.GREEN + f"Estado do sistema salvo em {caminho}" + Style.RESET_ALL)

    @staticmethod
    def carregar_estado(sistema: 'SistemaTorneioCommander', caminho: str = 'dados_sistema.json') -> bool:
        """Carrega o estado do sistema a partir de um arquivo JSON"""
        try:
            if not os.path.exists(caminho):
                return False
            
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Primeiro carrega juízes e jogadores
            sistema.gerenciador_cadastros.juizes = [
                Persistencia._deserializar_juiz(j) for j in dados.get("juizes", [])
            ]
            sistema.gerenciador_cadastros.jogadores = [
                Persistencia._deserializar_jogador(j) for j in dados.get("jogadores", [])
            ]
            
            # Depois carrega decks (que dependem de jogadores)
            sistema.gerenciador_cadastros.decks = [
                Persistencia._deserializar_deck(d, sistema.gerenciador_cadastros.jogadores) 
                for d in dados.get("decks", [])
            ]
            
            # Por fim carrega torneios (que dependem de tudo)
            sistema.gerenciador_torneio.torneios = [
                Persistencia._deserializar_torneio(
                    t, 
                    sistema.gerenciador_cadastros.jogadores,
                    sistema.gerenciador_cadastros.juizes
                ) for t in dados.get("torneios", [])
            ]
            
            print(Fore.GREEN + f"Estado do sistema carregado de {caminho}" + Style.RESET_ALL)
            return True
        except Exception as e:
            print(Fore.RED + f"Erro ao carregar estado: {e}" + Style.RESET_ALL)
            return False

    @staticmethod
    def _serializar_torneio(torneio: 'Torneio') -> dict:
        return {
            "id": torneio.id,
            "nome": torneio.nome,
            "data": torneio.data.isoformat(),
            "rodadas": torneio.rodadas,
            "min_jogadores": torneio.min_jogadores,
            "jogadores": [j.id for j in torneio.jogadores],
            "juizes": [j.id for j in torneio.juizes],
            "rodada_atual": torneio.rodada_atual,
            "inscricoes_abertas": torneio.inscricoes_abertas,
            "tempo_rodada": str(torneio.tempo_rodada),
            "turnos_extras": torneio.turnos_extras
        }

    @staticmethod
    def _serializar_jogador(jogador: 'Jogador') -> dict:
        return {
            "id": jogador.id,
            "nome": jogador.nome,
            "email": jogador.email,
            "indice_desempenho": jogador.indice_desempenho,
            "vitorias_isoladas": jogador.vitorias_isoladas,
            "senha_hash": jogador.senha_hash if hasattr(jogador, 'senha_hash') else None
        }

    @staticmethod
    def _serializar_juiz(juiz: 'Juiz') -> dict:
        return {
            "id": juiz.id,
            "nome": juiz.nome,
            "email": juiz.email,
            "permissoes": juiz.permissoes,
            "senha_hash": juiz.senha_hash if hasattr(juiz, 'senha_hash') else None
        }

    @staticmethod
    def _serializar_deck(deck: 'Deck') -> dict:
        return {
            "id": deck.id,
            "jogador_id": deck.jogador.id,
            "comandante": deck.comandante,
            "validado": deck.validado,
            "torneio_id": deck.torneio.id if deck.torneio else None,
            "ativo": deck.ativo if hasattr(deck, 'ativo') else True
        }

    @staticmethod
    def _deserializar_torneio(dados: dict, jogadores: List['Jogador'], juizes: List['Juiz']) -> 'Torneio':
        torneio = Torneio(dados["nome"], dados["min_jogadores"])
        torneio.id = dados["id"]
        torneio.data = datetime.fromisoformat(dados["data"])
        torneio.rodadas = dados["rodadas"]
        torneio.jogadores = [j for j in jogadores if j.id in dados["jogadores"]]
        torneio.juizes = [j for j in juizes if j.id in dados["juizes"]]
        torneio.rodada_atual = dados["rodada_atual"]
        torneio.inscricoes_abertas = dados["inscricoes_abertas"]
        torneio.tempo_rodada = datetime.strptime(dados["tempo_rodada"], "%H:%M:%S").time()
        torneio.turnos_extras = dados["turnos_extras"]
        return torneio

    @staticmethod
    def _deserializar_jogador(dados: dict) -> 'Jogador':
        jogador = Jogador(dados["nome"], dados["email"])
        jogador.id = dados["id"]
        jogador.indice_desempenho = dados["indice_desempenho"]
        jogador.vitorias_isoladas = dados["vitorias_isoladas"]
        if dados.get("senha_hash"):
            jogador.senha_hash = dados["senha_hash"]
        return jogador

    @staticmethod
    def _deserializar_juiz(dados: dict) -> 'Juiz':
        juiz = Juiz(dados["nome"], dados["email"])
        juiz.id = dados["id"]
        juiz.permissoes = dados["permissoes"]
        if dados.get("senha_hash"):
            juiz.senha_hash = dados["senha_hash"]
        return juiz

    @staticmethod
    def _deserializar_deck(dados: dict, jogadores: List['Jogador']) -> 'Deck':
        jogador = next(j for j in jogadores if j.id == dados["jogador_id"])
        deck = Deck(jogador, dados["comandante"])
        deck.id = dados["id"]
        deck.validado = dados["validado"]
        deck.ativo = dados.get("ativo", True)
        return deck

class Validador:
    """Classe responsável por validações do sistema"""
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida o formato de um email"""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, email))

    @staticmethod
    def validar_senha(senha: str) -> Tuple[bool, str]:
        """Valida a força de uma senha"""
        if len(senha) < 8:
            return False, "Senha deve ter pelo menos 8 caracteres"
        if not re.search(r'[A-Z]', senha):
            return False, "Senha deve ter pelo menos uma letra maiúscula"
        if not re.search(r'[a-z]', senha):
            return False, "Senha deve ter pelo menos uma letra minúscula"
        if not re.search(r'\d', senha):
            return False, "Senha deve ter pelo menos um número"
        return True, "Senha válida"

    @staticmethod
    def validar_vida_final(vida: int) -> int:
        """Valida e normaliza o valor de vida final"""
        return min(max(0, vida), 40)

    @staticmethod
    def validar_turno(turno: int, partida: 'Partida', torneio: 'Torneio') -> bool:
        """Valida se o turno está dentro dos limites permitidos"""
        max_turno = partida.turno_atual + torneio.turnos_extras
        return 1 <= turno <= max_turno

class Juiz:
    def __init__(self, nome: str, email: str):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.email = email
        self.permissoes = ["configurar_torneio", "validar_resultados", "aplicar_penalidades"]
        self.senha_hash = None

    def definir_senha(self, senha: str):
        """Define a senha do juiz após validação"""
        valido, mensagem = Validador.validar_senha(senha)
        if not valido:
            raise ValueError(mensagem)
        self.senha_hash = senha  # Em uma implementação real, usar hash seguro

class Jogador:
    def __init__(self, nome: str, email: str):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.email = email
        self.decks: List['Deck'] = []
        self.historico_partidas: List['Partida'] = []
        self.indice_desempenho: float = 0.0
        self.vitorias_isoladas: int = 0
        self.penalidades: List[Dict] = []
        self.senha_hash = None

    def definir_senha(self, senha: str):
        """Define a senha do jogador após validação"""
        valido, mensagem = Validador.validar_senha(senha)
        if not valido:
            raise ValueError(mensagem)
        self.senha_hash = senha  # Em uma implementação real, usar hash seguro

class Deck:
    def __init__(self, jogador: 'Jogador', comandante: str):
        self.id = str(uuid.uuid4())
        self.jogador = jogador
        self.comandante = comandante
        self.validado = False
        self.torneio: Optional['Torneio'] = None
        self.ativo = True

    def desativar(self):
        """Desativa o deck após o término do torneio"""
        self.ativo = False
        self.torneio = None

class Torneio:
    def __init__(self, nome: str, min_jogadores: int):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.data = datetime.now()
        self.rodadas = 0
        self.min_jogadores = min_jogadores
        self.jogadores: List[Jogador] = []
        self.juizes: List[Juiz] = []
        self.mesas: List[List[Jogador]] = []
        self.rodada_atual = 0
        self.inscricoes_abertas = True
        self.tempo_rodada = timedelta(minutes=45)
        self.turnos_extras = 5

    def finalizar(self):
        """Finaliza o torneio e libera os decks"""
        for jogador in self.jogadores:
            for deck in jogador.decks:
                if deck.torneio == self:
                    deck.desativar()

class Partida:
    def __init__(self, jogadores: List[Jogador], turno_inicial: int = 1):
        self.id = str(uuid.uuid4())
        self.jogadores = jogadores
        self.turno_atual = turno_inicial
        self.eliminacoes: List['Eliminacao'] = []
        self.resultado: Optional[str] = None
        self.pontuacoes: Dict[str, float] = {}
        self.tempo_inicio = datetime.now()

    def validar_turno(self, turno: int, torneio: 'Torneio') -> bool:
        """Valida se o turno está dentro dos limites permitidos"""
        return Validador.validar_turno(turno, self, torneio)

    def jogador_eliminado(self, jogador: 'Jogador') -> bool:
        """Verifica se um jogador foi eliminado"""
        return any(e.jogador_eliminado == jogador for e in self.eliminacoes)

class Eliminacao:
    def __init__(self, jogador_eliminado: Jogador, jogador_causador: Optional[Jogador], turno: int, desistiu: bool = False):
        self.jogador_eliminado = jogador_eliminado
        self.jogador_causador = jogador_causador
        self.turno = turno
        self.desistiu = desistiu

class Inscricao:
    """Classe que representa a inscrição de um jogador em um torneio com seu deck"""
    
    def __init__(self, torneio: 'Torneio', jogador: 'Jogador', deck: 'Deck'):
        self.id = str(uuid.uuid4())
        self.torneio = torneio
        self.jogador = jogador
        self.deck = deck
        self.data_inscricao = datetime.now()
        self.status = "ATIVA"  # ATIVA, CANCELADA, CONCLUIDA
        
    def cancelar(self):
        """Cancela a inscrição e libera o deck para outros torneios"""
        self.status = "CANCELADA"
        self.deck.torneio = None
        if self.jogador in self.torneio.jogadores:
            self.torneio.jogadores.remove(self.jogador)
            
    def concluir(self):
        """Marca a inscrição como concluída após o término do torneio"""
        self.status = "CONCLUIDA"
        self.deck.desativar()

class SistemaAntiColusao:
    def __init__(self):
        self.denuncias = []
        self.logs_suspeitos = []

    def analisar_padroes(self, partida: Partida, resultados: Dict[str, dict]) -> List[str]:
        suspeitas = []
        for jogador_id, dados in resultados.items():
            jogador = next(j for j in partida.jogadores if j.id == jogador_id)
            if self._verificar_vitoria_sem_pa(dados):
                suspeitas.append(f"{jogador.nome}: Vitória sem dano a oponentes (PA = 0).")
            if self._verificar_eliminacoes_concentradas(partida, jogador_id, dados):
                suspeitas.append(f"{jogador.nome}: Eliminações concentradas em um único causador.")
            if self._verificar_turnos_prolongados(dados):
                suspeitas.append(f"{jogador.nome}: Turno prolongado (>{dados['turno']}) sem eliminações.")
        self.logs_suspeitos.extend(suspeitas)
        return suspeitas

    def _verificar_vitoria_sem_pa(self, dados: dict) -> bool:
        return dados["resultado"] == "VITORIA" and dados["oponentes_danificados"] == 0

    def _verificar_eliminacoes_concentradas(self, partida: Partida, jogador_id: str, dados: dict) -> bool:
        if dados["eliminacoes"] == 0:
            return False
        causadores = [e.jogador_causador.id for e in partida.eliminacoes if e.jogador_causador and e.jogador_causador.id == jogador_id]
        return len(set(causadores)) == 1

    def _verificar_turnos_prolongados(self, dados: dict) -> bool:
        return dados["turno"] > 20 and dados["eliminacoes"] == 0

    def registrar_denuncia(self, jogador: Jogador, descricao: str):
        self.denuncias.append({"jogador": jogador.nome, "descricao": descricao, "data": datetime.now()})
        print(f"Denúncia registrada contra {jogador.nome}: {descricao}")

    def aplicar_penalidade(self, jogador: Jogador, tipo: str, torneio: Torneio) -> float:
        penalidade = {"jogador": jogador.nome, "tipo": tipo, "torneio": torneio.nome, "data": datetime.now()}
        jogador.penalidades.append(penalidade)
        if tipo == "ADVERTENCIA":
            print(f"Advertência aplicada a {jogador.nome}.")
            return 0
        elif tipo == "REDUCAO_ID":
            reducao = jogador.indice_desempenho * 0.2
            jogador.indice_desempenho -= reducao
            print(f"Redução de 20% no ID aplicada a {jogador.nome} (-{reducao:.2f} pontos).")
            return reducao
        elif tipo == "DESCLASSIFICACAO":
            torneio.jogadores.remove(jogador)
            jogador.indice_desempenho = 0
            print(f"{jogador.nome} desclassificado do torneio {torneio.nome}.")
            return jogador.indice_desempenho
        return 0

class SistemaEmparelhamento:
    def __init__(self):
        self.historico_oponentes = {}

    def validar_desvio(self, mesa: List[Jogador], media_torneio: float) -> bool:
        media_mesa = Utilitarios.calcular_media_ids(mesa)
        desvio = abs(media_mesa - media_torneio) / media_torneio if media_torneio > 0 else 0
        return desvio <= 0.05

    def evitar_repeticao(self, jogador: Jogador, mesa: List[Jogador]) -> bool:
        oponentes_anteriores = self.historico_oponentes.get(jogador.id, set())
        return not any(op.id in oponentes_anteriores for op in mesa)

    def distribuir_jogadores(self, torneio: Torneio) -> List[List[Jogador]]:
        num_jogadores = len(torneio.jogadores)
        if num_jogadores < 4:
            raise ValueError(f"Número de jogadores insuficiente ({num_jogadores}). Mínimo de 4 necessário.")
        
        valido, mensagem = GerenciadorTorneio.validar_distribuicao_mesas(num_jogadores)
        if not valido:
            raise ValueError(mensagem)
        
        jogadores = torneio.jogadores.copy()
        media_torneio = Utilitarios.calcular_media_ids(jogadores)
        if torneio.rodada_atual == 0:
            random.shuffle(jogadores)
        else:
            jogadores.sort(key=lambda x: x.indice_desempenho, reverse=True)
        
        mesas = []
        while jogadores:
            mesa_size = 4 if len(jogadores) >= 4 else 3
            mesa = self._formar_mesa(jogadores, mesa_size)
            if self.validar_desvio(mesa, media_torneio):
                mesas.append(mesa)
                for j in mesa:
                    self.historico_oponentes.setdefault(j.id, set()).update(op.id for op in mesa if op != j)
            else:
                jogadores.extend(mesa)
                random.shuffle(jogadores)
        
        if not mesas:
            raise ValueError("Não foi possível formar mesas válidas.")
        return mesas

    def _formar_mesa(self, jogadores: List[Jogador], mesa_size: int) -> List[Jogador]:
        mesa = []
        for jogador in jogadores[:]:
            if len(mesa) < mesa_size and self.evitar_repeticao(jogador, mesa):
                mesa.append(jogador)
                jogadores.remove(jogador)
        return mesa

class CalculadorIndiceDesempenho:
    """Classe responsável por calcular o índice de desempenho dos jogadores"""
    
    LIMITES_PONTUACAO = {
        4: {
            "VITORIA": (95.53, 100.0),
            "EMPATE": (40.0, 42.13),
            "DERROTA": (18.25, 20.88)
        },
        3: {
            "VITORIA": (95.51, 99.98),
            "EMPATE": (39.99, 42.11),
            "DERROTA": (18.25, 19.22)
        }
    }

    @staticmethod
    def calcular_rp(resultado: str) -> float:
        if resultado == "VITORIA":
            return 100 * 0.60
        elif resultado == "EMPATE":
            return 20 * 0.60
        else:  # DERROTA
            return 10 * 0.60

    @staticmethod
    def calcular_tv(resultado: str, turno: int) -> float:
        if resultado == "VITORIA":
            tv = CalculadorIndiceDesempenho._calcular_tv_base(turno)
        elif resultado == "EMPATE":
            tv = min(CalculadorIndiceDesempenho._calcular_tv_base(turno), 80)
        else:  # DERROTA
            tv = min(CalculadorIndiceDesempenho._calcular_tv_base(turno), 35)
        return tv * 0.35

    @staticmethod
    def _calcular_tv_base(turno: int) -> float:
        if turno == 1:
            return 100
        elif 2 <= turno <= 10:
            return 100 - ((turno - 1) * 0.222)
        elif 11 <= turno <= 20:
            return 98 - ((turno - 10) * 0.1)
        else:
            return 95.8

    @staticmethod
    def calcular_er(resultado: str, eliminacoes_validas: int, jogadores_mesa: int) -> float:
        if resultado == "DERROTA":
            return 0
        if eliminacoes_validas == 0 and resultado == "VITORIA":
            return 50
        return (eliminacoes_validas / (jogadores_mesa - 1)) * 100 * 0.02

    @staticmethod
    def calcular_pv(resultado: str, vida_final: int) -> float:
        # Limitando vida_final a 40
        vida_final = min(int(vida_final), 40)
        
        if resultado == "VITORIA":
            return 100 * 0.02
        elif resultado == "EMPATE":
            if vida_final >= 16:
                return 40 * 0.02
            return (vida_final / 40) * 100 * 0.02
        else:  # DERROTA
            if vida_final >= 6:
                return 15 * 0.02
            return (vida_final / 40) * 100 * 0.02

    @staticmethod
    def calcular_pa(resultado: str, oponentes_danificados: int) -> float:
        if resultado == "VITORIA":
            if oponentes_danificados >= 2:
                return 100 * 0.01
            elif oponentes_danificados == 1:
                return 50 * 0.01
        return 0

    @staticmethod
    def calcular_id(rp: float, tv: float, er: float, pv: float, pa: float, mesa_tres: bool) -> float:
        id_total = rp + tv + er + pv + pa
        if mesa_tres:
            id_total *= 0.9998
        return id_total

    @staticmethod
    def validar_pontuacao(id_calculado: float, resultado: str, jogadores_mesa: int) -> bool:
        min_lim, max_lim = CalculadorIndiceDesempenho.LIMITES_PONTUACAO[jogadores_mesa][resultado]
        return min_lim <= id_calculado <= max_lim

class GerenciadorTempo:
    def __init__(self):
        self.temporizadores = {}

    def iniciar_temporizador(self, partida: Partida, duracao: timedelta):
        self.temporizadores[partida.id] = {"inicio": datetime.now(), "duracao": duracao, "turnos_extras": 0}

    def verificar_tempo(self, partida: Partida, torneio: Torneio) -> bool:
        if partida.id not in self.temporizadores:
            return False
        tempo = self.temporizadores[partida.id]
        elapsed = datetime.now() - tempo["inicio"]
        if elapsed >= tempo["duracao"] and tempo["turnos_extras"] < torneio.turnos_extras:
            tempo["turnos_extras"] += 1
            return False
        elif elapsed >= tempo["duracao"] and tempo["turnos_extras"] >= torneio.turnos_extras:
            return True
        return False

class SistemaDesempate:
    @staticmethod
    def calcular_forca_oponentes(jogador: Jogador, partidas: List[Partida]) -> float:
        oponentes_ids = set()
        for partida in jogador.historico_partidas:
            oponentes_ids.update(op.id for op in partida.jogadores if op != jogador)
        if not oponentes_ids:
            return 0.0
        oponentes = [op for p in partidas for op in p.jogadores if op.id in oponentes_ids]
        return Utilitarios.calcular_media_ids(oponentes) if oponentes else 0.0

    @staticmethod
    def comparar_jogadores(j1: Jogador, j2: Jogador, partidas: List[Partida]) -> int:
        if j1.indice_desempenho != j2.indice_desempenho:
            return -1 if j1.indice_desempenho > j2.indice_desempenho else 1
        forca_j1 = SistemaDesempate.calcular_forca_oponentes(j1, partidas)
        forca_j2 = SistemaDesempate.calcular_forca_oponentes(j2, partidas)
        if forca_j1 != forca_j2:
            return -1 if forca_j1 > forca_j2 else 1
        if j1.vitorias_isoladas != j2.vitorias_isoladas:
            return -1 if j1.vitorias_isoladas > j2.vitorias_isoladas else 1
        return random.choice([-1, 1])

class GerenciadorCadastros:
    """Classe responsável por gerenciar os cadastros de juízes, jogadores e decks"""
    
    def __init__(self):
        self.juizes = []
        self.jogadores = []
        self.decks = []
    
    def cadastrar_juiz(self, nome: str, email: str) -> bool:
        """Cadastra um novo juiz"""
        # Valida email único
        if any(j.email == email for j in self.juizes):
            return False
            
        juiz = Juiz(nome, email)
        self.juizes.append(juiz)
        return True
        
    def cadastrar_jogador(self, nome: str, email: str) -> bool:
        """Cadastra um novo jogador"""
        # Valida email único
        if any(j.email == email for j in self.jogadores):
            return False
            
        jogador = Jogador(nome, email)
        self.jogadores.append(jogador)
        return True
        
    def cadastrar_deck(self, jogador: Jogador, comandante: str) -> Deck:
        """Cadastra um novo deck para um jogador"""
        deck = Deck(jogador, comandante)
        jogador.decks.append(deck)
        self.decks.append(deck)
        return deck
        
    def validar_deck(self, deck: Deck, torneio: Torneio) -> bool:
        """Valida se um deck pode ser usado em um torneio"""
        if not deck.comandante or deck.torneio is not None:
            return False
        deck.validado = True
        deck.torneio = torneio
        return True
        
    def buscar_juiz(self, email: str) -> Juiz:
        """Busca um juiz pelo email"""
        return next((j for j in self.juizes if j.email == email), None)
        
    def buscar_jogador(self, email: str) -> Jogador:
        """Busca um jogador pelo email"""
        return next((j for j in self.jogadores if j.email == email), None)
        
    def buscar_deck(self, email_jogador: str, nome_deck: str) -> Deck:
        """Busca um deck pelo nome e email do jogador"""
        return next(
            (
                d for d in self.decks
                if d.jogador.email == email_jogador and d.nome == nome_deck
            ),
            None
        )

class GerenciadorTorneio:
    """Classe responsável por gerenciar os torneios"""
    
    def __init__(self):
        self.torneios = []
        self.inscricoes = []
        self.partidas = []
        self.emparelhamento = SistemaEmparelhamento()
        self.tempo = GerenciadorTempo()
        self.desempate = SistemaDesempate()

    def configurar_torneio(self, nome: str, min_jogadores: int) -> Torneio:
        torneio = Torneio(nome, min_jogadores)
        self.torneios.append(torneio)
        return torneio

    def calcular_rodadas(self, num_jogadores: int) -> int:
        if num_jogadores <= 8:
            return 3
        elif num_jogadores <= 16:
            return 4
        elif num_jogadores <= 32:
            return 5
        elif num_jogadores <= 64:
            return 6
        else:
            return 7

    @staticmethod
    def validar_distribuicao_mesas(num_jogadores: int) -> Tuple[bool, str]:
        if num_jogadores < 4:
            return False, f"Número de jogadores insuficiente ({num_jogadores}). Mínimo de 4 jogadores necessário."
        resto = num_jogadores % 4
        if resto == 0 or resto == 3:
            return True, ""
        num_menor = num_jogadores - resto
        num_maior = num_menor + (3 if resto == 1 else 4)
        sugestao = f"Distribuição inválida: {num_jogadores} jogadores resultam em uma mesa com {resto} jogador(es). "
        if num_menor >= 4:
            sugestao += f"Adicione {num_maior - num_jogadores} jogador(es) para {num_maior} ou remova {resto} jogador(es) para {num_menor}."
        else:
            sugestao += f"Adicione {num_maior - num_jogadores} jogador(es) para {num_maior}."
        return False, sugestao

    def processar_resultados(self, partida: Partida, resultados: Dict[str, dict], anti_colusao: SistemaAntiColusao) -> None:
        self._validar_resultados(partida, resultados)
        eliminacoes_por_jogador = self._contar_eliminacoes(partida)
        self._calcular_e_atualizar_pontuacoes(partida, resultados, eliminacoes_por_jogador)
        self._analisar_anti_colusao(partida, resultados, anti_colusao)

    def _validar_resultados(self, partida: Partida, resultados: Dict[str, dict]) -> None:
        resultados_por_tipo = [dados["resultado"] for dados in resultados.values()]
        jogadores_ativos = [j for j in partida.jogadores if j not in [e.jogador_eliminado for e in partida.eliminacoes]]
        jogadores_eliminados = [e.jogador_eliminado for e in partida.eliminacoes]

        if "VITORIA" in resultados_por_tipo:
            if resultados_por_tipo.count("VITORIA") > 1 or any(r == "EMPATE" for r in resultados_por_tipo):
                raise ValueError("Não pode haver mais de uma VITORIA ou EMPATE na mesma mesa que uma VITORIA.")
            for r in resultados_por_tipo:
                if r != "VITORIA" and r != "DERROTA":
                    raise ValueError("Todos os outros jogadores devem ter DERROTA se há uma VITORIA.")

        if "EMPATE" in resultados_por_tipo:
            for jogador in jogadores_ativos:
                if resultados[jogador.id]["resultado"] != "EMPATE":
                    raise ValueError("Todos os jogadores ativos devem ter EMPATE.")

        for jogador in jogadores_eliminados:
            if resultados[jogador.id]["resultado"] != "DERROTA":
                raise ValueError("Jogadores eliminados devem ter DERROTA.")

    def _contar_eliminacoes(self, partida: Partida) -> Dict[str, int]:
        eliminacoes = {}
        for jogador in partida.jogadores:
            eliminacoes[jogador.id] = sum(1 for e in partida.eliminacoes if e.jogador_causador == jogador)
        return eliminacoes

    def _calcular_e_atualizar_pontuacoes(self, partida: Partida, resultados: Dict[str, dict], eliminacoes_por_jogador: Dict[str, int]) -> None:
        for jogador_id, dados in resultados.items():
            jogador = next(j for j in partida.jogadores if j.id == jogador_id)
            rp = CalculadorIndiceDesempenho.calcular_rp(dados["resultado"])
            tv = CalculadorIndiceDesempenho.calcular_tv(dados["resultado"], dados["turno"])
            er = CalculadorIndiceDesempenho.calcular_er(dados["resultado"], eliminacoes_por_jogador[jogador_id], len(partida.jogadores))
            pv = CalculadorIndiceDesempenho.calcular_pv(dados["resultado"], dados["vida_final"])
            pa = CalculadorIndiceDesempenho.calcular_pa(dados["resultado"], dados["oponentes_danificados"])
            
            id_calculado = CalculadorIndiceDesempenho.calcular_id(rp, tv, er, pv, pa, len(partida.jogadores) == 3)
            if not CalculadorIndiceDesempenho.validar_pontuacao(id_calculado, dados["resultado"], len(partida.jogadores)):
                raise ValueError(f"Pontuação inválida para {jogador.nome}: {id_calculado}")
            
            jogador.indice_desempenho = id_calculado
            if dados["resultado"] == "VITORIA" and eliminacoes_por_jogador[jogador_id] == len(partida.jogadores) - 1:
                jogador.vitorias_isoladas += 1

    def _analisar_anti_colusao(self, partida: Partida, resultados: Dict[str, dict], anti_colusao: SistemaAntiColusao) -> None:
        suspeitas = anti_colusao.analisar_padroes(partida, resultados)
        if suspeitas:
            print("\nALERTA: Padrões suspeitos detectados!")
            for suspeita in suspeitas:
                print(suspeita)

    def inscrever_jogador(
        self,
        torneio: Torneio,
        jogador: Jogador,
        deck: Deck
    ) -> bool:
        """Inscreve um jogador em um torneio"""
        # Valida se o jogador já está inscrito
        if any(
            i.torneio == torneio and i.jogador == jogador
            for i in self.inscricoes
        ):
            return False
            
        inscricao = Inscricao(torneio, jogador, deck)
        self.inscricoes.append(inscricao)
        return True
        
    def iniciar_torneio(self, torneio: Torneio) -> bool:
        """Inicia um torneio"""
        # Valida número mínimo de jogadores
        inscricoes_torneio = [
            i for i in self.inscricoes if i.torneio == torneio
        ]
        if len(inscricoes_torneio) < torneio.min_jogadores:
            return False
            
        torneio.status = "EM_ANDAMENTO"
        return True
        
    def registrar_resultado(
        self,
        partida: Partida,
        vencedor: Jogador,
        turno: int,
        eliminacoes: list[Eliminacao],
        pontos_vida: dict[Jogador, int],
        dano_causado: dict[Jogador, int]
    ) -> bool:
        """Registra o resultado de uma partida"""
        if partida not in self.partidas:
            return False
            
        # Calcula índices de desempenho
        for jogador in partida.jogadores:
            resultado = "VITORIA" if jogador == vencedor else "DERROTA"
            elim_jogador = sum(
                1 for e in eliminacoes if e.eliminador == jogador
            )
            pv_jogador = pontos_vida.get(jogador, 0)
            dano_jogador = dano_causado.get(jogador, 0)
            
            indice = CalculadorIndiceDesempenho.calcular_indice_partida(
                resultado,
                turno,
                elim_jogador,
                pv_jogador,
                dano_jogador
            )
            
            CalculadorIndiceDesempenho.atualizar_indice_jogador(
                jogador,
                indice
            )
            
        partida.status = "CONCLUIDA"
        return True
        
    def buscar_torneio(self, nome: str) -> Torneio:
        """Busca um torneio pelo nome"""
        return next((t for t in self.torneios if t.nome == nome), None)
        
    def listar_inscricoes(self, torneio: Torneio) -> list[Inscricao]:
        """Lista as inscrições de um torneio"""
        return [i for i in self.inscricoes if i.torneio == torneio]
        
    def listar_partidas(self, torneio: Torneio) -> list[Partida]:
        """Lista as partidas de um torneio"""
        return [p for p in self.partidas if p.torneio == torneio]

class SistemaTorneioCommander:
    def __init__(self):
        self.gerenciador_torneio = GerenciadorTorneio()
        self.gerenciador_cadastros = GerenciadorCadastros()
        self.partidas_ativas: List[Partida] = []
        self.anti_colusao = SistemaAntiColusao()
        self.erros = Utilitarios.mensagens_erro()

    def exibir_menu(self):
        print("\n=== Sistema de Gerenciamento de Torneios Commander ===")
        print("1. Cadastrar Juiz")
        print("2. Cadastrar Torneio")
        print("3. Cadastrar Jogador")
        print("4. Cadastrar Deck do Jogador")
        print("5. Inscrever Jogador no Torneio")
        print("6. Finalizar Inscrições")
        print("7. Iniciar Rodada")
        print("8. Registrar Resultados da Partida")
        print("9. Gerar Ranking")
        print("10. Gerar Relatório")
        print("11. Registrar Eliminação/Desistência Parcial")
        print("12. Registrar Denúncia de Colusão")
        print("13. Aplicar Penalidade")
        print("14. Sair")
        return input("Escolha uma opção (1-14): ") 

    def _validar_torneio_existe(self) -> Torneio:
        if not self.gerenciador_torneio.torneios:
            raise ValueError(self.erros["torneio_nao_existe"])
        return self.gerenciador_torneio.torneios[-1]

    def cadastrar_juiz(self):
        try:
            nome = input("Nome do juiz: ").strip()
            email = input("Email do juiz: ").strip()
            
            # Validação de email
            if not Validador.validar_email(email):
                print(Fore.RED + "Email inválido. Por favor, forneça um email válido." + Style.RESET_ALL)
                return
                
            juiz = self.gerenciador_cadastros.cadastrar_juiz(nome, email)
            
            # Definir senha para o juiz
            senha = input("Senha para o juiz (mínimo 8 caracteres): ").strip()
            valido, mensagem = Validador.validar_senha(senha)
            if not valido:
                print(Fore.RED + f"Erro: {mensagem}" + Style.RESET_ALL)
                return
            juiz.definir_senha(senha)
            
            print(Fore.GREEN + f"Juiz {juiz.nome} cadastrado com sucesso!" + Style.RESET_ALL)
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)

    def cadastrar_torneio(self):
        try:
            nome = input("Nome do torneio: ").strip()
            min_jogadores = input("Mínimo de jogadores: ").strip()
            if not min_jogadores.isdigit() or int(min_jogadores) < 4:
                raise ValueError("Mínimo de jogadores deve ser pelo menos 4.")
            min_jogadores = int(min_jogadores)
            torneio = self.gerenciador_torneio.configurar_torneio(nome, min_jogadores)
            print(Fore.GREEN + f"Torneio {torneio.nome} criado com sucesso! O número de rodadas será definido ao finalizar inscrições." + Style.RESET_ALL)
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)

    def cadastrar_jogador(self):
        try:
            nome = input("Nome do jogador: ").strip()
            email = input("Email do jogador: ").strip()
            
            # Validação de email
            if not Validador.validar_email(email):
                print(Fore.RED + "Email inválido. Por favor, forneça um email válido." + Style.RESET_ALL)
                return
                
            jogador = self.gerenciador_cadastros.cadastrar_jogador(nome, email)
            
            # Definir senha para o jogador
            senha = input("Senha para o jogador (mínimo 8 caracteres): ").strip()
            valido, mensagem = Validador.validar_senha(senha)
            if not valido:
                print(Fore.RED + f"Erro: {mensagem}" + Style.RESET_ALL)
                return
            jogador.definir_senha(senha)
            
            print(Fore.GREEN + f"Jogador {jogador.nome} cadastrado com sucesso!" + Style.RESET_ALL)
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)

    def cadastrar_deck(self):
        try:
            email = input("Email do jogador: ").strip()
            jogador = next((j for j in self.gerenciador_cadastros.jogadores if j.email == email), None)
            if not jogador:
                raise ValueError(self.erros["jogador_nao_encontrado"])
                
            comandante = input("Nome do comandante: ").strip()
            if not comandante:
                raise ValueError("Nome do comandante não pode ser vazio.")
                
            deck = self.gerenciador_cadastros.cadastrar_deck(jogador, comandante)
            print(Fore.GREEN + f"Deck com comandante {deck.comandante} cadastrado com sucesso!" + Style.RESET_ALL)
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL) 

    def inscrever_jogador(self):
        try:
            torneios_abertos = [t for t in self.gerenciador_torneio.torneios if t.inscricoes_abertas]
            if not torneios_abertos:
                raise ValueError("Nenhum torneio com inscrições abertas. Crie um torneio (opção 2).")
                
            print("Torneios disponíveis com inscrições abertas:")
            for i, torneio in enumerate(torneios_abertos, 1):
                print(f"{i}. {torneio.nome}")
                
            torneio_idx = Utilitarios.validar_indice_numerico(input("Selecione o torneio (número): ").strip(), 1, len(torneios_abertos))
            torneio = torneios_abertos[torneio_idx - 1]

            email = input("Email do jogador: ").strip()
            jogador = next((j for j in self.gerenciador_cadastros.jogadores if j.email == email), None)
            if not jogador:
                raise ValueError(self.erros["jogador_nao_encontrado"])
                
            if jogador in torneio.jogadores:
                raise ValueError(f"{jogador.nome} já está inscrito no torneio {torneio.nome}.")

            if not jogador.decks:
                raise ValueError(f"{jogador.nome} não possui decks cadastrados. Cadastre um deck (opção 4).")
                
            # Filtrar apenas decks ativos e não associados a torneios
            decks_disponiveis = [d for d in jogador.decks if d.ativo and d.torneio is None]
            if not decks_disponiveis:
                raise ValueError(f"{jogador.nome} não possui decks disponíveis. Todos os decks já estão em uso em outros torneios.")
                
            print(f"Decks disponíveis de {jogador.nome}:")
            for i, deck in enumerate(decks_disponiveis, 1):
                print(f"{i}. {deck.comandante}")
                
            deck_idx = Utilitarios.validar_indice_numerico(input("Selecione o deck (número): ").strip(), 1, len(decks_disponiveis))
            deck = decks_disponiveis[deck_idx - 1]

            if self.gerenciador_cadastros.validar_deck(deck, torneio):
                torneio.jogadores.append(jogador)
                print(Fore.GREEN + f"{jogador.nome} inscrito no torneio {torneio.nome} com o deck {deck.comandante}!" + Style.RESET_ALL)
            else:
                raise ValueError("Deck inválido ou já associado a outro torneio.")
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)

    def finalizar_inscricoes(self):
        try:
            torneio = self._validar_torneio_existe()
            if not torneio.inscricoes_abertas:
                raise ValueError(f"Inscrições do torneio {torneio.nome} já finalizadas.")
                
            if not torneio.jogadores:
                raise ValueError(f"Nenhum jogador inscrito no torneio {torneio.nome}. Inscreva jogadores primeiro (opção 5).")
                
            if len(torneio.jogadores) < torneio.min_jogadores:
                raise ValueError(f"O torneio {torneio.nome} tem {len(torneio.jogadores)} jogadores. Mínimo de {torneio.min_jogadores} necessário.")
            
            valido, mensagem = self.gerenciador_torneio.validar_distribuicao_mesas(len(torneio.jogadores))
            if not valido:
                raise ValueError(mensagem)
            
            num_rodadas = self.gerenciador_torneio.calcular_rodadas(len(torneio.jogadores))
            torneio.rodadas = num_rodadas
            torneio.inscricoes_abertas = False
            
            num_mesas = len(torneio.jogadores) // 4 + (1 if len(torneio.jogadores) % 4 == 3 else 0)
            print(Fore.GREEN + f"Inscrições do torneio {torneio.nome} finalizadas com sucesso!" + Style.RESET_ALL)
            print(f"Configurado para {num_rodadas} rodadas com {len(torneio.jogadores)} jogadores em {num_mesas} mesa(s).")
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL) 

    def iniciar_rodada(self):
        try:
            torneio = self._validar_torneio_existe()
            if torneio.inscricoes_abertas:
                raise ValueError(f"Inscrições do torneio {torneio.nome} ainda abertas. Finalize as inscrições primeiro (opção 6).")
                
            if not torneio.jogadores:
                raise ValueError(f"Nenhum jogador inscrito no torneio {torneio.nome}. Inscreva jogadores e finalize as inscrições (opções 5 e 6).")
                
            if torneio.rodada_atual >= torneio.rodadas:
                raise ValueError(f"Torneio {torneio.nome} já concluído.")
            
            torneio.rodada_atual += 1
            mesas = self.gerenciador_torneio.emparelhamento.distribuir_jogadores(torneio)
            if not mesas:
                raise ValueError("Nenhuma mesa formada. Verifique o número de jogadores.")
                
            torneio.mesas = mesas
            self.partidas_ativas = [Partida(mesa) for mesa in mesas if mesa]
            
            for partida in self.partidas_ativas:
                self.gerenciador_torneio.tempo.iniciar_temporizador(partida, torneio.tempo_rodada)
            
            print(Fore.GREEN + f"Rodada {torneio.rodada_atual} do torneio {torneio.nome} iniciada com {len(mesas)} mesas:" + Style.RESET_ALL)
            for i, mesa in enumerate(mesas, 1):
                nomes = [j.nome for j in mesa]
                print(f"Mesa {i}: {', '.join(nomes)}")
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)

    def registrar_eliminacao_parcial(self):
        try:
            torneio = self._validar_torneio_existe()
            if not self.partidas_ativas:
                raise ValueError(f"{self.erros['sem_partidas_ativas']} no torneio {torneio.nome}.")
            
            print("Partidas ativas:")
            for i, partida in enumerate(self.partidas_ativas, 1):
                nomes = [j.nome for j in partida.jogadores]
                print(f"{i}. Mesa com {', '.join(nomes)}")
            
            idx = Utilitarios.validar_indice_numerico(input("Selecione a partida (número): ").strip(), 1, len(self.partidas_ativas))
            partida = self.partidas_ativas[idx - 1]
            
            print("Jogadores na partida:")
            for i, jogador in enumerate(partida.jogadores, 1):
                print(f"{i}. {jogador.nome}")
            
            elim_idx = Utilitarios.validar_indice_numerico(input("Selecione o jogador eliminado/desistente (número): ").strip(), 1, len(partida.jogadores))
            jogador_eliminado = partida.jogadores[elim_idx - 1]
            
            # Verificar se o jogador já foi eliminado
            if any(e.jogador_eliminado == jogador_eliminado for e in partida.eliminacoes):
                raise ValueError(f"{jogador_eliminado.nome} já foi eliminado nesta partida.")
            
            desistiu = input("Foi desistência? (S/N): ").strip().upper() == "S"
            causador_idx = None
            if not desistiu:
                print("Selecione o jogador que causou a eliminação (ou 0 para auto-eliminação):")
                for i, jogador in enumerate(partida.jogadores, 1):
                    if jogador != jogador_eliminado:
                        print(f"{i}. {jogador.nome}")
                print("0. Auto-eliminação")
                
                causador_idx = input("Número: ").strip()
                if not causador_idx.isdigit() or int(causador_idx) < 0 or int(causador_idx) > len(partida.jogadores):
                    raise ValueError("Causador inválido.")
                    
                causador_idx = int(causador_idx) - 1 if int(causador_idx) > 0 else None
            
            turno = input("Turno da eliminação/desistência: ").strip()
            if not turno.isdigit() or int(turno) < 1:
                raise ValueError("Turno deve ser um número positivo.")
                
            turno = int(turno)
            # Validação de turno com base nos turnos extras permitidos
            if not partida.validar_turno(turno, torneio):
                raise ValueError(f"Turno {turno} excede o limite permitido (máximo: {partida.turno_atual + torneio.turnos_extras}).")
            
            vida_final = input("Vida final do jogador eliminado/desistente: ").strip()
            if not vida_final.isdigit() or int(vida_final) < 0:
                raise ValueError("Vida final deve ser não-negativa.")
                
            vida_final = int(vida_final)
            # Aplicar limite de 40 pontos de vida
            vida_final = min(vida_final, 40)
            
            if vida_final > 1000:
                print(Fore.YELLOW + f"Aviso: Vida final de {vida_final} é muito alta. Verifique se está correto." + Style.RESET_ALL)
            
            jogador_causador = partida.jogadores[causador_idx] if causador_idx is not None else None
            eliminacao = Eliminacao(jogador_eliminado, jogador_causador, turno, desistiu)
            partida.eliminacoes.append(eliminacao)
            
            rp = CalculadorIndiceDesempenho.calcular_rp("DERROTA")
            tv = CalculadorIndiceDesempenho.calcular_tv("DERROTA", turno)
            er = 0
            pv = CalculadorIndiceDesempenho.calcular_pv("DERROTA", vida_final)
            pa = 0
            mesa_tres = len(partida.jogadores) == 3
            id_parcial = CalculadorIndiceDesempenho.calcular_id(rp, tv, er, pv, pa, mesa_tres)
            
            print(Fore.GREEN + f"{jogador_eliminado.nome} {'desistiu' if desistiu else 'eliminado por ' + (jogador_causador.nome if jogador_causador else 'auto-eliminação')} no turno {turno}." + Style.RESET_ALL)
            print(f"Pontuação parcial: {id_parcial:.2f}%")
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL) 

    def registrar_resultados_partida(self):
        try:
            torneio = self._validar_torneio_existe()
            if not self.partidas_ativas:
                raise ValueError(f"{self.erros['sem_partidas_ativas']} no torneio {torneio.nome}.")
            
            print("Partidas ativas:")
            for i, partida in enumerate(self.partidas_ativas, 1):
                nomes = [j.nome for j in partida.jogadores]
                print(f"{i}. Mesa com {', '.join(nomes)}")
            
            idx = Utilitarios.validar_indice_numerico(input("Selecione a partida (número): ").strip(), 1, len(self.partidas_ativas))
            partida = self.partidas_ativas[idx - 1]
            
            if self.gerenciador_torneio.tempo.verificar_tempo(partida, torneio):
                print(Fore.YELLOW + "Tempo da rodada esgotado. Forçando empate para jogadores ativos." + Style.RESET_ALL)
                resultados = {}
                jogadores_ativos = [j for j in partida.jogadores if j not in [e.jogador_eliminado for e in partida.eliminacoes]]
                for jogador in jogadores_ativos:
                    resultados[jogador.id] = {
                        "resultado": "EMPATE",
                        "turno": partida.turno_atual,
                        "eliminacoes": 0,
                        "vida_final": 16,
                        "oponentes_danificados": 0
                    }
                for jogador in partida.jogadores:
                    if jogador not in jogadores_ativos:
                        resultados[jogador.id] = {
                            "resultado": "DERROTA",
                            "turno": partida.turno_atual,
                            "eliminacoes": 0,
                            "vida_final": 0,
                            "oponentes_danificados": 0
                        }
            else:
                resultados = {}
                jogadores_ativos = [j for j in partida.jogadores if j not in [e.jogador_eliminado for e in partida.eliminacoes]]
                vitoria_registrada = False
                for jogador in partida.jogadores:
                    print(f"\nRegistrando resultados para {jogador.nome}:")
                    if jogador not in jogadores_ativos:
                        print(f"{jogador.nome} já eliminado/desistente. Atribuindo DERROTA.")
                        eliminacao = next(e for e in partida.eliminacoes if e.jogador_eliminado == jogador)
                        resultados[jogador.id] = {
                            "resultado": "DERROTA",
                            "turno": eliminacao.turno,
                            "eliminacoes": 0,
                            "vida_final": 0,
                            "oponentes_danificados": 0
                        }
                        continue
                    
                    resultado = input("Resultado (VITORIA/EMPATE/DERROTA): ").upper()
                    if resultado not in ["VITORIA", "EMPATE", "DERROTA"]:
                        raise ValueError("Resultado inválido. Use VITORIA, EMPATE ou DERROTA.")
                    
                    # Validação reforçada para uma única vitória
                    if resultado == "VITORIA":
                        if vitoria_registrada:
                            raise ValueError(f"Já foi registrada uma VITORIA para outro jogador. Apenas um jogador pode vencer.")
                        vitoria_registrada = True
                    
                    # Validação preliminar de consistência para jogadores eliminados
                    if resultado in ["VITORIA", "EMPATE"] and jogador in [e.jogador_eliminado for e in partida.eliminacoes]:
                        raise ValueError(f"Jogador eliminado ({jogador.nome}) deve ter DERROTA como resultado.")
                    
                    # Validação preliminar de consistência para garantir coerência de resultados
                    resultados_por_tipo = [dados["resultado"] for dados in resultados.values() if dados["resultado"] != "DERROTA"]
                    if resultado == "EMPATE" and any(r == "VITORIA" for r in resultados_por_tipo):
                        raise ValueError(f"Não pode registrar EMPATE para {jogador.nome} quando outro jogador ativo tem VITORIA.")
                    if resultado == "VITORIA" and any(r == "EMPATE" for r in resultados_por_tipo):
                        raise ValueError(f"Não pode registrar VITORIA para {jogador.nome} quando outro jogador ativo tem EMPATE.")
                    if resultado == "EMPATE" and any(r != "EMPATE" and r != "DERROTA" for r in resultados_por_tipo):
                        raise ValueError(f"Todos os jogadores ativos devem ter EMPATE se {jogador.nome} tem EMPATE.")
                    
                    turno = input("Turno final: ").strip()
                    if not turno.isdigit() or int(turno) < 1:
                        raise ValueError("Turno final deve ser um número positivo.")
                    
                    turno = int(turno)
                    # Validação de turno com base nos turnos extras permitidos
                    if not partida.validar_turno(turno, torneio):
                        raise ValueError(f"Turno {turno} excede o limite permitido (máximo: {partida.turno_atual + torneio.turnos_extras}).")
                    
                    vida_final = input("Vida final: ").strip()
                    if not vida_final.isdigit() or int(vida_final) < 0:
                        raise ValueError("Vida final deve ser não-negativa.")
                    
                    vida_final = int(vida_final)
                    # Aplicar limite de 40 pontos de vida
                    vida_final = min(vida_final, 40)
                    
                    if vida_final > 1000:
                        print(Fore.YELLOW + f"Aviso: Vida final de {vida_final} é muito alta. Verifique se está correto." + Style.RESET_ALL)
                    
                    oponentes_danificados = input(f"Oponentes danificados (0-{len(partida.jogadores)-1}): ").strip()
                    if not oponentes_danificados.isdigit() or int(oponentes_danificados) < 0 or int(oponentes_danificados) > len(partida.jogadores) - 1:
                        raise ValueError(f"Oponentes danificados deve ser entre 0 e {len(partida.jogadores)-1}.")
                    
                    oponentes_danificados = int(oponentes_danificados)
                    
                    resultados[jogador.id] = {
                        "resultado": resultado,
                        "turno": turno,
                        "eliminacoes": 0,
                        "vida_final": vida_final,
                        "oponentes_danificados": oponentes_danificados
                    }
                
                # Validação final de consistência para empate
                resultados_por_tipo = [dados["resultado"] for dados in resultados.values() if dados["resultado"] != "DERROTA"]
                if "EMPATE" in resultados_por_tipo and not all(r == "EMPATE" for r in resultados_por_tipo):
                    raise ValueError("Todos os jogadores ativos devem ter EMPATE se um jogador ativo tem EMPATE.")
                if "VITORIA" in resultados_por_tipo and "EMPATE" in resultados_por_tipo:
                    raise ValueError("Não pode haver VITORIA e EMPATE na mesma mesa.")
            
            self.gerenciador_torneio.processar_resultados(partida, resultados, self.anti_colusao)
            
            # Gerar ranking da partida
            print(Fore.GREEN + "\n=== Ranking da Partida ===" + Style.RESET_ALL)
            jogadores_com_pontuacao = [(jogador, partida.pontuacoes.get(jogador.id, 0)) for jogador in partida.jogadores]
            ranking_mesa = sorted(
                jogadores_com_pontuacao,
                key=lambda x: (
                    x[1],  # Índice de Desempenho da partida
                    self.gerenciador_torneio.desempate.calcular_forca_oponentes(x[0], self.partidas_ativas),
                    x[0].vitorias_isoladas
                ),
                reverse=True
            )
            for i, (jogador, id_partida) in enumerate(ranking_mesa, 1):
                resultado = resultados[jogador.id]["resultado"]
                print(f"{i}. {jogador.nome}: {id_partida:.2f} pontos ({resultado})")
            
            self.partidas_ativas.pop(idx - 1)
            print(Fore.GREEN + "Resultados registrados com sucesso!" + Style.RESET_ALL)
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)

    def registrar_denuncia(self):
        try:
            email = input("Email do jogador denunciado: ").strip()
            
            # Validação de email
            if not Validador.validar_email(email):
                print(Fore.RED + "Email inválido. Por favor, forneça um email válido." + Style.RESET_ALL)
                return
                
            jogador = next((j for j in self.gerenciador_cadastros.jogadores if j.email == email), None)
            if not jogador:
                raise ValueError(self.erros["jogador_nao_encontrado"])
                
            descricao = input("Descrição da denúncia: ").strip()
            if not descricao:
                raise ValueError("A descrição da denúncia não pode ser vazia.")
                
            self.anti_colusao.registrar_denuncia(jogador, descricao)
            print(Fore.GREEN + "Denúncia registrada com sucesso." + Style.RESET_ALL)
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)

    def aplicar_penalidade(self):
        try:
            torneio = self._validar_torneio_existe()
            
            # Verificar se o usuário é um juiz
            email_juiz = input("Email do juiz: ").strip()
            senha_juiz = input("Senha do juiz: ").strip()
            
            juiz = next((j for j in self.gerenciador_cadastros.juizes if j.email == email_juiz), None)
            if not juiz:
                raise ValueError("Juiz não encontrado.")
                
            if not hasattr(juiz, 'senha_hash') or juiz.senha_hash != senha_juiz:  # Em produção, usar verificação de hash segura
                raise ValueError("Autenticação falhou. Senha incorreta.")
            
            email = input("Email do jogador a penalizar: ").strip()
            
            # Validação de email
            if not Validador.validar_email(email):
                print(Fore.RED + "Email inválido. Por favor, forneça um email válido." + Style.RESET_ALL)
                return
                
            jogador = next((j for j in self.gerenciador_cadastros.jogadores if j.email == email), None)
            if not jogador:
                raise ValueError(self.erros["jogador_nao_encontrado"])
            
            print("Tipos de penalidade:")
            print("1. Advertência")
            print("2. Redução de 20% no ID")
            print("3. Desclassificação")
            
            tipo_idx = Utilitarios.validar_indice_numerico(input("Selecione o tipo (1-3): ").strip(), 1, 3)
            tipo = ["ADVERTENCIA", "REDUCAO_ID", "DESCLASSIFICACAO"][tipo_idx - 1]
            
            self.anti_colusao.aplicar_penalidade(jogador, tipo, torneio)
            print(Fore.GREEN + "Penalidade aplicada com sucesso." + Style.RESET_ALL)
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL) 

    def gerar_ranking(self):
        try:
            torneio = self._validar_torneio_existe()
            if not torneio.jogadores:
                raise ValueError(f"Nenhum jogador inscrito no torneio {torneio.nome}. Inscreva jogadores primeiro (opção 5).")
            
            ranking = sorted(
                torneio.jogadores, 
                key=lambda x: (
                    x.indice_desempenho, 
                    self.gerenciador_torneio.desempate.calcular_forca_oponentes(x, self.partidas_ativas), 
                    x.vitorias_isoladas
                ), 
                reverse=True
            )
            
            print(Fore.GREEN + f"\n=== Ranking do Torneio {torneio.nome} ===" + Style.RESET_ALL)
            if not ranking:
                print("Nenhum jogador com pontuação registrada.")
            else:
                for i, jogador in enumerate(ranking, 1):
                    forca_oponentes = self.gerenciador_torneio.desempate.calcular_forca_oponentes(jogador, self.partidas_ativas)
                    winrate = (jogador.vitorias_isoladas / len(jogador.historico_partidas)) * 100 if jogador.historico_partidas else 0
                    print(f"{i}. {jogador.nome}: {jogador.indice_desempenho:.2f} pontos | Vitórias: {jogador.vitorias_isoladas} | Winrate: {winrate:.2f}% | Força dos Oponentes: {forca_oponentes:.2f}")
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)

    def gerar_relatorio(self):
        try:
            filtro_torneio = input("Filtrar por torneio (deixe em branco para mostrar todos): ").strip()
            filtro_status = input("Filtrar por status [ATIVO/INATIVO/TODOS] (padrão: TODOS): ").strip().upper()
            if filtro_status not in ["ATIVO", "INATIVO", "TODOS", ""]:
                filtro_status = "TODOS"
            
            print(Fore.GREEN + "\n=== Relatório do Sistema de Torneios Commander ===" + Style.RESET_ALL)
            
            print(Fore.CYAN + "\nJuízes Cadastrados:" + Style.RESET_ALL)
            if not self.gerenciador_cadastros.juizes:
                print("  Nenhum juiz cadastrado.")
            else:
                for juiz in self.gerenciador_cadastros.juizes:
                    print(f"  - {juiz.nome} ({juiz.email})")
            
            print(Fore.CYAN + "\nTorneios:" + Style.RESET_ALL)
            torneios_filtrados = self.gerenciador_torneio.torneios
            if filtro_torneio:
                torneios_filtrados = [t for t in torneios_filtrados if filtro_torneio.lower() in t.nome.lower()]
            
            if not torneios_filtrados:
                print("  Nenhum torneio encontrado com o filtro aplicado.")
            else:
                for torneio in torneios_filtrados:
                    status = "Inscrições Abertas" if torneio.inscricoes_abertas else "Inscrições Finalizadas"
                    if not torneio.inscricoes_abertas:
                        status += f" ({'Concluído' if torneio.rodada_atual >= torneio.rodadas else 'Em Andamento, Rodada ' + str(torneio.rodada_atual)})"
                    
                    ativo = torneio.inscricoes_abertas or torneio.rodada_atual < torneio.rodadas
                    if filtro_status == "ATIVO" and not ativo:
                        continue
                    if filtro_status == "INATIVO" and ativo:
                        continue
                    
                    num_mesas = len(torneio.jogadores) // 4 + (1 if len(torneio.jogadores) % 4 == 3 else 0) if torneio.jogadores else 0
                    print(Fore.YELLOW + f"\n  Torneio: {torneio.nome}" + Style.RESET_ALL)
                    print(f"    Data de Criação: {torneio.data.strftime('%d/%m/%Y %H:%M')}")
                    print(f"    Status: {status}")
                    print(f"    Mínimo de Jogadores: {torneio.min_jogadores}")
                    print(f"    Jogadores Inscritos: {len(torneio.jogadores)}")
                    print(f"    Rodadas: {torneio.rodadas}")
                    print(f"    Mesas: {num_mesas}")
                    print("    Jogadores e Decks:")
                    if not torneio.jogadores:
                        print("      Nenhum jogador inscrito.")
                    else:
                        for jogador in torneio.jogadores:
                            deck = next((d for d in jogador.decks if d.torneio == torneio), None)
                            deck_info = deck.comandante if deck else "Sem deck associado"
                            print(f"      - {jogador.nome} ({jogador.email}): Deck {deck_info}")
                    print("    Estatísticas do Torneio:")
                    if torneio.jogadores:
                        media_id = Utilitarios.calcular_media_ids(torneio.jogadores)
                        comandantes = [d.comandante for j in torneio.jogadores for d in j.decks if d.torneio == torneio]
                        print(f"      Média de ID: {media_id:.2f}")
                        print(f"      Comandantes utilizados: {', '.join(set(comandantes)) if comandantes else 'Nenhum'}")
            
            print(Fore.CYAN + "\nJogadores Cadastrados:" + Style.RESET_ALL)
            if not self.gerenciador_cadastros.jogadores:
                print("  Nenhum jogador cadastrado.")
            else:
                for jogador in self.gerenciador_cadastros.jogadores:
                    print(Fore.YELLOW + f"\n  Jogador: {jogador.nome} ({jogador.email})" + Style.RESET_ALL)
                    print("    Decks:")
                    if not jogador.decks:
                        print("      Nenhum deck cadastrado.")
                    else:
                        for deck in jogador.decks:
                            status = "Ativo" if deck.ativo else "Inativo"
                            torneio_info = deck.torneio.nome if deck.torneio else "Não associado a torneio"
                            print(f"      - {deck.comandante} (Torneio: {torneio_info}, Status: {status})")
                    print("    Torneios Participados/Participando:")
                    torneios_jogador = [t for t in self.gerenciador_torneio.torneios if jogador in t.jogadores]
                    if not torneios_jogador:
                        print("      Nenhum torneio.")
                    else:
                        for t in torneios_jogador:
                            status = "Inscrições Abertas" if t.inscricoes_abertas else ("Concluído" if t.rodada_atual >= t.rodadas else f"Em Andamento, Rodada {t.rodada_atual}")
                            print(f"      - {t.nome} ({status})")
                    print("    Visão Individual:")
                    if not jogador.historico_partidas:
                        print("      Nenhuma partida registrada.")
                    else:
                        winrate = (jogador.vitorias_isoladas / len(jogador.historico_partidas)) * 100 if jogador.historico_partidas else 0
                        print(f"      Vitórias Isoladas: {jogador.vitorias_isoladas}")
                        print(f"      Winrate: {winrate:.2f}%")
                        print(f"      Índice de Desempenho Total: {jogador.indice_desempenho:.2f}")
                        print("      Histórico de Partidas:")
                        for partida in jogador.historico_partidas:
                            id_partida = partida.pontuacoes.get(jogador.id, 0)
                            resultado = "Desconhecido"
                            for jid, dados in partida.pontuacoes.items():
                                if jid == jogador.id:
                                    resultado = dados["resultado"] if isinstance(dados, dict) and "resultado" in dados else "Desconhecido"
                            print(f"        - Mesa com {', '.join(j.nome for j in partida.jogadores)}: ID {id_partida:.2f} ({resultado})")
                            print("          Eliminações:")
                            for e in partida.eliminacoes:
                                if e.jogador_causador == jogador:
                                    print(f"            Eliminou {e.jogador_eliminado.nome} no turno {e.turno}")
                                elif e.jogador_eliminado == jogador:
                                    causador = e.jogador_causador.nome if e.jogador_causador else "Auto-eliminação"
                                    tipo = "Desistência" if e.desistiu else "Eliminação"
                                    print(f"            {tipo} por {causador} no turno {e.turno}")
        except ValueError as e:
            print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Erro inesperado ao gerar relatório: {e}" + Style.RESET_ALL)

    def executar(self):
        # Tenta carregar dados salvos anteriormente
        dados_carregados = Persistencia.carregar_estado(self)
        if dados_carregados:
            print(Fore.GREEN + "Dados do sistema carregados com sucesso!" + Style.RESET_ALL)
        
        while True:
            opcao = self.exibir_menu()
            try:
                if opcao == "1":
                    self.cadastrar_juiz()
                elif opcao == "2":
                    self.cadastrar_torneio()
                elif opcao == "3":
                    self.cadastrar_jogador()
                elif opcao == "4":
                    self.cadastrar_deck()
                elif opcao == "5":
                    self.inscrever_jogador()
                elif opcao == "6":
                    self.finalizar_inscricoes()
                elif opcao == "7":
                    self.iniciar_rodada()
                elif opcao == "8":
                    self.registrar_resultados_partida()
                elif opcao == "9":
                    self.gerar_ranking()
                elif opcao == "10":
                    self.gerar_relatorio()
                elif opcao == "11":
                    self.registrar_eliminacao_parcial()
                elif opcao == "12":
                    self.registrar_denuncia()
                elif opcao == "13":
                    self.aplicar_penalidade()
                elif opcao == "14":
                    # Salva os dados antes de sair
                    Persistencia.salvar_estado(self)
                    print(Fore.GREEN + "Dados do sistema salvos. Saindo do sistema. Até logo!" + Style.RESET_ALL)
                    break
                else:
                    print(Fore.RED + "Opção inválida. Escolha entre 1 e 14." + Style.RESET_ALL)
            except ValueError as e:
                print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Erro inesperado: {e}" + Style.RESET_ALL)
            
            # Salva os dados após cada operação
            try:
                Persistencia.salvar_estado(self)
            except Exception as e:
                print(Fore.YELLOW + f"Aviso: Não foi possível salvar o estado: {e}" + Style.RESET_ALL)


if __name__ == "__main__":
    sistema = SistemaTorneioCommander()
    sistema.executar() 

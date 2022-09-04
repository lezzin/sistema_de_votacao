import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

ESTILO_INPUT = "background-color: #fff; color: #000; border: none; border-radius: 5px; padding: 7px;"
ESTILO_BOTAO = "border: none; background-color: #9ecfc2; color: #333; font-size: 13px; font-family: Arial; border-radius: 4px; padding: 10px;"
ESTILO_BOTAO_SAIR = "border: none; background-color: #b22222; color: #fff; font-size: 12px; font-family: Arial; border-radius: 4px; padding: 10px;"
ESTILO_TITULO = "font-size: 20px; font-family: Arial; color: #fff; font-weight: bold;"
ESTILO_TEXTO = "font-size: 15px; font-family: Arial; color: #fff;"
ESTILO_LISTA = "font-size: 15px; font-family: Arial; color: #fff; border: none; background-color: #252525; border-radius: 5px; padding: 7px;"
BACKGROUND = "background-color: #2b2b2b;"

num_votos = 0
participantes = []
votos = {}
votos["branco"] = 0
contagem = 1


# janela de erro (widget)
def widget_erro(titulo, mensagem):
    mensagem_erro = QMessageBox()

    mensagem_erro.setWindowTitle(titulo)
    mensagem_erro.setText(mensagem)
    mensagem_erro.setIcon(QMessageBox.Critical)

    mensagem_erro.exec_()


# janela principal
class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("robo.png"))
        self.setWindowTitle("Página Inicial")
        self.setStyleSheet(BACKGROUND)
        self.setFixedSize(540, 540)
        self.design_tela()

    def design_tela(self):
        self.titulo = QLabel(
            "Olá, seja bem vindo ao nosso sistema de votação!", self)
        self.titulo.setWordWrap(True)
        self.titulo.setStyleSheet(ESTILO_TITULO)
        self.titulo.setAlignment(Qt.AlignCenter)

        self.imagem = QLabel(self)
        self.imagem.setPixmap(QPixmap("robo.png"))
        self.imagem.resize(120, 120)
        self.imagem.setAlignment(Qt.AlignCenter)

        self.botao_iniciar = QPushButton("Iniciar", self)
        self.botao_iniciar.clicked.connect(self.nova_janela)
        self.botao_iniciar.setStyleSheet(ESTILO_BOTAO)

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.titulo, 0, 0)
        self.layout.addWidget(self.imagem, 1, 0, 1, 2)
        self.layout.addWidget(self.botao_iniciar, 2, 0)

        self.setLayout(self.layout)
        self.show()

    def nova_janela(self):
        self.nova_janela = Configuracao()
        self.close()


# janela de configurações
class Configuracao(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("robo.png"))
        self.setWindowTitle("Configurações")
        self.setFixedSize(540, 540)
        self.setStyleSheet(BACKGROUND)
        self.design_tela()

    def design_tela(self):
        self.titulo = QLabel("Configurações da votação", self)
        self.titulo.setStyleSheet(f"{ESTILO_TITULO}; margin-bottom: 20px")
        self.titulo.setAlignment(Qt.AlignCenter)

        self.num_votos_texto = QLabel("Número de votos:", self)
        self.num_votos_texto.setStyleSheet(ESTILO_TEXTO)
        self.num_votos_texto.setAlignment(Qt.AlignCenter)

        self.input_num_votos = QLineEdit(self)
        self.input_num_votos.setStyleSheet(ESTILO_INPUT)
        self.input_num_votos.setPlaceholderText("Digite o número de votos")

        self.candidatos_texto = QLabel(
            "Informe o nome dos candidatos (separados por vírgula):", self)
        self.candidatos_texto.setWordWrap(True)
        self.candidatos_texto.setStyleSheet(ESTILO_TEXTO)
        self.candidatos_texto.setAlignment(Qt.AlignCenter)

        self.input_candidatos = QLineEdit(self)
        self.input_candidatos.setStyleSheet(ESTILO_INPUT)
        self.input_candidatos.setPlaceholderText("Digite os candidatos")

        self.botao_iniciar = QPushButton("Iniciar votação", self)
        self.botao_iniciar.setStyleSheet(f"{ESTILO_BOTAO}; margin-top: 30px")
        self.botao_iniciar.clicked.connect(self.salvar_numero_de_votos)

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(50, 0, 50, 0)

        self.layout.addWidget(self.titulo, 0, 0, 1, 2)
        self.layout.addWidget(self.num_votos_texto, 1, 0)
        self.layout.addWidget(self.input_num_votos, 1, 1)
        self.layout.addWidget(self.candidatos_texto, 3, 0)
        self.layout.addWidget(self.input_candidatos, 3, 1)
        self.layout.addWidget(self.botao_iniciar, 5, 0, 1, 2)

        self.setLayout(self.layout)
        self.show()

    def salvar_numero_de_votos(self):
        global num_votos, votos

        if self.input_num_votos.text().isdigit() and self.input_candidatos.text() != "" and len(self.input_candidatos.text().split(",")) > 1:
            num_votos = int(self.input_num_votos.text())
            self.salvar_nomes()
            self.nova_janela()
        else:
            if self.input_candidatos.text() == "":
                widget_erro("Erro - candidatos",
                            "Por favor, informe os candidatos!")
            elif self.input_num_votos.text().isdigit() == False:
                widget_erro("Erro - número de votos",
                            "Por favor, informe um número válido!")
            else:
                widget_erro("Erro - número de candidatos",
                            "Por favor, informe mais de um candidato!")

    def salvar_nomes(self):
        participantes = self.input_candidatos.text().split(",")
        for participante in participantes:
            votos[participante] = 0

    def nova_janela(self):
        self.nova_janela = Votacao()
        self.close()


# janela de votação
class Votacao(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("robo.png"))
        self.setWindowTitle("Votação")
        self.setFixedSize(540, 540)
        self.setStyleSheet(BACKGROUND)
        self.design_tela()

    def design_tela(self):
        global contagem

        self.texto_num_voto = QLabel(self)
        self.texto_num_voto.setText(f"Voto número: {contagem}")
        self.texto_num_voto.setStyleSheet(
            f"{ESTILO_TITULO}; margin-bottom: 20px")
        self.texto_num_voto.setAlignment(Qt.AlignCenter)

        self.input_voto = QLineEdit(self)
        self.input_voto.setStyleSheet(ESTILO_INPUT)
        self.input_voto.setPlaceholderText("Digite o nome do candidato")
        self.input_voto.setFixedWidth(300)

        self.mensagem = QLabel("", self)
        self.mensagem.setStyleSheet(f"{ESTILO_TEXTO}; margin-bottom: 20px")
        self.mensagem.setAlignment(Qt.AlignCenter)

        self.botao_votar = QPushButton("Votar", self)
        self.botao_votar.setStyleSheet(f"{ESTILO_BOTAO}; padding: 7px")
        self.botao_votar.clicked.connect(self.adicionar_voto)

        self.botao_mostra_candidatos = QPushButton("Mostrar candidatos", self)
        self.botao_mostra_candidatos.setStyleSheet(ESTILO_BOTAO)
        self.botao_mostra_candidatos.clicked.connect(self.mostrar_candidatos)

        self.botao_nova_pagina = QPushButton(
            "Exibir resultados", self, visible=False)
        self.botao_nova_pagina.clicked.connect(self.nova_janela)
        self.botao_nova_pagina.setStyleSheet(
            f"{ESTILO_BOTAO}; margin-top: 30px")

        self.layout = QGridLayout()
        self.layout.addWidget(self.texto_num_voto, 1, 0, 1, 2)
        self.layout.addWidget(self.input_voto, 2, 0)
        self.layout.addWidget(self.botao_votar, 2, 1)
        self.layout.addWidget(self.mensagem, 4, 0, 1, 2)
        self.layout.addWidget(self.botao_nova_pagina, 5, 0, 1, 2)
        self.layout.addWidget(self.botao_mostra_candidatos, 6, 0, 1, 2)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self.show()

    def mostrar_candidatos(self):
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon("robo.png"))
        self.widget.setWindowTitle("Candidatos")
        self.widget.setFixedSize(300, 300)
        self.widget.setStyleSheet(BACKGROUND)

        self.candidatos = QLabel(self.widget)
        self.candidatos.setText(
            "Candidatos: " + ", ".join([candidato for candidato in votos if candidato != "branco"]))
        self.candidatos.setStyleSheet(ESTILO_TEXTO)
        self.candidatos.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.candidatos, 0, 0)

        self.widget.setLayout(self.layout)
        self.widget.show()

    def contar_numero_de_votos(self):
        global contagem
        contagem += 1
        self.texto_num_voto.setText(f"Voto número: {contagem}")

        if contagem == (num_votos + 1):
            self.botao_votar.setVisible(False)
            self.texto_num_voto.setVisible(False)
            self.input_voto.setVisible(False)
            self.botao_nova_pagina.setVisible(True)
            self.mensagem.setText("Votação encerrada!")

    def adicionar_voto(self):
        voto = self.input_voto.text().lower()

        if voto in votos:
            votos[voto] += 1
        else:
            votos["branco"] += 1

        self.contar_numero_de_votos()
        self.input_voto.setText("")
        self.input_voto.setFocus()

    def nova_janela(self):
        self.nova_janela = Resultado()
        self.close()


# janela de resultado
class Resultado(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("robo.png"))
        self.setWindowTitle("Resultado")
        self.setFixedSize(540, 540)
        self.setStyleSheet(BACKGROUND)
        self.design_tela()

    def design_tela(self):
        self.imagem = QLabel(self)
        self.imagem.setPixmap(QPixmap("robo.png"))
        self.imagem.setFixedSize(170, 170)

        self.label_resultado = QLabel(
            f"{self.verificar_resultado()}\nO número de votos foi de {num_votos} votos.", self)
        self.label_resultado.setStyleSheet(
            f"{ESTILO_TITULO}; margin-bottom: 10px")
        self.label_resultado.setAlignment(Qt.AlignCenter)

        self.creditos = QLabel(
            "Desenvolvido por: Leandro Adrian, João Moreira, Inaiê Moreira e Mariana Almeida", self)
        self.creditos.setStyleSheet(
            "font-size: 12px; color: grey; margin-top: 20px")
        self.creditos.setAlignment(Qt.AlignCenter)
        self.creditos.setWordWrap(True)

        self.botao_resultado = QPushButton("Fechar página", self)
        self.botao_resultado.setStyleSheet(ESTILO_BOTAO_SAIR)
        self.botao_resultado.clicked.connect(self.close)

        self.botao_resultado_detalhado = QPushButton(
            "Resultado detalhado", self)
        self.botao_resultado_detalhado.setStyleSheet(ESTILO_BOTAO)
        self.botao_resultado_detalhado.clicked.connect(self.nova_janela)

        self.botao_pagina_inicial = QPushButton("Página inicial", self)
        self.botao_pagina_inicial.setStyleSheet(ESTILO_BOTAO)
        self.botao_pagina_inicial.clicked.connect(self.reiniciar_votacao)

        self.layout = QGridLayout()
        self.layout.addWidget(self.imagem, 0, 0, 1, 3, Qt.AlignCenter)
        self.layout.addWidget(self.label_resultado, 1, 0, 1, 3)
        self.layout.addWidget(self.botao_resultado, 2, 0, Qt.AlignLeft)
        self.layout.addWidget(
            self.botao_resultado_detalhado, 2, 1, Qt.AlignCenter)
        self.layout.addWidget(self.botao_pagina_inicial, 2, 2, Qt.AlignRight)
        self.layout.addWidget(self.creditos, 3, 0, 1, 3)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self.show()

    def verificar_resultado(self):
        duplicados = {}
        empate = False

        for candidato, voto in votos.items():
            if candidato != "branco":
                duplicados.setdefault(voto, set()).add(candidato)

            if duplicados != {}:
                if len(duplicados[max(duplicados)]) > 1 and candidato != "branco":
                    empate = True

            if voto == max(votos.values()) and candidato != "branco":
                vencedor = candidato
            elif voto == sorted(votos.values(), reverse=True)[1] and candidato == "branco":
                vencedor = candidato

        if empate:
            return "Empate entre os candidatos!"
        else:
            return (f"O vencedor é: \"{vencedor}\". Parabéns!")

    def reiniciar_votacao(self):
        global contagem, votos, num_votos, participantes

        msg = QMessageBox()
        msg.setWindowTitle("Confirmar")
        msg.setText("Tem certeza que deseja reiniciar a votação?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setIcon(QMessageBox.Question)
        resposta = msg.exec_()

        if resposta == QMessageBox.Yes:
            num_votos = 0
            participantes = []
            votos = {"branco": 0}
            contagem = 1

            self.newWindow = Main()
            self.close()
        else:
            pass

    def nova_janela(self):
        self.nova_janela = ResultadoDetalhado()
        self.close()


# janela de resultado detalhado
class ResultadoDetalhado(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("robo.png"))
        self.setWindowTitle("Resultado detalhado")
        self.setFixedSize(540, 540)
        self.setStyleSheet(BACKGROUND)
        self.design_tela()

    def design_tela(self):
        self.label_resultado = QLabel(
            "Resultado detalhado dos candidatos", self)
        self.label_resultado.setStyleSheet(
            f"{ESTILO_TITULO}; margin-bottom: 30px")
        self.label_resultado.setAlignment(Qt.AlignCenter)

        self.label_resultado_detalhado = QLabel(self)
        self.label_resultado_detalhado.setStyleSheet(ESTILO_TEXTO)
        self.label_resultado_detalhado.setText(
            self.exibir_resultado_detalhado())

        self.botao_sair = QPushButton("Sair", self)
        self.botao_sair.setStyleSheet(ESTILO_BOTAO_SAIR)
        self.botao_sair.clicked.connect(self.close)

        self.botao_voltar = QPushButton("Voltar ao resultado", self)
        self.botao_voltar.setStyleSheet(ESTILO_BOTAO)
        self.botao_voltar.clicked.connect(self.voltar_pagina_anterior)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label_resultado, 1, 0, 1, 2)
        self.layout.addWidget(self.label_resultado_detalhado, 3, 0, 1, 2)
        self.layout.addWidget(self.botao_voltar, 5, 1, Qt.AlignRight)
        self.layout.addWidget(self.botao_sair, 5, 1, Qt.AlignLeft)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self.show()

    def exibir_resultado_detalhado(self):
        percentual = {}
        resultado = ""

        for nome, quantidade_voto in votos.items():
            percentual[nome] = round((quantidade_voto / num_votos) * 100, 2)

            if percentual[nome].is_integer():
                percentual[nome] = int(percentual[nome])

            if nome == 'branco':
                if quantidade_voto == 1:
                    str_voto_branco = "voto"
                else:
                    str_voto_branco = "votos"
                resultado += f"Votos em branco: {quantidade_voto} {str_voto_branco} ({percentual[nome]}%).\n"
            else:
                if quantidade_voto == 1:
                    str_voto = "voto"
                else:
                    str_voto = "votos"
                resultado += f"O candidato \"{nome}\" obteve {quantidade_voto} {str_voto}, sendo {percentual[nome]}% do total\n"

        return resultado

    def voltar_pagina_anterior(self):
        self.nova_janela = Resultado()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())

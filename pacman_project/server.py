import xmlrpc.server
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from datetime import datetime
import sys

HOST = 'localhost'
PORT = 8000

# Para aparecer o (POST) no log do servidor
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class GameServer:
    def __init__(self):
        self.pontuacao = 0
        self.vidas = 3
        print(f"--- SERVIDOR DBZ PAC-MAN INICIADO EM {HOST}:{PORT} ---")
        print("--- AGUARDANDO CONEXÕES... ---")

    def _hora(self):
        return datetime.now().strftime("%H:%M:%S")

    def resetar_jogo(self):
        self.pontuacao = 0
        self.vidas = 3
        print(f"[{self._hora()}] JOGO: Novo jogo iniciado.")
        sys.stdout.flush()
        return True

    def processar_colisao_item(self, tipo):
        pts = 10 if tipo == "PONTO" else 50
        self.pontuacao += pts
        return self.pontuacao

    def processar_colisao_vilao(self):
        self.vidas -= 1
        print(f"[{self._hora()}] DANO: Colisão detectada! Vidas restantes: {self.vidas}")
        if self.vidas <= 0:
            print(f"[{self._hora()}] GAME OVER: O jogador perdeu todas as vidas.")
        sys.stdout.flush()
        return self.vidas

    def get_estado(self):
        return {"pontuacao": self.pontuacao, "vidas": self.vidas}

    def log_evento(self, categoria, mensagem):
        """
        Recebe logs do cliente (jogo.py) e imprime no terminal do servidor.
        Ex: categoria='AUDIO', mensagem='Som de soco tocando'
        """
        print(f"[{self._hora()}] ➤ {categoria}: {mensagem}")
        sys.stdout.flush()
        return True

# O 'requestHandler' garante que os logs de POST/IP/PORTA continuem aparecendo
server = SimpleXMLRPCServer((HOST, PORT), requestHandler=RequestHandler, allow_none=True)
server.register_instance(GameServer())

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServidor encerrado.")
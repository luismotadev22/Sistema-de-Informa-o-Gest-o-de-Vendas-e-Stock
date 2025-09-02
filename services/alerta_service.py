from dao.alerta_dao import AlertaDAO

class AlertaService:
    def __init__(self):
        self.alerta_dao = AlertaDAO()

    def listar_alertas_ativos(self):
        return self.alerta_dao.listar_ativos()

    def resolver_alerta(self, alerta_id):
        self.alerta_dao.marcar_resolvido(alerta_id)
def criar_modulo(
    nome,
    tipo,
    prioridade,
    combustivel,
    massa,
    criticidade,
    hora_chegada,
    sensor_ok,
    area_livre,
):
    return {
        "nome": nome,
        "tipo": tipo,
        "prioridade": prioridade,
        "combustivel": combustivel,
        "massa": massa,
        "criticidade": criticidade,
        "hora_chegada": hora_chegada,
        "sensor_ok": sensor_ok,
        "area_livre": area_livre,
    }


MODULOS_MISSAO = [
    criar_modulo("HABIT-01", "Habitação", 1, 72, 18.5, 9, 6.0, True, True),
    criar_modulo("ENERG-01", "Energia", 2, 85, 12.0, 8, 7.5, True, True),
    criar_modulo("LAB-01", "Laboratorio", 3, 60, 10.0, 7, 9.0, True, False),
    criar_modulo("LOG-01", "Logística", 4, 45, 22.0, 6, 10.5, True, True),
    criar_modulo("MED-01", "Médico", 1, 90, 8.0, 10, 11.0, True, True),
    criar_modulo("HABIT-02", "Habitação", 2, 30, 18.5, 7, 12.0, False, True),
    criar_modulo("ENERG-02", "Energia", 2, 55, 11.0, 8, 13.5, True, True),
    criar_modulo("LOG-02", "Logística", 3, 20, 24.0, 5, 14.0, True, False),
]

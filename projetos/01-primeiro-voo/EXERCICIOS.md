# Exercícios

Variações ao `primeiro_voo.py`, uma por ficheiro em `exercicios/`. O original fica intacto.

| # | Ficheiro | O que muda | Estado |
|---|---|---|---|
| 1 | `ex1_triangulo.py` | Triângulo em vez de quadrado: (20, 20), (40, 0), casa | feito |
| 2 | `ex2_parametros.py` | Altura e lado passados na linha de comandos (`python3 ex2_parametros.py 15 30`) | feito, falta valor por defeito sem argumentos |
| 3 | `ex3_land.py` | Aterra no último ponto com LAND e só termina quando o drone desarma (lê o HEARTBEAT) | feito |
| 4 | `ex4_tempos.py` | Cronometra cada lado e calcula a velocidade média | feito |
| 5 | | Failsafe de bateria feito no script | por fazer |
| 6 | | Telemetria com `MAV_CMD_SET_MESSAGE_INTERVAL` em vez de tudo a 4 Hz | por fazer |
| 7 | | Círculo de 15 m com 12 pontos | por fazer |

Resultado do exercício 4 (lados de 20 m a 10 m de altura):

```
Tempo: 6.3 s, velocidade: 3.2 m/s
Tempo: 6.0 s, velocidade: 3.3 m/s
Tempo: 5.2 s, velocidade: 3.8 m/s
Tempo: 5.5 s, velocidade: 3.6 m/s
```

O primeiro lado é o mais lento porque o drone parte parado, logo a seguir à descolagem.

## Por fazer

### Ex. 5 · Failsafe de bateria
Antes de cada ponto, lê a bateria. Se estiver abaixo de 30%, imprime um aviso e faz RTL imediatamente.
- **Pista:** mensagem `SYS_STATUS`, campo `battery_remaining` (%). No MAVProxy podes simular bateria fraca com `param set SIM_BATT_CAP_AH 0.5`.
- **Verificação:** com bateria baixa, o drone interrompe o percurso e volta.

### Ex. 6 · Telemetria eficiente
Substitui o `request_data_stream_send` (tudo a 4 Hz) por pedidos individuais:
`GLOBAL_POSITION_INT` a 2 Hz, `LOCAL_POSITION_NED` a 5 Hz, `HEARTBEAT` fica como está.
- **Pista:** comando `MAV_CMD_SET_MESSAGE_INTERVAL` (id 511). `param1` = id da mensagem, `param2` = intervalo em **microssegundos**.
- **Verificação:** grava uma captura nova, corre o `analisar_voo.py` e compara os kbit/s com os 31,5 kbit/s do primeiro voo. Registar a diferença no README.

### Ex. 7 · Desafio: círculo
Voa um círculo de raio 15 m com 12 pontos.
- **Pista:** `math.cos` e `math.sin`, ângulo = 2π · i / 12.
- **Verificação:** um dodecágono quase redondo no QGC.


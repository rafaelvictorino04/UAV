# Como arrancar tudo (do zero até ver o drone a voar)

## Visão geral
```
[arducopter]  ← drone simulado (janela que abre sozinha, não mexer)
     │
[MAVProxy]    ← Terminal 1 (VS Code), onde escreves comandos: STABILIZE>
     ├── UDP 14550 → QGroundControl (mapa)
     └── UDP 14551 → o teu script Python (Terminal 2)
```

## Passo a passo
1. **Abrir o VS Code** na pasta `~/UAV` (File → Open Folder).
2. **Terminal 1: simulador** (no VS Code: Terminal → New Terminal):
   ```bash
   cd ~/UAV/ferramentas/ardupilot
   Tools/autotest/sim_vehicle.py -v ArduCopter --out 127.0.0.1:14551
   ```
   - Abre sozinha uma 2.ª janela (`arducopter`). Deixa-a aberta e não escrevas lá.
   - Espera até aparecer `STABILIZE>` e mensagens tipo `EKF3 IMU0 is using GPS` (~30 s).
3. **Abrir o QGroundControl.** Deve mostrar o drone no mapa e "Ready" no topo.
4. **(Opcional) Wireshark:** interface `Loopback: lo0`, filtro `udp.port == 14551`, iniciar captura.
5. **Terminal 2: script** (no VS Code, botão **+** do painel do terminal):
   ```bash
   cd ~/UAV/projetos/01-primeiro-voo/exercicios
   python3 ex1_triangulo.py
   ```
6. **Ver o voo** no QGroundControl. O script termina sozinho no fim.

## Desligar
1. Terminal 1: `Ctrl + C` (para o MAVProxy e o simulador).
2. Se a janela `arducopter` ficar aberta, fecha-a.
3. Fecha o QGroundControl.

## Problemas comuns
| Sintoma | Causa | Solução |
|---|---|---|
| Script fica parado sem dizer "Ligado ao sistema" | Simulador arrancado sem `--out 127.0.0.1:14551` | No Terminal 1: `output add 127.0.0.1:14551` |
| `TypeError: unsupported operand type(s) for \|` | Terminal a usar Python 3.9 | `source ~/.zshrc` e confirmar `python3 --version` (3.10) |
| "À espera do GPS/EKF para poder armar" várias vezes | GPS simulado ainda não pronto | Esperar ~30 s após arrancar |
| QGC diz "Disconnected" | Simulador não está a correr | Ver Terminal 1 |
| Drone arma e desarma sozinho | Passaram 10 s sem descolar | Fazer `takeoff` logo a seguir ao `arm` |
| `No module named pymavlink` | Falta a biblioteca | `python3 -m pip install pymavlink` |

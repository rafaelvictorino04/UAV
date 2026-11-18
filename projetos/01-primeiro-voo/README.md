# 01 — Primeiro voo autónomo

Script em Python (pymavlink) que liga ao ArduPilot SITL, descola até 10 m, voa um quadrado de 20 m e regressa a casa (RTL).

## Como correr

1. Arrancar o simulador:
   ```bash
   cd ~/UAV/ferramentas/ardupilot
   Tools/autotest/sim_vehicle.py -v ArduCopter --out 127.0.0.1:14551
   ```
2. Abrir o QGroundControl para ver o voo no mapa.
3. Noutro terminal:
   ```bash
   pip3 install pymavlink
   python3 primeiro_voo.py
   ```

## O que aprendi
- 

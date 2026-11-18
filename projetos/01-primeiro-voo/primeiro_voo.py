#!/usr/bin/env python3
"""
Primeiro voo autónomo no ArduPilot SITL.
Descola, voa um quadrado e regressa a casa (RTL).

Uso (com o SITL já a correr noutro terminal):
    pip3 install pymavlink
    python3 primeiro_voo.py
"""
import time
from pymavlink import mavutil

ALT = 10    # altura de voo (m)
LADO = 20   # lado do quadrado (m)

# Arranca o SITL com: sim_vehicle.py -v ArduCopter --out 127.0.0.1:14551
m = mavutil.mavlink_connection("udpin:127.0.0.1:14551")
m.wait_heartbeat()
print(f"Ligado ao sistema {m.target_system}, componente {m.target_component}")

# Pede telemetria a 4 Hz
m.mav.request_data_stream_send(
    m.target_system, m.target_component, mavutil.mavlink.MAV_DATA_STREAM_ALL, 4, 1
)


def modo(nome):
    m.set_mode(nome)
    while True:
        hb = m.recv_match(type="HEARTBEAT", blocking=True)
        if hb.get_srcSystem() == m.target_system and mavutil.mode_string_v10(hb) == nome:
            print(f"Modo: {nome}")
            return


def armar():
    for _ in range(30):
        m.arducopter_arm()
        # Lê os HEARTBEAT dos 2 s seguintes (ignora os antigos que estejam na fila)
        fim = time.time() + 2
        while time.time() < fim:
            hb = m.recv_match(type="HEARTBEAT", blocking=True, timeout=0.5)
            if (hb and hb.get_srcSystem() == m.target_system
                    and hb.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED):
                print("Motores armados")
                return
        print("À espera do GPS/EKF para poder armar...")
    raise SystemExit("Não foi possível armar. Verifica as mensagens PreArm no SITL.")


def descolar(alt):
    m.mav.command_long_send(
        m.target_system, m.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, alt,
    )
    while True:
        msg = m.recv_match(type="GLOBAL_POSITION_INT", blocking=True)
        h = msg.relative_alt / 1000
        print(f"Altura: {h:5.1f} m", end="\r")
        if h >= alt * 0.95:
            print(f"\nNa altura de {alt} m")
            return


def ir_para(norte, este, alt):
    # Posição em metros relativa à origem (NED: z positivo para baixo)
    m.mav.set_position_target_local_ned_send(
        0, m.target_system, m.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b110111111000,          # usa só a posição
        norte, este, -alt,
        0, 0, 0, 0, 0, 0, 0, 0,
    )
    while True:
        p = m.recv_match(type="LOCAL_POSITION_NED", blocking=True)
        dist = ((p.x - norte) ** 2 + (p.y - este) ** 2) ** 0.5
        print(f"A {dist:5.1f} m do ponto ({norte}, {este})", end="\r")
        if dist < 1:
            print(f"\nChegou a ({norte}, {este})")
            return


modo("GUIDED")
armar()
descolar(ALT)
for n, e in [(LADO, 0), (LADO, LADO), (0, LADO), (0, 0)]:
    ir_para(n, e, ALT)
modo("RTL")
print("A regressar a casa e a aterrar. Voo concluído.")

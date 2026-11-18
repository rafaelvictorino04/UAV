#!/usr/bin/env python3
"""
Analisa uma captura do Wireshark (.pcapng, interface loopback) de um voo no ArduPilot SITL.
Reconstrói a linha temporal do voo, os comandos enviados, a telemetria e os pontos de segurança.

Uso:
    pip3 install dpkt pymavlink
    python3 analisar_voo.py Voo.pcapng
"""
import sys
import collections
import dpkt
from pymavlink import mavutil
from pymavlink.dialects.v20 import ardupilotmega as mav2

CMD = {176: "DO_SET_MODE", 400: "ARM/DISARM", 22: "NAV_TAKEOFF", 21: "NAV_LAND", 20: "NAV_RTL"}


def ler_captura(path):
    parsers, msgs, icmp, nbytes = {}, [], [], collections.Counter()
    t0 = t = None
    for ts, buf in dpkt.pcapng.Reader(open(path, "rb")):
        t0 = ts if t0 is None else t0
        t = ts - t0
        try:
            ip = dpkt.loopback.Loopback(buf).data
        except Exception:
            continue
        if not isinstance(ip, dpkt.ip.IP):
            continue
        if isinstance(ip.data, dpkt.icmp.ICMP):
            icmp.append(t)
            continue
        if not isinstance(ip.data, dpkt.udp.UDP):
            continue
        u = ip.data
        key = (u.sport, u.dport)
        nbytes[key] += len(u.data)
        if key not in parsers:
            parsers[key] = mav2.MAVLink(None)
            parsers[key].robust_parsing = True
        try:
            for m in parsers[key].parse_buffer(bytes(u.data)) or []:
                if m.get_type() != "BAD_DATA":
                    msgs.append((t, key, m))
        except Exception:
            pass
    return msgs, icmp, nbytes, t


def main(path):
    msgs, icmp, nbytes, dur = ler_captura(path)
    drone = [(t, k, m) for t, k, m in msgs if m.get_srcSystem() == 1]
    if not drone:
        sys.exit("Não encontrei mensagens MAVLink do drone (sysid 1).")

    fluxos_drone = collections.Counter(k for _, k, _ in drone)
    F = fluxos_drone.most_common(1)[0][0]          # um fluxo de telemetria, para não contar duplicados
    tel = [(t, m) for t, k, m in drone if k == F]

    print(f"\n=== CAPTURA ===\nDuração: {dur:.1f} s | mensagens MAVLink: {len(msgs)} | ICMP: {len(icmp)}")
    print("Fluxos de telemetria do drone (o MAVProxy envia uma cópia para cada saída):")
    for k, n in fluxos_drone.most_common():
        print(f"  {k[0]} -> {k[1]}: {n} mensagens, {nbytes[k] / dur / 1000:.1f} kB/s ({nbytes[k] * 8 / dur / 1000:.1f} kbit/s)")

    print("\n=== LINHA TEMPORAL (HEARTBEAT + STATUSTEXT) ===")
    ultimo = None
    eventos = []
    for t, m in tel:
        if m.get_type() == "HEARTBEAT":
            estado = (mavutil.mode_string_v10(m), bool(m.base_mode & 128), m.system_status)
            if estado != ultimo:
                eventos.append((t, f"modo={estado[0]} armado={estado[1]} estado={'ATIVO' if estado[2] == 4 else 'STANDBY'}"))
                ultimo = estado
        elif m.get_type() == "STATUSTEXT":
            eventos.append((t, f"mensagem: {m.text}"))
    for t, e in eventos:
        print(f"{t:7.2f} s  {e}")

    print("\n=== COMANDOS ENVIADOS AO DRONE ===")
    enviados = [(t, k, m) for t, k, m in msgs if m.get_srcSystem() != 1 and m.get_type() != "HEARTBEAT"]
    vistos = collections.Counter()
    for t, k, m in enviados:
        if m.get_type() == "COMMAND_LONG":
            desc = f"{CMD.get(m.command, m.command)} p1={m.param1:g} p2={m.param2:g} p7={m.param7:g}"
        elif m.get_type() == "SET_POSITION_TARGET_LOCAL_NED":
            desc = f"ir para norte={m.x:g} m, este={m.y:g} m, altura={-m.z:g} m"
        else:
            desc = m.get_type()
        vistos[(round(t, 1), desc)] += 1
    for (t, desc), n in sorted(vistos.items()):
        rep = f"  (x{n})" if n > 1 else ""
        print(f"{t:7.2f} s  {desc}{rep}")
    sysids = collections.Counter(m.get_srcSystem() for _, _, m in msgs if m.get_srcSystem() != 1)
    print("Sysids que enviaram mensagens ao drone:", dict(sysids))

    alt = [(t, m.relative_alt / 1000) for t, m in tel if m.get_type() == "GLOBAL_POSITION_INT"]
    spd = [(t, m.groundspeed) for t, m in tel if m.get_type() == "VFR_HUD"]
    bat = [(t, m.battery_remaining) for t, m in tel if m.get_type() == "SYS_STATUS"]
    no_ar = [t for t, a in alt if a > 0.5]

    print("\n=== VOO ===")
    if no_ar:
        print(f"No ar (> 0,5 m): {no_ar[0]:.1f} s → {no_ar[-1]:.1f} s = {no_ar[-1] - no_ar[0]:.1f} s")
    armado = [t for t, m in tel if m.get_type() == "HEARTBEAT" and m.base_mode & 128]
    if armado:
        print(f"Armado: {armado[0]:.1f} s → {armado[-1]:.1f} s = {armado[-1] - armado[0]:.1f} s")
    print(f"Altura máxima: {max(a for _, a in alt):.2f} m | velocidade máxima: {max(s for _, s in spd):.1f} m/s")
    if bat:
        print(f"Bateria: {bat[0][1]}% → {bat[-1][1]}%")

    gaps = [(a, b) for a, b in zip(icmp, icmp[1:]) if b - a > 1]
    if gaps:
        print("Períodos sem ICMP (script à escuta na 14551):")
        for a, b in gaps:
            print(f"  {a:.1f} s → {b:.1f} s = {b - a:.1f} s")

    print("\n=== SEGURANÇA ===")
    assinadas = sum(1 for _, _, m in msgs if getattr(m, "_signed", False))
    print(f"Mensagens assinadas (MAVLink 2 signing): {assinadas} de {len(msgs)}")
    perdidas, prev = 0, None
    for t, m in tel:
        s = m.get_seq()
        if prev is not None:
            perdidas += (s - prev - 1) % 256
        prev = s
    print(f"Mensagens perdidas (números de sequência em falta): {perdidas}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python3 analisar_voo.py captura.pcapng")
    main(sys.argv[1])

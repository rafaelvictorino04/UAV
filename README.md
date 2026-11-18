# UAV — Aprendizagem

Objetivo: especializar-me em UAVs inteligentes, com foco em **comunicações e segurança**.

## Estrutura

```
UAV/
├── README.md        ← roteiro e estado (este ficheiro)
├── certificados/    ← certificado A1/A3 e futuros (fora do Git)
├── notas/           ← apontamentos (ex.: regras-A1-A3.md)
├── projetos/        ← um projeto por pasta (01-, 02-, ...)
└── recursos/        ← artigos, PDFs, links
```

O ArduPilot fica em `~/ardupilot` (é uma ferramenta, não faz parte deste repositório).

## Estado

- [x] Certificado A1/A3 ANAC/EASA — obtido a 18/11/2026, válido até 18/11/2031
- [ ] Registo de operador em uas.anac.pt (quando tiver drone real com câmara ou > 250 g)
- [ ] ArduPilot SITL + QGroundControl a funcionar no Mac
- [ ] Projeto 01 — primeiro voo autónomo

## Roteiro

### Fase 1 — Como um drone voa
- Conceitos: dinâmica de multirotor, PID, IMU/GPS/barómetro/magnetómetro, EKF, modos de voo
- Ferramentas: ArduPilot, PX4, MAVLink, QGroundControl
- [ ] Projeto 01: voo autónomo com pymavlink (`projetos/01-primeiro-voo`)
- [ ] Capturar o tráfego MAVLink no Wireshark (loopback, `udp.port == 14551`)

### Fase 2 — Comunicações
- Conceitos: link C2, telemetria e vídeo, link budget, propagação ar-solo, drones em LTE/5G (3GPP), FANETs, drone como estação base
- Ferramentas: mavlink-router, ns-3 ou OMNeT++, SDR (RTL-SDR/HackRF) + GNU Radio
- [ ] Projeto 02: telemetria por túnel IPsec/WireGuard, medir latência e perda, testar o failsafe

### Fase 3 — Segurança de UAV
- Ameaças: GPS spoofing, jamming, MAVLink sem autenticação, falsificação de Remote ID, deteção RF (counter-UAS)
- [ ] Projeto 03: GCS intrusa no SITL e mitigação com assinatura MAVLink 2
- ⚠️ Jamming e spoofing de RF real são ilegais — só em simulação ou laboratório controlado

### Fase 4 — Autonomia
- ROS 2 (PX4 via uXRCE-DDS), OpenCV/YOLO, planeamento (A*, RRT), SLAM, enxames
- [ ] Projeto 04: drone no Gazebo que deteta e segue um alvo com a câmara

### Fase 5 — Hardware
- Kit com controladora tipo Pixhawk (PX4/ArduPilot) ou drone < 250 g para começar

## Ambiente

| O quê | Onde / como |
|---|---|
| ArduPilot SITL | `cd ~/ardupilot && Tools/autotest/sim_vehicle.py -v ArduCopter` |
| QGroundControl | liga-se sozinho por UDP 14550 |
| Scripts (pymavlink) | `udpin:127.0.0.1:14551` |

## Recursos

- Documentação: docs.px4.io, ardupilot.org/dev, mavlink.io
- Zeng, Wu, Zhang — *Accessing From the Sky: A Tutorial on UAV Communications for 5G and Beyond* (Proc. IEEE, 2019)
- Beard & McLain — *Small Unmanned Aircraft: Theory and Practice*
- Curso *Aerial Robotics* (UPenn, Coursera)
- Comunidade: discuss.ardupilot.org, discuss.px4.io

## Ecossistema em Portugal

- **IT-Iscte, Grupo de Sistemas de Rádio** (Nuno Souto, Pedro Sebastião) — dissertações em jamming, spoofing GPS e deteção de UAVs com SDR → tema de dissertação
- **Empresas:** Tekever, Beyond Vision (Alverca), UAVision, CEiiA

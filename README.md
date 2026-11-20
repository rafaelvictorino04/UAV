# UAV

Repositório onde registo o que vou aprendendo sobre drones, com foco nas comunicações e na segurança dos links entre o drone e a estação de solo.

Sou aluno do Mestrado em Engenharia de Telecomunicações e Informática (Iscte), na especialização em Cibersegurança. Venho das redes (IPsec, MPLS, FortiGate, automação com n8n) e estou a aplicar essa base aos UAVs. Tenho o certificado de piloto A1/A3 (ANAC/EASA).

## Projetos

| # | Projeto | Estado |
|---|---|---|
| 01 | [Primeiro voo autónomo e análise do tráfego MAVLink](projetos/01-primeiro-voo) | concluído |
| 02 | Telemetria MAVLink por VPN (IPsec/WireGuard), com latência e perda simuladas | a seguir |
| 03 | Estação de solo intrusa no SITL e mitigação com assinatura MAVLink 2 | planeado |

## Ambiente

Tudo corre em simulação, no macOS:

- ArduPilot SITL (ArduCopter), MAVProxy e QGroundControl
- Python 3.10 com pymavlink
- Wireshark com o dissector MAVLink gerado pelo `mavgen`

Os passos para arrancar o simulador estão em [notas/como-arrancar.md](notas/como-arrancar.md).

## Notas

- [Como arrancar o ambiente](notas/como-arrancar.md)
- [Resumo das regras da categoria aberta (A1/A3)](notas/regras-A1-A3.md)

## Próximos passos

- Pôr a telemetria a passar por uma VPN entre duas máquinas e medir o efeito de latência tipo satélite (~600 ms) no failsafe.
- Mostrar no SITL que é possível enviar comandos ao drone a partir de outra estação de solo e testar a assinatura de mensagens do MAVLink 2.
- Mais tarde: ROS 2, visão por computador e hardware real (controladora Pixhawk).

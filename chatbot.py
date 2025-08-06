import json
import os
from datetime import datetime, timedelta

# Caminho do arquivo onde os ciclos são salvos
ARQUIVO = "ciclos.json"

def carregar_ciclos():
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def salvar_ciclos(ciclos):
    with open(ARQUIVO, "w", encoding='utf-8') as f:
        json.dump(ciclos, f, indent=2)

def adicionar_ciclo():
    while True:
        data_str = input("Digite a data do primeiro dia da menstruação (DD/MM/AAAA): ").strip()
        try:
            data = datetime.strptime(data_str, "%d/%m/%Y")
            if data > datetime.now():
                print("Erro: Data no futuro. Digite uma data válida.")
                continue
                
            ciclos = carregar_ciclos()
            if ciclos:
                ultimo_ciclo = datetime.strptime(ciclos[-1], "%d/%m/%Y")
                if data <= ultimo_ciclo:
                    print("Erro: Data anterior ao último ciclo registrado.")
                    continue
                    
            ciclos.append(data_str)
            salvar_ciclos(ciclos)
            print("Ciclo adicionado com sucesso!")
            return
            
        except ValueError:
            print("Formato inválido. Use DD/MM/AAAA.")

def calcular_duracao_ciclos():
    ciclos = carregar_ciclos()
    if len(ciclos) < 2:
        return None
        
    datas = sorted([datetime.strptime(c, "%d/%m/%Y") for c in ciclos])
    diferencas = [(datas[i] - datas[i-1]).days for i in range(1, len(datas))]
    return sum(diferencas) // len(diferencas)

def ver_dia_do_ciclo():
    ciclos = carregar_ciclos()
    if not ciclos:
        print("Nenhum ciclo registrado.")
        return
        
    ultima_data = datetime.strptime(ciclos[-1], "%d/%m/%Y")
    hoje = datetime.now()
    dia_ciclo = (hoje - ultima_data).days + 1
    
    if dia_ciclo <= 0:
        print("Erro: Último ciclo registrado no futuro.")
    else:
        print(f"Você está no dia {dia_ciclo} do seu ciclo.")

def estimar_proxima_menstruacao():
    duracao = calcular_duracao_ciclos()
    if duracao is None:
        print("São necessários ao menos dois ciclos para estimativa.")
        return
        
    ultima_data = datetime.strptime(carregar_ciclos()[-1], "%d/%m/%Y")
    proxima = ultima_data + timedelta(days=duracao)
    print(f"Próxima menstruação prevista: {proxima.strftime('%d/%m/%Y')}")

def estimar_periodo_fertil():
    ciclos = carregar_ciclos()
    if not ciclos:
        print("Nenhum ciclo registrado.")
        return
        
    ultima_data = datetime.strptime(ciclos[-1], "%d/%m/%Y")
    duracao = calcular_duracao_ciclos() or 28  # Default 28 dias se não houver histórico
    
    # Período fértil ocorre geralmente entre os dias 10 a 17 do ciclo
    inicio_fertil = ultima_data + timedelta(days=10)
    fim_fertil = ultima_data + timedelta(days=17)
    
    print("Período fértil estimado:")
    print(f"• Início: {inicio_fertil.strftime('%d/%m/%Y')}")
    print(f"• Término: {fim_fertil.strftime('%d/%m/%Y')}")

def ver_ciclos_salvos():
    ciclos = carregar_ciclos()
    if not ciclos:
        print("Nenhum ciclo registrado.")
        return
        
    print("\nCiclos registrados (mais recente primeiro):")
    for i, ciclo in enumerate(reversed(ciclos), 1):
        print(f"{i}. {ciclo}")

def menu():
    while True:
        print("\n" + "="*40)
        print("MENU PRINCIPAL - ACOMPANHAMENTO MENSTRUAL")
        print("="*40)
        print("1. Ver dia atual do ciclo")
        print("2. Estimar próxima menstruação")
        print("3. Estimar período fértil")
        print("4. Registrar novo ciclo")
        print("5. Histórico de ciclos")
        print("0. Sair")
        
        escolha = input("\nEscolha uma opção: ").strip()
        
        if escolha == "1":
            ver_dia_do_ciclo()
        elif escolha == "2":
            estimar_proxima_menstruacao()
        elif escolha == "3":
            estimar_periodo_fertil()
        elif escolha == "4":
            adicionar_ciclo()
        elif escolha == "5":
            ver_ciclos_salvos()
        elif escolha == "0":
            print("\nAté mais! Cuide da sua saúde.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
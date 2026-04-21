import json
import os

ARQUIVO = "dados.json"
ARQUIVO_TXT = "relatorio.txt"
safras = []

# ------------------ FORMATAÇÃO ------------------
# Essa parte é só para melhorar a visualização dos dados no sistema

def formatar_numero(valor: float) -> str:
    if valor.is_integer():
        return str(int(valor))
    return f"{valor:.2f}".rstrip('0').rstrip('.')

def formatar_moeda(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ------------------ CARREGAR DADOS ------------------
def carregar_dados() -> None:
    global safras

    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                safras = json.load(f)
        except json.JSONDecodeError:
            safras = []
    else:
        safras = []


# ------------------ SALVAR DADOS ------------------
def salvar_dados() -> None:
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(safras, f, indent=4, ensure_ascii=False)  # ensure_ascii=False mantém caracteres especiais no json


# ------------------ VALIDAR NÚMEROS ------------------
def validar_positivo(valor: float, nome: str) -> bool:
    if valor <= 0:
        print(f"Erro: {nome} deve ser maior que zero.")
        return False
    return True


# ------------------ CADASTRAR SAFRA ------------------
def cadastrar_safra() -> None:
    print("\n--- CADASTRAR SAFRA ---")

    try:
        cultura = input("Cultura: ")

        area = float(input("Área plantada (ha): "))
        if not validar_positivo(area, "Área"):
            return

        producao = float(input("Produção (toneladas): "))
        if not validar_positivo(producao, "Produção"):
            return

        custo = float(input("Custo de produção (R$): "))
        if not validar_positivo(custo, "Custo"):
            return

        # gera ID único baseado no maior ID existente
        if safras:
            novo_id = max(s["id"] for s in safras) + 1
        else:
            novo_id = 1

        safra = {
            "id": novo_id,
            "cultura": cultura,
            "area_ha": area,
            "producao_ton": producao,
            "custo": custo,
            "data": input("Data (DD-MM-AAAA): ")
        }

        safras.append(safra)
        salvar_dados()
        print(f"Safra cadastrada com sucesso! ID gerado: {novo_id}")

    except ValueError:
        print("Erro: digite apenas números válidos.")


# ------------------ LISTAR SAFRAS ------------------
def listar_safras() -> None:
    print("\n--- LISTA DE SAFRAS ---")

    if not safras:
        print("Nenhuma safra cadastrada.")
        return

    for s in safras:
        print(f"""
ID: {s['id']}
Cultura: {s['cultura']}
Área: {formatar_numero(s['area_ha'])} ha
Produção: {formatar_numero(s['producao_ton'])} ton
Custo: R$ {formatar_moeda(s['custo'])}
Data: {s['data']}
-----------------------------
        """)


# ------------------ EDITAR SAFRA ------------------
def editar_safra() -> None:
    if not safras:
        print("\nNenhuma safra cadastrada.")
        return

    listar_safras()

    try:
        id_editar = int(input("Digite o ID da safra para editar: "))

        for s in safras:
            if s["id"] == id_editar:

                s["cultura"] = input("Nova cultura: ")

                area = float(input("Nova área (ha): "))
                if not validar_positivo(area, "Área"):
                    return
                s["area_ha"] = area

                producao = float(input("Nova produção (ton): "))
                if not validar_positivo(producao, "Produção"):
                    return
                s["producao_ton"] = producao

                custo = float(input("Novo custo: "))
                if not validar_positivo(custo, "Custo"):
                    return
                s["custo"] = custo

                s["data"] = input("Nova data (DD-MM-AAAA): ")

                salvar_dados()
                print("Safra atualizada!")
                return

        print("ID não encontrado.")

    except ValueError:
        print("Erro: entrada inválida.")


# ------------------ REMOVER SAFRA ------------------
def remover_safra() -> None:
    if not safras:
        print("\nNenhuma safra cadastrada.")
        return

    listar_safras()

    try:
        id_remover = int(input("Digite o ID para remover: "))

        for s in safras:
            if s["id"] == id_remover:
                safras.remove(s)
                salvar_dados()
                print("Safra removida!")
                return

        print("ID não encontrado.")

    except ValueError:
        print("Erro: entrada inválida.")


# ------------------ RELATÓRIO ------------------
def relatorio() -> None:
    print("\n--- RELATÓRIO GERAL ---")

    if not safras:
        print("Sem dados.")
        return

    try:
        total_producao = 0
        for s in safras:
            total_producao += s["producao_ton"]

        total_custo = 0
        for s in safras:
            total_custo += s["custo"]

        total_area = 0
        for s in safras:
            total_area += s["area_ha"]

        produtividade_media = total_producao / total_area

        print(f"Produção total: {formatar_numero(total_producao)} ton")
        print(f"Custo total: R$ {formatar_moeda(total_custo)}")
        print(f"Área total: {formatar_numero(total_area)} ha")
        print(f"Produtividade média: {formatar_numero(produtividade_media)} ton/ha")

        gerar_relatorio_txt(total_producao, total_custo, total_area, produtividade_media)

    except ZeroDivisionError:
        print("Erro: área total não pode ser zero.")


# ------------------ RELATÓRIO TXT ------------------
def gerar_relatorio_txt(total_producao, total_custo, total_area, produtividade_media) -> None:
    with open(ARQUIVO_TXT, "w", encoding="utf-8") as f:
        f.write("RELATÓRIO AGRO CONTROL\n")
        f.write("----------------------\n\n")
        f.write("Resumo Gerencial das Safras\n\n")

        f.write(f"Produção total: {formatar_numero(total_producao)} ton\n")
        f.write(f"Custo total: R$ {formatar_moeda(total_custo)}\n")
        f.write(f"Área total: {formatar_numero(total_area)} ha\n")
        f.write(f"Produtividade média: {formatar_numero(produtividade_media)} ton/ha\n")


# ------------------ MENU ------------------
def menu() -> None:
    carregar_dados()

    while True:
        print("\n===== AGRO CONTROL =====")
        print("1 - Cadastrar safra")
        print("2 - Listar safras")
        print("3 - Editar safra")
        print("4 - Remover safra")
        print("5 - Relatório")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_safra()
        elif opcao == "2":
            listar_safras()
        elif opcao == "3":
            editar_safra()
        elif opcao == "4":
            remover_safra()
        elif opcao == "5":
            relatorio()
        elif opcao == "0":
            salvar_dados()
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


# ------------------ EXECUÇÃO ------------------
menu()
